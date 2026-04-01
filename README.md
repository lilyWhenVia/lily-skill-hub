# Lily Skill Hub

自定义 Claude Code Skills 仓库，适用于各类 AI Agent。

## 一键安装

```bash
curl -fsSL https://raw.githubusercontent.com/lilyWhenVia/lily-skill-hub/main/install.sh | bash
```

或手动安装：

```bash
git clone https://github.com/lilyWhenVia/lily-skill-hub.git ~/.claude/commands
cp ~/.claude/commands/scripts/*.sh ~/.claude/scripts/
chmod +x ~/.claude/scripts/*.sh
```

## 可用 Skills

| Skill | 命令 | 说明 |
|-------|------|------|
| [SIT 部署](./docs/sit.md) | `/sit` | 自动提交代码并合并到 SIT 环境 |
| [Confluence 读写](./docs/confluence.md) | `/confluence` | 读写 Confluence 页面（[安装指南](./docs/confluence-setup.md)） |

## 使用方法

在 Claude Code 中直接输入对应命令即可触发，例如：

```
/sit
```

## 目录结构

```
~/.claude/commands/
├── README.md           # 本文件
├── sit.md              # SIT 部署 skill
├── confluence.md       # Confluence 读取 skill
└── docs/               # 各 skill 的详细文档
    ├── sit.md
    └── confluence.md
```

## 贡献

欢迎提交 PR 添加新的 skill！

## 作者

- [@lilyWhenVia](https://github.com/lilyWhenVia)
