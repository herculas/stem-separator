"""Run the archived MVSep Mega 53 other-stem refinement experiment."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

import imageio_ffmpeg


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_ROOT = PROJECT_ROOT / "models" / "experimental" / "mvsep-mega-53"
TARGETS = ("bowed_strings", "brass", "woodwind", "synth", "keys", "percussion")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-file", type=Path, required=True)
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--existing-stems-root", type=Path)
    parser.add_argument("--targets", nargs="+", choices=TARGETS, default=list(TARGETS))
    parser.add_argument("--device-ids", nargs="+", default=["0"])
    parser.add_argument("--keep-decoded-wav", action="store_true")
    return parser.parse_args()


def run(args: argparse.Namespace) -> Path:
    source = args.input_file.expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(source)

    output_root = (
        args.output_root or PROJECT_ROOT / "outputs" / "experiments" / "other-refinement"
    ).resolve()
    existing_root = (args.existing_stems_root or PROJECT_ROOT / "outputs" / "6-stem").resolve()
    existing_other = existing_root / source.stem / f"{source.stem}_other.wav"
    if not existing_other.is_file():
        raise FileNotFoundError(
            f"existing six-stem other track not found: {existing_other}"
        )

    work_dir = PROJECT_ROOT / ".work" / "experiments" / "other-refinement" / source.stem
    decoded_wav = work_dir / f"{source.stem}.wav"
    track_output = output_root / source.stem
    raw_output = track_output / "raw_candidates"
    consistent_output = track_output / "consistent_stems"
    partition_script = Path(__file__).with_name("partition_other.py")
    mpl_config = PROJECT_ROOT / ".work" / "matplotlib"
    for directory in (work_dir, raw_output, consistent_output, mpl_config):
        directory.mkdir(parents=True, exist_ok=True)

    environment = os.environ.copy()
    environment["MPLCONFIGDIR"] = str(mpl_config)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    print(f"Decoding original mix: {source}", flush=True)
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
            "pcm_f32le",
            str(decoded_wav),
        ],
        check=True,
    )

    for target in args.targets:
        model_base = f"bs_mega_53stem_{target}_mvsep"
        config = MODEL_ROOT / f"{model_base}.yaml"
        checkpoint = MODEL_ROOT / f"{model_base}.ckpt"
        for asset in (config, checkpoint):
            if not asset.is_file():
                raise FileNotFoundError(asset)

        print(f"Separating candidate: {target}", flush=True)
        subprocess.run(
            [
                sys.executable,
                "-c",
                "from msst.cli import main; main()",
                "inference",
                "--model_type",
                "bs_roformer",
                "--config_path",
                str(config),
                "--start_check_point",
                str(checkpoint),
                "--input_folder",
                str(work_dir),
                "--store_dir",
                str(raw_output),
                "--device_ids",
                *args.device_ids,
                "--pcm_type",
                "FLOAT",
                "--filename_template",
                "{instr}",
                "--disable_detailed_pbar",
            ],
            cwd=PROJECT_ROOT,
            env=environment,
            check=True,
        )

    print("Projecting candidates into the existing other stem", flush=True)
    subprocess.run(
        [
            sys.executable,
            str(partition_script),
            "--other",
            str(existing_other),
            "--candidates-dir",
            str(raw_output),
            "--output-dir",
            str(consistent_output),
            "--targets",
            *args.targets,
        ],
        cwd=PROJECT_ROOT,
        check=True,
    )

    if not args.keep_decoded_wav:
        decoded_wav.unlink(missing_ok=True)
    print(f"Completed: {track_output}")
    return track_output


def main() -> None:
    try:
        run(parse_args())
    except (FileNotFoundError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"error: {error}") from error


if __name__ == "__main__":
    main()
