# 执行与存储政策

| 位置 | 职责与内容 |
| --- | --- |
| VPS `~/Developer/StemSeparator` | Git 工作树、文档维护、项目管理、Git 审阅与同步、SSH 控制。可保留待提交的 Git 内容。 |
| PolyU 的 `StemSeparator` 工作树 | 代码开发、依赖安装、测试、音频分轨。项目 `.venv/`、`.runtime/`、`.cache/`、`.work/`、`outputs/`、本机配置与模型权重留在此处。 |
| PolyU 上经授权的外部音频库 | 原始音乐。用 `--input-file` 或本机 `config/local.toml` 指定输入，分轨只读原音频。 |
| GitHub `origin` | 两端共享的版本记录，包括源码、文档、依赖声明、配置模板、模型配置和小型来源记录。 |

PolyU 的实际工作树绝对路径保存在 VPS 的 `stemseparator.remoteRoot` 仓库本地 Git
配置中。执行环境使用该工作树内独立的 `.venv/bin/python`，环境初始化见
[PolyU 交接说明](../POLYU_HANDOFF.md)。旧 Windows 环境按 Linux 的依赖重建。

开始时核对 Git 状态、实际主机和绝对路径，保留两端待提交的改动。需要迁移既有资产时，
先列出明确的源、目的地、大小与校验值，经授权后按清单传输并回读验证。资产清理需单独
授权，Git 忽略规则只决定版本管理边界。

任务结束时确认退出状态与实际输出，检查两端已跟踪、未跟踪和忽略内容的归属。
开发或运行产生的本机文件留在 PolyU。需要同步时核对两端 `HEAD` 和 GitHub 分支提交，
并保留有意留在任一端的工作中改动。
