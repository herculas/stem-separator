# Sonic

跨平台的本地音乐分轨与分析工作区。当前主流程使用 **BS-RoFormer-SW
6-stem**，生成 `bass`、`drums`、`guitar`、`piano`、`vocals`、`other`
以及便于试听的 `instrumental`。

所有可执行代码统一位于 `src/`。53-stem 精细化方案保留在
`src/other_refinement/`，但由于串音与误分类较明显，不属于日常流程。

## 快速开始

Python 3.12 环境安装：

```shell
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
python -m pip install -r requirements.txt
```

Windows PowerShell 中将激活命令替换为 `.\.venv\Scripts\Activate.ps1`。

激活虚拟环境后直接传入项目外部的音乐文件：

```shell
python src/run_bs_roformer.py --input-file "/path/to/track.flac"
```

Apple Silicon 可显式尝试 `--device mps`，NVIDIA 环境可使用
`--device cuda`；默认 `--device auto` 交由依赖库选择设备。

若经常使用同一音乐库，可复制 `config/local.example.toml` 为
`config/local.toml`，随后按文件名运行：

```shell
python src/run_bs_roformer.py --track "track.flac"
```

输出默认写入 `outputs/6-stem/<曲名>/`。原始音乐不会被修改，中间 WAV
会在成功完成后自动删除。

## 目录

```text
sonic/
├── src/                            全部可执行代码
│   ├── run_bs_roformer.py          当前 6-stem 主流程
│   └── other_refinement/           已归档的 53-stem 实验代码
├── config/                         跨平台本机配置模板
├── docs/                           项目说明、实验记录与交接文档
├── models/                         模型配置与本地权重
├── outputs/                        生成结果（Git 忽略）
├── .venv/                          本机 Python 环境（Git 忽略）
└── .work/                          解码缓存（Git 忽略）
```

环境与行为说明见 [项目文档](docs/PROJECT.md)，迁移至 macOS 前请阅读
[Mac 交接说明](docs/MAC_HANDOFF.md)。
