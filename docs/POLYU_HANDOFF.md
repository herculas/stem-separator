# PolyU 开发交接

## 日常同步

VPS 用于文档与项目管理，PolyU 用于代码开发与运行。两端使用
`git@github.com:herculas/stem-separator.git` 的 `main` 作为共同基线。
远程访问前读 [远程操作政策](governance/remote-execution-policy.md)。

1. 在两端确认 `git status --short --branch` 和 `git remote -v`。同步 `main` 时确认
   当前分支为 `main`，工作树干净，再运行 `git pull --ff-only origin main`。有未提交
   改动或分叉时先核对内容。
2. 在 PolyU 开发和验证代码，在 VPS 维护文档与项目记录。提交前检查暂存 diff，
   用现有 `origin` 正常推送已授权的提交，再在另一端快进。新克隆分别执行
   `git config --local core.hooksPath .githooks` 和 `git config --local pull.ff only`。
3. 两端分别执行 `git rev-parse HEAD`，再用 `git ls-remote origin refs/heads/main`
   验证 GitHub。同步完成时三个提交号相同。推送权限或直连受限时，先保留原提交；
   经授权可通过现有 SSH 连接传递经 `git bundle verify` 验证的 Git bundle，再快进。

## Linux 环境初始化

初始基线沿用已验证 Windows 环境的 Python 3.12、PyTorch 2.9.0 和 CUDA 12.8。
Linux 的实际兼容性以 PolyU 验收为准。在获准安装后，从 PolyU 项目根目录执行。
如系统没有 Python 3.12，可用服务器已有的 `uv` 在项目内准备解释器和依赖。

```bash
project_root=$(pwd -P)
export UV_PYTHON_INSTALL_DIR="$project_root/.runtime/python"
export UV_CACHE_DIR="$project_root/.cache/uv"
export UV_PYTHON_CACHE_DIR="$UV_CACHE_DIR/python"
export TMPDIR="$project_root/.work/tmp"
mkdir -p -- "$TMPDIR"
uv venv --python 3.12 .venv
uv pip install --python "$project_root/.venv/bin/python" \
  --index-url https://download.pytorch.org/whl/cu128 'torch==2.9.0+cu128'
uv pip install --python "$project_root/.venv/bin/python" \
  -r requirements.txt 'torch==2.9.0+cu128'
uv pip check --python "$project_root/.venv/bin/python"
```

在非交互 SSH 会话中，若 `uv` 未加入 `PATH`，使用服务器上已核对的可执行文件绝对路径。
以上命令面向新环境，已有 `.venv` 时先核对其用途和状态。PyTorch 安装版本见
[官方版本说明](https://pytorch.org/get-started/previous-versions/)，`uv` 的目录设置见
[官方存储文档](https://docs.astral.sh/uv/reference/storage/)。

## 验收

从 PolyU 工作树执行环境检查，确认 CUDA 张量运算和 CLI 入口均正常。

```bash
"$project_root/.venv/bin/python" -B -c 'import torch; print(torch.__version__, torch.version.cuda); print(torch.ones(1, device="cuda").item())'
"$project_root/.venv/bin/python" -B src/run_bs_roformer.py --help
```

授权首跑时，指定一段可读的短音频，核对 `models/` 的权重目标、`.work/bs-roformer/`
的解码路径和独立输出目录均在预期范围内。第一次运行会下载 BS-RoFormer-SW 模型，
主流程使用 44.1 kHz 双声道解码，并生成六个模型 stem 与 `instrumental`。
核对退出状态、七个 WAV 文件、声道、采样率及音频时长。53-stem 实验另按
[实验说明](OTHER_REFINEMENT.md)独立验收。
