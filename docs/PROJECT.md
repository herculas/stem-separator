# 项目说明

## 当前决策

日常分析统一使用 BS-RoFormer-SW 6-stem。它在本项目的游戏原声测试中表现稳定，
速度约为每首 30–34 秒（具体取决于曲长与机器负载）。53-stem 大类精细化试验
能够产生更多候选轨，但串音和误分类较明显，目前不继续作为默认步骤。

主流程始终直接处理原始音频，不对既有 stem 反复分离。这样可以避免多轮掩码估计
累积伪影。原始音乐库位于项目外部，项目只保存代码、模型配置和生成结果。

## 代码布局

全部可执行代码统一位于 `src/`：

- `src/run_bs_roformer.py`：跨平台 6-stem 主流程。
- `src/other_refinement/`：已归档的 53-stem 实验。

音乐源不属于项目目录。脚本只读取显式传入或 `config/local.toml` 指向的外部音频。

## 已验证环境

- Windows
- NVIDIA GeForce RTX 5070 Ti，16GB 显存
- Python 3.12 虚拟环境：`.venv`
- PyTorch `2.9.0+cu128`
- `bs-roformer-infer 0.1.5`
- `imageio-ffmpeg 0.6.0`
- BS-RoFormer-SW checkpoint：`BS-Rofo-SW-Fixed.ckpt`

主流程已在上述 Windows + CUDA 环境完成端到端测试。macOS 交接步骤见
`docs/MAC_HANDOFF.md`；Apple Silicon MPS 尚待在目标机器上验证。

## 安装

在项目根目录创建虚拟环境。虚拟环境包含平台和绝对路径信息，换机器或操作系统时
必须重建，不能直接复制。

Windows + NVIDIA CUDA：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install torch==2.9.0 `
  --index-url https://download.pytorch.org/whl/cu128
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

macOS：

```shell
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

第一次运行主脚本时，`bs-roformer-infer` 会将 6-stem 模型下载到 `models/`。
模型 checkpoint 不由 Git 跟踪。

## 输入与输出

可直接通过 `--input-file` 传入项目外部音频。可选的本机配置为
`config/local.toml`；它从 `config/local.example.toml` 复制而来，不进入 Git。

输出位于 `outputs/6-stem/<曲名>/`。每首正常包含六个模型 stem 和一个便捷的
`instrumental`，格式为 44.1kHz、双声道、32-bit float WAV。

## 已验证曲目

- `01_01_メインテーマ` — 222.654 秒
- `01_17_敵との対峙 (Definitive Edition ver.)` — 229.834 秒
- `02_17_燐光の地ザトール／夜 (Definitive Edition ver.)` — 约 3:31
- `03_10_名を冠する者たち (Definitive Edition ver.)` — 161.194 秒
- `04_01_堕ちた地で… (Definitive Edition ver.)` — 198.722 秒
- `04_02_堕ちた地で…／夜 (Definitive Edition ver.)` — 约 4:00
- `05_05_ザンザ (Definitive Edition ver.)` — 约 3:20
- `05_08_Beyond the Sky` — 约 4:29

上述结果均已检查文件数量、时长、采样率、声道和非空状态。生成结果保留在
`outputs/6-stem/`，但不会提交到 Git。

## Git 边界

Git 跟踪：

- `src/` 下的 Python 代码
- Markdown 文档
- 依赖清单
- 模型 YAML 与来源/哈希 manifest
- 本机配置模板

Git 忽略：

- `.venv/` 与 `.work/`
- `outputs/` 下的所有分轨结果
- checkpoint 等大型模型权重
- `config/local.toml`
- 常见音频文件，避免误将原始音乐加入仓库
