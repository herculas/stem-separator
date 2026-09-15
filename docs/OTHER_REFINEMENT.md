# Other-stem refinement experiment

这是一次基于 MVSep Mega 53 Stems 单目标模型的探索性试验。它分别从原始混音
估计 `bowed_strings`、`brass`、`woodwind`、`synth`、`keys` 和
`percussion`，再将候选结果投影到现有 6-stem 的 `other` 中。

在 `01_01_メインテーマ` 上，流程通过了格式与加和一致性验证，但实际听感中的
串音和类别判断没有达到替代 6-stem 主流程的程度。因此本流程仅作历史记录，默认
不运行。

相关内容：

- `../src/other_refinement/run_other_refinement.py`：实验入口
- `../src/other_refinement/partition_other.py`：时频掩码投影
- `../src/other_refinement/verify_other_refinement.py`：格式与重组误差检查
- `../models/experimental/mvsep-mega-53/`：模型配置、manifest 和本地权重
- `../outputs/experiments/other-refinement/`：生成结果（Git 忽略）

如需复现实验，先生成相同曲目的常规 6-stem，然后运行：

```shell
python src/other_refinement/run_other_refinement.py \
  --input-file "/path/to/track.flac"
```

该实验额外依赖 `requirements-experimental.txt` 中的 MSST 和本地 checkpoint，
目前只在 NVIDIA CUDA 环境中验证过。
