# Sonic

Windows 本地音乐分轨与分析工作区。目前的主流程是使用
**BS-RoFormer-SW 6-stem** 将音乐拆分为：

- `bass`
- `drums`
- `guitar`
- `piano`
- `vocals`
- `other`
- `instrumental`（便于试听的附加轨）

53-stem 精细化方案已经试验过，但当前听感收益有限，因此已归档到
`experiments/other-refinement/`，不属于日常流程。

## 快速开始

默认音乐库配置位于 `config/local.psd1`。当前默认专辑为：

```text
D:\Music\Xenoblade Chronicles 1 Definitive Edition
```

按默认音乐库中的文件名运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run-bs-roformer.ps1 `
  -Track '01_01_メインテーマ.m4a'
```

也可以直接传入任意音乐文件的完整路径：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run-bs-roformer.ps1 `
  -InputFile 'D:\Music\其他专辑\track.flac'
```

输出默认写入 `outputs/6-stem/<曲名>/`，原始音乐不会被修改。中间 WAV
在成功完成后自动删除。

## 目录

```text
sonic/
├── config/                         本机音乐库配置
├── docs/                           环境、流程与历史说明
├── experiments/                    非主流程实验
├── models/                         模型配置与本地权重
├── outputs/                        所有生成结果（Git 忽略）
│   ├── 6-stem/                     当前主流程结果
│   └── experiments/                历史实验结果
├── scripts/                        当前主流程脚本
├── .venv/                          Python 虚拟环境（Git 忽略）
└── .work/                          解码缓存与临时文件（Git 忽略）
```

环境安装、模型行为及验证记录见 [项目文档](docs/PROJECT.md)。
