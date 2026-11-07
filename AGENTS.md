# 项目指引

开始前读 [README.md](README.md) 和 [项目说明](docs/PROJECT.md)，检查
`git status --short --branch`，保留已有改动。任何 PolyU 操作前读
[远程操作政策](docs/governance/remote-execution-policy.md)，选择执行或输出位置前读
[执行与存储政策](docs/governance/execution-and-storage-policy.md)。

- 在 PolyU 工作树开发代码、配置环境、测试和运行分轨。VPS 工作树负责文档、Git
  审阅与同步、项目管理和 SSH 控制。实际 PolyU 别名和目录由 VPS 的仓库本地配置提供。
- 初次远程调查使用有界的只读命令。远程写入需要用户明确授权的绝对路径和范围，
  包括环境、缓存、临时文件和输出。已有的具体授权可继续使用。
- 使用现有 SSH 配置和已验证的主机密钥。VPS 的沙箱无法约束远程账号的权限。
  工作树、原音频、模型、配置和已完成结果均按各自边界保护。
- 使用共同的 GitHub `origin` 同步两端。保持 `core.hooksPath=.githooks`，提交前检查
  暂存内容和 `git diff --cached --check`。冲突或分叉时先核对两端改动。
- Git 保存代码、文档、依赖声明、配置模板和模型 YAML/manifest。真实音频、权重、
  输出、环境、日志、缓存和凭据留在其授权位置。
- PolyU 的环境、Git 操作与首跑验收见 [PolyU 交接说明](docs/POLYU_HANDOFF.md)。
