# PolyU Linux runtime validation

On 2026-11-07, PolyU validated the x86-64 Linux environment for commit
[`1dbd448`](https://github.com/herculas/stem-separator/commit/1dbd448de9c33bfc05864d7758ba0b740c35bc13).
Python 3.12.15 ran PyTorch `2.9.0+cu128` on an NVIDIA RTX PRO 6000 Blackwell.
The [dependency lock](../../requirements/linux-cu128.txt) matched all 45
installed packages, and `uv pip check` passed.

| Check | Result |
| --- | --- |
| Runtime | CUDA matrix multiplication, bundled FFmpeg, SoundFile, and help for all four CLI entry points passed. |
| Model | The BS-RoFormer-SW test checkpoint matched the published 699,412,152-byte size and SHA-256. The first download attempt stopped on a redirect outside the initial allowlist. The retry used the verified Hugging Face CDN endpoint. |
| End-to-end separation | The CUDA run used `--track` and a local TOML fixture. A 12-second, 48 kHz mono FLAC produced seven finite, 12-second, 44.1 kHz stereo float WAVs. The source hash matched, the decode was cleaned up, and a duplicate run left the output hashes intact. |
| Historical projection tools | Synthetic projection and reconstruction passed. The runner rejected duplicate targets, and the projection tool rejected an escaping target and an existing output directory. |

The [development guide](../operations/polyu-development.md) owns the current
runtime procedure. The checkpoint and fixtures are isolated in the PolyU run
archive under `work/archive/runtime/linux-bootstrap/2026-11-07/`. At bootstrap
closeout the checkpoint was present only in the archive. The
[separation guide](../operations/separation.md#checkpoint-and-output) records
its subsequent deployment to the standard model directory.
The tests used synthetic audio. The full MSST experiment and real-music quality
assessment remain outside this validation.
