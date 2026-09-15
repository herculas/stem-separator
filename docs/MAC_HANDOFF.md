# macOS 开发交接

## 搬迁边界

推荐先在 Windows 端提交并推送本次整理，再通过 Git clone/pull 在 Mac 上取得代码，
而不是复制整个 Windows 目录。
仓库已经将全部代码收敛到 `src/`，音乐源始终位于项目外部。

以下内容不会随 Git 搬迁，也不应直接从 Windows 复制：

- `.venv/`：包含平台和绝对路径信息，必须在 Mac 上重建。
- `.work/` 与 `outputs/`：缓存及生成结果。
- `config/local.toml`：当前机器的音乐库路径。
- `models/**/*.ckpt` 等权重：体积较大且被 Git 忽略；首次主流程运行可重新下载。

## Mac 初始化

建议使用 Python 3.12：

```shell
git clone <repository-url> sonic
cd sonic
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

如果需要按音乐库文件名运行：

```shell
cp config/local.example.toml config/local.toml
```

编辑 `config/local.toml`，将 `music_root` 和 `default_collection` 改为 Mac
上的真实路径。也可以不创建配置，始终使用 `--input-file`。

## 运行与设备

```shell
python src/run_bs_roformer.py \
  --input-file "/Users/your-name/Music/track.flac" \
  --device mps
```

主流程已在 Windows + NVIDIA CUDA 上完成端到端验证，但尚未在 Apple
Silicon 上验证。建议依次尝试 `mps`、`auto`、`cpu`；若上游模型存在尚未
支持的 MPS 算子，`cpu` 是兼容性回退方案，但速度会明显降低。

## 交接验收

安装完成后先执行：

```shell
python -m compileall -q src
python src/run_bs_roformer.py --help
python src/other_refinement/run_other_refinement.py --help
```

再用一段短音频验证主流程。正常结果应包含六个模型 stem 和一个
`instrumental`，均为 44.1 kHz 双声道 WAV。

`src/other_refinement/` 是归档实验，额外依赖
`requirements-experimental.txt`、本地 checkpoint 和当前只在 CUDA
环境验证过的 MSST 流程；Mac 初次接手时无需优先恢复它。
