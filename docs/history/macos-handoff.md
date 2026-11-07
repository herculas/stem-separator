# macOS handoff

This workstation handoff has been retired. The project now uses the
[PolyU development guide](../operations/polyu-development.md) for setup and the
[separation guide](../operations/separation.md) for configuration and validation.

The handoff proposed obtaining code through Git and rebuilding a Python 3.12
virtual environment on the destination. Workstation caches, outputs, music
paths, and checkpoints were machine-local. The same migration principle applies
to PolyU because virtual environments encode platform and absolute paths.

The plan called for syntax and CLI checks followed by a short audio trial,
with seven 44.1 kHz stereo WAVs as the expected result. Apple Silicon MPS was
unverified at handoff. The suggested device order was `mps`, `auto`, then
`cpu`, with slower processing expected on CPU. The archived
[53-stem experiment](other-stem-refinement.md) required additional packages and
checkpoints and had only been exercised on NVIDIA CUDA.
