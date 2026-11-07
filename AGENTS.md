# Project agent instructions

Read [README.md](README.md) and the [documentation index](docs/README.md).
Inspect `git status --short --branch` and preserve existing changes.

| Before | Read |
| --- | --- |
| Any PolyU access or operation | [Remote execution policy](docs/governance/remote-execution-policy.md) |
| Choosing a write location, testing, migrating assets, or closing a run | [Execution and storage policy](docs/governance/execution-and-storage-policy.md) |
| Creating, resuming, or archiving a run in `work/` | [Work directory](docs/operations/work-layout.md) |
| Creating, retiring, or moving a document | [Documentation policy](docs/governance/documentation-policy.md) |
| Setting up Linux or synchronizing checkouts | [PolyU development](docs/operations/polyu-development.md) |
| Running separation or changing local settings | [Separation guide](docs/operations/separation.md) |

- Develop and run code on PolyU. Use the VPS for Git, documentation, project
  management, and SSH control. Keep runtime files and bulk assets on PolyU.
- Start remote investigation with bounded reads. Confirm authorization for
  exact remote write paths, including side effects. Use the existing SSH setup
  and the explicit project Python. The VPS sandbox applies to the VPS only.
- Keep `core.hooksPath=.githooks`. Inspect the staged diff, run
  `git diff --cached --check`, and preserve unrelated work on both hosts.
- Update the owning English guide and its index. Keep historical records in
  `docs/history/` and record validation limits where readers will find them.
