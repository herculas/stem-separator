"""Validate format, finiteness, and additive reconstruction of refined stems."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np
import soundfile as sf


DEFAULT_TARGETS = (
    "bowed_strings",
    "brass",
    "woodwind",
    "synth",
    "keys",
    "percussion",
    "unclassified_other",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--other", type=Path, required=True)
    parser.add_argument("--refined-dir", type=Path, required=True)
    parser.add_argument("--targets", nargs="+", default=list(DEFAULT_TARGETS))
    return parser.parse_args()


def dbfs(sum_squares: float, sample_count: int) -> float:
    rms = math.sqrt(sum_squares / sample_count)
    return 20.0 * math.log10(max(rms, 1e-12))


def main() -> None:
    args = parse_args()
    paths = [args.refined_dir / f"{target}.wav" for target in args.targets]
    reference_info = sf.info(args.other)
    for path in paths:
        info = sf.info(path)
        if (info.samplerate, info.channels, info.frames, info.subtype) != (
            reference_info.samplerate,
            reference_info.channels,
            reference_info.frames,
            "FLOAT",
        ):
            raise ValueError(f"Format mismatch: {path}: {info}")

    sums = {target: 0.0 for target in args.targets}
    peaks = {target: 0.0 for target in args.targets}
    max_reconstruction_error = 0.0
    sample_count = reference_info.frames * reference_info.channels

    with sf.SoundFile(args.other) as reference, sf.SoundFile(paths[0]) as first:
        handles = [first, *[sf.SoundFile(path) for path in paths[1:]]]
        try:
            while True:
                expected = reference.read(262144, dtype="float32", always_2d=True)
                if not len(expected):
                    break
                actual = np.zeros_like(expected)
                for target, handle in zip(args.targets, handles):
                    block = handle.read(len(expected), dtype="float32", always_2d=True)
                    if len(block) != len(expected) or not np.isfinite(block).all():
                        raise ValueError(f"Invalid audio block: {target}")
                    actual += block
                    sums[target] += float(np.square(block.astype(np.float64)).sum())
                    peaks[target] = max(peaks[target], float(np.abs(block).max()))
                max_reconstruction_error = max(
                    max_reconstruction_error,
                    float(np.abs(expected - actual).max()),
                )
        finally:
            for handle in handles[1:]:
                handle.close()

    for target in args.targets:
        print(f"{target:20s} rms={dbfs(sums[target], sample_count):7.2f} dBFS peak={peaks[target]:.6f}")
    print(f"max_reconstruction_error={max_reconstruction_error:.9g}")
    if max_reconstruction_error > 2e-6:
        raise ValueError("Refined stems do not reconstruct the source other stem")


if __name__ == "__main__":
    main()
