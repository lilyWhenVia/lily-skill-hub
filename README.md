# Lily Skill Hub

自定义 Claude Code Skills 仓库。

## 可用 Skills

| Skill | 命令 | 说明 |
|-------|------|------|
| [SIT 部署](./docs/sit.md) | `/sit` | 自动提交代码并合并到 SIT 环境 |
| [Confluence 读写](./docs/confluence.md) | `/confluence` | 读写 Confluence 页面 |
| [智能目录整理](./repomap/skill.md) | `/repomap` | 自主整理目录结构，生成 .repomap |

## 单独安装

### /sit
```bash
curl -fsSL https://raw.githubusercontent.com/lilyWhenVia/lily-skill-hub/main/sit.md -o ~/.claude/commands/sit.md
```

### /confluence
```bash
curl -fsSL https://raw.githubusercontent.com/lilyWhenVia/lily-skill-hub/main/confluence.md -o ~/.claude/commands/confluence.md
```

### /repomap
```bash
curl -fsSL https://raw.githubusercontent.com/lilyWhenVia/lily-skill-hub/main/repomap/install.sh | bash
```

## 全部安装

```bash
curl -fsSL https://raw.githubusercontent.com/lilyWhenVia/lily-skill-hub/main/install.sh | bash
```

## 作者

[@lilyWhenVia](https://github.com/lilyWhenVia)
