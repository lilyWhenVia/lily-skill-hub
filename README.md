# Lily Skill Hub

自定义 Claude Code Skills 仓库，适用于各类 AI Agent。

## 安装

将此仓库克隆到 `~/.claude/commands/` 目录：

```bash
git clone https://github.com/lilyWhenVia/lily-skill-hub.git ~/.claude/commands
```

## 可用 Skills

| Skill | 命令 | 说明 |
|-------|------|------|
| [SIT 部署](./docs/sit.md) | `/sit` | 自动提交代码并合并到 SIT 环境 |
| [Confluence 读取](./docs/confluence.md) | `/confluence` | 读取 Confluence 页面内容 |

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
