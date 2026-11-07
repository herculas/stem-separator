# Windows validation

This is a historical record. Use the [PolyU development guide](../operations/polyu-development.md)
for the current environment and [separation guide](../operations/separation.md)
for the current workflow.

The original Windows + CUDA environment completed end-to-end tests with an
NVIDIA GeForce RTX 5070 Ti (16 GB), Python 3.12, PyTorch `2.9.0+cu128`,
`bs-roformer-infer 0.1.5`, `imageio-ffmpeg 0.6.0`, and
`BS-Rofo-SW-Fixed.ckpt`. Separation took roughly 30–34 seconds per track,
depending on duration and machine load. These are Windows measurements.

| Track ID | English rendering of the recorded title | Duration |
| --- | --- | --- |
| `01_01` | Main Theme | 222.654 s |
| `01_17` | Confronting the Enemy (Definitive Edition ver.) | 229.834 s |
| `02_17` | Phosphorescent Land of Satorl / Night (Definitive Edition ver.) | About 3:31 |
| `03_10` | Those Who Bear Their Names (Definitive Edition ver.) | 161.194 s |
| `04_01` | In the Fallen Land (Definitive Edition ver.) | 198.722 s |
| `04_02` | In the Fallen Land / Night (Definitive Edition ver.) | About 4:00 |
| `05_05` | Zanza (Definitive Edition ver.) | About 3:20 |
| `05_08` | Beyond the Sky | About 4:29 |

The original validation checked file count, duration, sample rate, channels,
and nonempty output for each track. Results were stored locally in
`outputs/6-stem/`. Track IDs map to the original filenames in the
[prior record](https://github.com/herculas/stem-separator/blob/5b8205f31f283c099d680ec2f9f306b499604115/docs/PROJECT.md).
