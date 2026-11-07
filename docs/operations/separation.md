# Six-stem separation

Use BS-RoFormer-SW on the original music mix. Repeated separation of existing
stems can accumulate masking artifacts. The archived
[53-stem experiment](../history/other-stem-refinement.md) documents its separate
use of the `other` stem. Start with the [PolyU environment](polyu-development.md)
and the [remote execution policy](../governance/remote-execution-policy.md).

## Input and optional local configuration

An explicit `--input-file` reads the named file and requires no configuration.
For repeated use of a music library, create the `config/` directory if needed
and write `config/local.toml` on PolyU with these optional settings. The file is
machine-local and Git-ignored.

```toml
music_root = "/path/to/music"
default_collection = "Album Name"
```

| Key | Meaning |
| --- | --- |
| `music_root` | Nonempty string containing the authorized music library's absolute directory. The `--music-root` option overrides it. |
| `default_collection` | Nonempty string containing a collection directory relative to the library. The `--collection` option overrides it. |

`--track` names a file inside that collection and requires both settings,
supplied through the file, flags, or a combination. Run from the project root
with `python` set to its absolute interpreter path.

```bash
"$python" -B src/run_bs_roformer.py --track 'track.flac' --device cuda
```

## Checkpoint and output

The tracked [model config](../../models/roformer-model-bs-roformer-sw-by-jarredou/BS-Rofo-SW-Fixed.yaml)
pairs with the Git-ignored `BS-Rofo-SW-Fixed.ckpt` in the same directory. The
first run can fetch the missing checkpoint through `bs-roformer-infer`.
Before authorizing a fetch, verify the source, redirects, space, and SHA-256
against the [upstream release record](https://pypi.org/project/bs-roformer-infer/0.1.5/).
Apply the same checks when placing an existing copy. The published checkpoint
size is 699,412,152 bytes.

On 2026-11-07, PolyU deployed a verified copy from the
[Linux validation archive](../history/linux-runtime-validation-2026-11-07.md).
The CUDA runner loaded the checkpoint from the default model directory and
produced all seven WAVs from synthetic audio with IPv4 and IPv6 socket creation
blocked. The PolyU run record is under
`.work/archive/runtime/local-checkpoint/2026-11-07/`.

`--device cuda` selects the NVIDIA GPU. The default `auto` delegates device
selection to the inference package. The CLI also accepts `cpu` and `mps`.
FFmpeg decodes to 44.1 kHz stereo. Decodes live under `.work/bs-roformer/` and
are removed on successful runs unless `--keep-decoded-wav` is set. The input
file is read-only. Results go under `outputs/6-stem/<track-stem>/` by default.
The runner refuses an existing track directory. For a retry, use
`--output-root` to choose a fresh authorized location and preserve the previous
output. Inspect paths and symlinks before launching.

## Verify a run

Check the exit status, then read back the seven WAVs. Expect one for each of
`bass`, `drums`, `guitar`, `piano`, `vocals`, `other`, and `instrumental`, all
44.1 kHz stereo 32-bit float with finite samples and the decoded duration.
In the pinned upstream release the convenience `instrumental` is the mix
minus the first configured instrument, which is `bass` in this model YAML.
Use the named `vocals` and instrument stems for downstream work.
