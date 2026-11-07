# Work directory

`work/` is visible and Git-ignored. Keep it on PolyU. Read the
[remote execution policy](../governance/remote-execution-policy.md) and
[storage policy](../governance/execution-and-storage-policy.md) before writing.

| Location | Contents |
| --- | --- |
| `work/runs/<topic>/<task>/<run-id>/` | Active or unresolved run workspaces |
| `work/archive/<topic>/<task>/<run-id>/` | Sealed run evidence, with a closure receipt beside each run |
| `work/scratch/` | Transient decodes, temporary files, and explicitly retained scratch data |
| `work/index.tsv` | Append-only index of closed runs and their receipts |

Use stable lowercase hyphenated topics and tasks. Choose a unique run ID such
as `2026-11-08-01` and use the next free sequence for retries. Reuse the topic
and task for related attempts. Reserve each run directory with an exclusive
create. Create directories only for the work they hold.
Keep operational separation results in `outputs/` or the authorized output
root. Keep model assets in `models/` and runtime caches in `.runtime/cache/`.

## Open a run

Before starting, record the run ID, authorized input and write paths, intended
archive, Git commit and pending changes, command and environment, expected
outputs, limits, progress check, and stop method. Keep logs and status with the
run. Add `input/`, `outputs/`, or `logs/` within it when they help separate
different material. Use original music read-only. Reference existing weights
and other large inputs by path and checksum when the task can reuse them.

Keep ordinary decode and installation scratch files under `work/scratch/`.
Use run-specific scratch paths when they are needed for diagnosis or repeatable
validation. A failed attempt keeps its logs, partials, and exit status. A retry
uses a new run ID and refers to the earlier attempt in its record.

## Close and retain a run

1. Confirm the writers have stopped, record the terminal status and outcome,
   and read back outputs against the acceptance criteria.
2. Seal retained files with a SHA-256 manifest using paths relative to the run.
   Move the closed workspace to its planned archive on the same filesystem
   with a no-replace move. Independently read back the relocated files and
   save `<run-id>-closure.txt` beside the sealed directory.
3. Append a row to `work/index.tsv` with tab-separated columns `topic`, `task`,
   `run_id`, `outcome`, `archive`, and `receipt`. Use paths relative to `work/`.
   Lock the index for the duplicate-key check and append. Use `passed`,
   `failed`, or `stopped` as the outcome. Keep an unresolved run under `runs/`
   with its current state. Update the owning guide for accepted operational
   changes, and keep full evidence on PolyU.

Treat archived files and their manifests as immutable. Retention has no automatic
expiration. Review disk use when planning a large run and classify old scratch,
duplicate copies, and failed results before proposing cleanup. Deletion requires
specific authorization. A sealed archive is evidence and should be referenced
by future runs instead of edited or replayed in place.

## Historical paths

The 2026-11-08 migration moved the former `.work/archive/` tree to `work/archive/`
with the same relative member paths. Existing records may cite `.work/runs/`
for an earlier workspace, or the former registry-based model directory
`models/roformer-model-bs-roformer-sw-by-jarredou/` for a weight now in
`models/bs-roformer-sw/`. Read archived files at their indexed location and
use these mappings when resolving historical paths. The former `.work/tmp/`
and `.work/bs-roformer/` now live under `work/scratch/`.

The accepted migration is recorded under
`work/archive/runtime/layout-migration/2026-11-08-02/`. Its receipt covers the
old archive readbacks, model checksum, offline dependency rebuild, and CUDA
separation from the new model path.
