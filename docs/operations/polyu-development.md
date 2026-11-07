# PolyU development

## Synchronize the checkouts

The VPS and PolyU use the same GitHub `origin` and `main` baseline. Read the
[remote execution policy](../governance/remote-execution-policy.md) before using
SSH. From the VPS checkout, read the destination with
`git config --local --get stemseparator.remoteRoot`.

1. Check `git status --short --branch` and `git remote -v` on both hosts. On a
   clean `main`, update with `git pull --ff-only origin main`. Investigate
   pending changes or a divergence before updating that checkout.
2. Develop and test code on PolyU. Maintain docs and review changes on the VPS.
   Enable the local guards on new clones with `git config --local core.hooksPath
   .githooks` and `git config --local pull.ff only`. Inspect staged changes with
   `git diff --cached` and `git diff --cached --check` before committing.
3. Push the authorized commit to the existing `origin`, then fast-forward the
   other checkout. Compare each `git rev-parse HEAD` with
   `git ls-remote origin refs/heads/main`. If direct transfer is unavailable,
   preserve the commits and use an authorized, verified Git bundle over the
   existing SSH connection.

## Provision Linux

The PolyU baseline is x86-64 Linux, Python 3.12.15, and PyTorch 2.9.0 with
CUDA 12.8. [The Linux dependency lock](../../requirements/linux-cu128.txt)
captures the resolved versions. [Main requirements](../../requirements/base.txt)
declare the portable top-level dependencies. Use the existing `uv` executable.
If it is outside `PATH` in a noninteractive session, use its verified absolute
path. Check the [storage policy](../governance/execution-and-storage-policy.md)
and the status of any existing `.runtime/venv/` before provisioning. The commands below
assume a fresh, authorized environment and run from the PolyU project root.

```bash
project_root=$(pwd -P)
export UV_PYTHON_INSTALL_DIR="$project_root/.runtime/python"
export UV_CACHE_DIR="$project_root/.runtime/cache/uv"
export UV_PYTHON_CACHE_DIR="$UV_CACHE_DIR/python"
export XDG_CACHE_HOME="$project_root/.runtime/cache"
export TMPDIR="$project_root/work/scratch/tmp"
mkdir -p -- "$TMPDIR"

uv --no-config venv --no-project --managed-python --python 3.12.15 .runtime/venv
python="$project_root/.runtime/venv/bin/python"
uv --no-config pip install --python "$python" -c requirements/linux-cu128.txt \
  --index-url https://download.pytorch.org/whl/cu128 'torch==2.9.0+cu128'
uv --no-config pip install --python "$python" -c requirements/linux-cu128.txt \
  --index-url https://pypi.org/simple -r requirements/base.txt 'torch==2.9.0+cu128'
uv --no-config pip check --python "$python"
```

PyTorch publishes the matching wheel on its CUDA 12.8 index.
[PyTorch release instructions](https://pytorch.org/get-started/previous-versions/)
and [uv storage settings](https://docs.astral.sh/uv/reference/storage/) document
the package source and local storage controls.

Keep the base interpreter under `.runtime/python/`, installed dependencies in
`.runtime/venv/`, and package and compiler caches under `.runtime/cache/`.
The active virtual environment was rebuilt in place at its new path using the
existing `uv` cache and dependency lock. The previous root-level environment is
preserved at `.runtime/retired/venv-2026-11-08/` as a rollback copy. Its launchers
still use the original path. A rollback requires an authorized restoration to
that path and runtime validation before use.

## Validate the environment

Set the cache paths within the authorized project scope before invoking CUDA.
Compare `uv pip freeze --python "$python"` with the Linux dependency lock and
verify the bundled FFmpeg executable and SoundFile imports.

```bash
export CUDA_CACHE_PATH="$project_root/.runtime/cache/cuda"
export TRITON_CACHE_DIR="$project_root/.runtime/cache/triton"
export PYTHONDONTWRITEBYTECODE=1
"$python" -B -c 'import torch; print(torch.__version__, torch.version.cuda); print(torch.ones(1, device="cuda").item())'
"$python" -B src/run_bs_roformer.py --help
```

For end-to-end validation, use the [separation guide](separation.md#verify-a-run)
with a short, authorized fixture in a new run directory. The
[PolyU acceptance record](../history/linux-runtime-validation-2026-11-07.md)
lists the checks performed and their limits. The archived
[53-stem experiment](../history/other-stem-refinement.md) uses separate
dependencies and checkpoints.
