# Execution and storage policy

| Location | Work and materials |
| --- | --- |
| VPS `~/Developer/StemSeparator` | Git-managed source, docs, dependency declarations, model metadata, compact receipts, pending Git changes, and SSH control |
| PolyU project checkout | Code development, runtime installation, tests, separation, local configuration, models, caches, logs, workspaces, and outputs |
| Authorized audio library | Original mixes, read as input to the project |
| Shared GitHub `origin` | Versioned code, docs, dependency declarations, model metadata, and compact nonsensitive evidence |

The VPS checkout's local Git config records the PolyU project root. Use the
project's absolute `.runtime/venv/bin/python` path on PolyU. Read the
[remote execution policy](remote-execution-policy.md) before any remote action.
Use the [development guide](../operations/polyu-development.md) to synchronize Git.

## Run and archive

Use the [work directory procedure](../operations/work-layout.md) for new
validations and multi-step runs. Choose the authorized workspace and final
archive before execution. Keep logs, source snapshots, temporary files,
failures, and partials within the approved scope. Use an explicitly authorized
output directory for normal separation. Protect original inputs, weights,
accepted results, and sealed archives.

## Git and transfer boundaries

Git tracks maintained code under `src/`, model configuration and manifests,
docs, dependency declarations, and compact records. Environments, local TOML,
audio, weights, full runs, and credentials stay in their approved local paths.
Keep `core.hooksPath=.githooks` and inspect the staged diff before a commit.

For a migration, inventory exact source paths, sizes, and hashes. Transfer only
the authorized inventory into absent destinations and independently read back
the destination bytes. Source removal requires its own authorization and a
check that the original bytes still match. Git exclusion and reconstructability
establish file classification. Deletion requires separate authorization.

At closeout, inspect tracked, untracked, and ignored content and retain pending
Git work. Compare both checkouts with the GitHub branch for synchronized changes.
