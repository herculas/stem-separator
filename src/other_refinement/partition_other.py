"""Project broad instrument estimates into an existing six-stem ``other`` track.

The specialist models are run on the original mix, so their raw estimates can
overlap.  This script turns those estimates into a conservative, additive view
of the existing ``other`` stem.  It uses stereo-linked STFT masks and writes an
exact time-domain residual named ``unclassified_other.wav``.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import soundfile as sf
import torch


DEFAULT_TARGETS = (
    "bowed_strings",
    "brass",
    "woodwind",
    "synth",
    "keys",
    "percussion",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--other", type=Path, required=True)
    parser.add_argument("--candidates-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--targets", nargs="+", default=list(DEFAULT_TARGETS))
    parser.add_argument("--chunk-seconds", type=float, default=20.0)
    parser.add_argument("--context-seconds", type=float, default=2.0)
    return parser.parse_args()


def audio_info(path: Path) -> sf.SoundFile:
    if not path.is_file():
        raise FileNotFoundError(path)
    return sf.info(path)


def read_segment(path: Path, start: int, frames: int) -> np.ndarray:
    with sf.SoundFile(path) as handle:
        handle.seek(start)
        audio = handle.read(frames, dtype="float32", always_2d=True)
    return audio


def stft(audio: np.ndarray, window: torch.Tensor, n_fft: int, hop: int) -> torch.Tensor:
    tensor = torch.from_numpy(audio.T.copy())
    return torch.stft(
        tensor,
        n_fft=n_fft,
        hop_length=hop,
        win_length=n_fft,
        window=window,
        center=True,
        return_complex=True,
    )


def istft(spec: torch.Tensor, window: torch.Tensor, n_fft: int, hop: int, length: int) -> np.ndarray:
    audio = torch.istft(
        spec,
        n_fft=n_fft,
        hop_length=hop,
        win_length=n_fft,
        window=window,
        center=True,
        length=length,
    )
    return audio.T.cpu().numpy().astype(np.float32, copy=False)


def main() -> None:
    args = parse_args()
    other_info = audio_info(args.other)
    if other_info.channels != 2:
        raise ValueError(f"Expected stereo other stem, got {other_info.channels} channels")

    candidate_paths = {target: args.candidates_dir / f"{target}.wav" for target in args.targets}
    for target, path in candidate_paths.items():
        info = audio_info(path)
        if (info.samplerate, info.channels, info.frames) != (
            other_info.samplerate,
            other_info.channels,
            other_info.frames,
        ):
            raise ValueError(f"Audio format mismatch for {target}: {info}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_paths = {target: args.output_dir / f"{target}.wav" for target in args.targets}
    output_paths["unclassified_other"] = args.output_dir / "unclassified_other.wav"

    writers = {
        name: sf.SoundFile(
            path,
            mode="w",
            samplerate=other_info.samplerate,
            channels=other_info.channels,
            subtype="FLOAT",
        )
        for name, path in output_paths.items()
    }

    n_fft = 2048
    hop = 512
    window = torch.hann_window(n_fft)
    chunk_frames = max(int(args.chunk_seconds * other_info.samplerate), n_fft * 2)
    context_frames = max(int(args.context_seconds * other_info.samplerate), n_fft)
    epsilon = 1e-8

    try:
        for core_start in range(0, other_info.frames, chunk_frames):
            core_end = min(core_start + chunk_frames, other_info.frames)
            read_start = max(0, core_start - context_frames)
            read_end = min(other_info.frames, core_end + context_frames)
            segment_frames = read_end - read_start
            left = core_start - read_start
            right = left + (core_end - core_start)

            other_audio = read_segment(args.other, read_start, segment_frames)
            other_spec = stft(other_audio, window, n_fft, hop)

            scores = []
            amplitudes = []
            for path in candidate_paths.values():
                candidate = read_segment(path, read_start, segment_frames)
                candidate_spec = stft(candidate, window, n_fft, hop)
                power = candidate_spec.abs().square().mean(dim=0)
                scores.append(power)
                amplitudes.append(power.sqrt())

            score_stack = torch.stack(scores, dim=0)
            amplitude_stack = torch.stack(amplitudes, dim=0)
            score_total = score_stack.sum(dim=0)
            shares = score_stack / (score_total.unsqueeze(0) + epsilon)

            other_amplitude = other_spec.abs().square().mean(dim=0).sqrt()
            # A max-based coverage estimate prevents overlapping specialist
            # predictions from consuming the residual merely because many
            # models emitted the same sound.
            coverage = torch.clamp(
                amplitude_stack.max(dim=0).values / (other_amplitude + epsilon),
                min=0.0,
                max=1.0,
            )
            weights = shares * coverage.unsqueeze(0)

            candidate_cores: list[np.ndarray] = []
            for index, target in enumerate(args.targets):
                projected_spec = other_spec * weights[index].unsqueeze(0)
                projected = istft(projected_spec, window, n_fft, hop, segment_frames)
                core = projected[left:right]
                candidate_cores.append(core)
                writers[target].write(core)

            other_core = other_audio[left:right]
            residual = other_core - np.sum(candidate_cores, axis=0)
            writers["unclassified_other"].write(residual.astype(np.float32, copy=False))
    finally:
        for writer in writers.values():
            writer.close()

    print(f"Partitioned {other_info.frames / other_info.samplerate:.3f}s into {len(output_paths)} stems")


if __name__ == "__main__":
    main()
