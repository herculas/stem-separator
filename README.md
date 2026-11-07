# StemSeparator

StemSeparator separates original music mixes with BS-RoFormer-SW. The default
pipeline writes `bass`, `drums`, `guitar`, `piano`, `vocals`, `other`, and an
additional `instrumental` WAV for listening.

PolyU hosts development, tests, and runs. The VPS checkout handles documentation,
project management, Git synchronization, and SSH control. Start with the
[documentation index](docs/README.md) and the [agent instructions](AGENTS.md).

## Run a track

From the PolyU checkout, use the [project Python environment](docs/operations/polyu-development.md).

```bash
project_root=$(pwd -P)
"$project_root/.runtime/venv/bin/python" -B src/run_bs_roformer.py \
  --input-file /path/to/track.flac --device cuda
```

See the [separation guide](docs/operations/separation.md) for model setup, optional
music-library configuration, and output checks. See [history](docs/history/README.md)
for the Windows results, retired macOS handoff, and 53-stem experiment.

## Repository layout

| Path | Contents |
| --- | --- |
| `src/` | The main pipeline and preserved experimental code |
| `docs/` | Current guides and policies, plus separate historical records |
| `models/` | Tracked model YAML and manifests alongside ignored weights |
| `requirements/` | Main, Linux CUDA, and experimental dependency declarations |
| `config/local.toml` | Optional machine-local music library settings, Git-ignored |
| `.githooks/` | Staged-content checks for placement, credentials, and size |
| `.runtime/` | PolyU-local Python, virtual environment, and caches |
| `work/`, `outputs/` | PolyU-local run evidence, scratch space, and separation results |
