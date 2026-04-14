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

### 自建 Skills

| Skill | 命令 | 说明 |
|-------|------|------|
| [SIT 部署](./docs/sit.md) | `/sit` | 自动提交代码并合并到 SIT 环境 |
| [Confluence 读写](./docs/confluence.md) | `/confluence` | 读写 Confluence 页面（[安装指南](./docs/confluence-setup.md)） |
| [智能目录整理](./org/skill.md) | `/org` | 自主整理目录结构，生成 AI 可读的 .repomap 文件 |

### 推荐的第三方 Skills

以下是精选的优质第三方 Skills，安装到 `~/.claude/skills/` 目录：

| Skill | 说明 | 安装命令 |
|-------|------|----------|
| [resume-optimization-pro](https://github.com/taielab/resume-optimization-pro) | 8维度评分、迭代优化、面试准备 | `git clone https://github.com/taielab/resume-optimization-pro.git ~/.claude/skills/resume-optimization-pro` |
| [ResumeSkills](https://github.com/Paramchoudhary/ResumeSkills) | ATS优化、求职策略、职业发展 | `git clone https://github.com/Paramchoudhary/ResumeSkills.git ~/.claude/skills/ResumeSkills` |
| [resume-tailoring-skill](https://github.com/varunr89/resume-tailoring-skill) | 针对职位定制简历 | `git clone https://github.com/varunr89/resume-tailoring-skill.git ~/.claude/skills/resume-tailoring-skill` |

**一键安装所有简历相关 Skills：**

```bash
mkdir -p ~/.claude/skills && cd ~/.claude/skills && \
git clone https://github.com/taielab/resume-optimization-pro.git && \
git clone https://github.com/Paramchoudhary/ResumeSkills.git && \
git clone https://github.com/varunr89/resume-tailoring-skill.git
```

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
