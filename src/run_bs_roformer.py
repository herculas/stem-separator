"""Cross-platform BS-RoFormer six-stem runner for the Sonic workspace."""

from __future__ import annotations

import argparse
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Any

import imageio_ffmpeg


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "local.toml"
DEFAULT_MODEL = "roformer-model-bs-roformer-sw-by-jarredou"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run six-stem BS-RoFormer separation")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--input-file", type=Path, help="audio file to separate")
    source.add_argument("--track", help="filename inside the configured music collection")
    parser.add_argument("--music-root", type=Path, help="override config music_root")
    parser.add_argument("--collection", help="override config default_collection")
    parser.add_argument("--output-root", type=Path)
    parser.add_argument(
        "--device",
        choices=("auto", "cuda", "mps", "cpu"),
        default="auto",
        help="inference device; auto lets bs-roformer-infer choose",
    )
    parser.add_argument("--keep-decoded-wav", action="store_true")
    return parser.parse_args()


def load_local_config() -> dict[str, Any]:
    if not DEFAULT_CONFIG.is_file():
        return {}
    with DEFAULT_CONFIG.open("rb") as handle:
        return tomllib.load(handle)


def resolve_source(args: argparse.Namespace) -> Path:
    if args.input_file is not None:
        source = args.input_file.expanduser()
    else:
        config = load_local_config()
        music_root = args.music_root or config.get("music_root")
        collection = args.collection or config.get("default_collection")
        if not music_root or not collection:
            raise ValueError(
                "--track requires --music-root and --collection, or config/local.toml"
            )
        source = Path(music_root).expanduser() / collection / args.track

    source = source.resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    return source


def run(args: argparse.Namespace) -> Path:
    source = resolve_source(args)
    models_dir = PROJECT_ROOT / "models"
    work_dir = PROJECT_ROOT / ".work" / "bs-roformer" / source.stem
    decoded_wav = work_dir / f"{source.stem}.wav"
    output_root = (args.output_root or PROJECT_ROOT / "outputs" / "6-stem").resolve()
    track_output = output_root / source.stem

    for directory in (models_dir, work_dir, track_output):
        directory.mkdir(parents=True, exist_ok=True)

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    print(f"Decoding: {source}", flush=True)
    subprocess.run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(source),
            "-vn",
            "-map_metadata",
            "-1",
            "-ac",
            "2",
            "-ar",
            "44100",
            "-c:a",
            "pcm_s24le",
            str(decoded_wav),
        ],
        check=True,
    )

    print(f"Separating on device: {args.device}", flush=True)
    command = [
        sys.executable,
        "-c",
        "from bs_roformer.inference import main; main()",
        "--model",
        DEFAULT_MODEL,
        "--models_dir",
        str(models_dir),
        "--input_folder",
        str(work_dir),
        "--store_dir",
        str(track_output),
    ]
    if args.device != "auto":
        command.extend(("--device", args.device))
    subprocess.run(command, cwd=PROJECT_ROOT, check=True)

    if not args.keep_decoded_wav:
        decoded_wav.unlink(missing_ok=True)

    print(f"Completed: {track_output}")
    return track_output


def main() -> None:
    try:
        run(parse_args())
    except (FileNotFoundError, ValueError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"error: {error}") from error


if __name__ == "__main__":
    main()
