# Confluence Skill 安装指南

## 快速安装

### 1. 克隆仓库

```bash
git clone https://github.com/lilyWhenVia/lily-skill-hub.git ~/.claude/commands
```

### 2. 配置脚本

将脚本复制到 `~/.claude/scripts/` 目录：

```bash
mkdir -p ~/.claude/scripts
cp ~/.claude/commands/scripts/confluence-*.sh ~/.claude/scripts/
chmod +x ~/.claude/scripts/confluence-*.sh
```

### 3. 设置环境变量

在 `~/.bashrc` 或 `~/.zshrc` 中添加：

```bash
export CONFLUENCE_URL="https://your-domain.atlassian.net/wiki"
export CONFLUENCE_PAT="your-personal-access-token"
```

或者直接修改脚本中的配置区域。

### 4. 获取 PAT Token

#### Atlassian Cloud
1. 访问 https://id.atlassian.com/manage-profile/security/api-tokens
2. 点击 "Create API token"
3. 复制生成的 token

#### Confluence Server/Data Center
1. 访问个人设置 → Personal Access Tokens
2. 创建新 token，勾选 Confluence 权限
3. 复制生成的 token

### 5. 验证安装

```bash
# 测试读取
~/.claude/scripts/confluence-read.sh <your-page-id>
```

## 使用方法

安装完成后，在 Claude Code 中直接使用：

```
读取这个 confluence 页面 https://your-domain/confluence/pages/viewpage.action?pageId=123456
```

或：

```
/confluence
```

## 文件结构

```
~/.claude/
├── commands/           # Skill 定义
│   ├── confluence.md
│   ├── scripts/        # 脚本模板
│   │   ├── confluence-read.sh
│   │   └── confluence-write.sh
│   └── docs/
│       └── confluence.md
└── scripts/            # 实际执行的脚本（包含你的配置）
    ├── confluence-read.sh
    └── confluence-write.sh
```

## 常见问题

### Q: curl 报证书错误
A: 脚本已添加 `-k` 参数跳过证书验证，如需验证请移除该参数

### Q: 返回 401 Unauthorized
A: 检查 PAT token 是否正确，是否有 Confluence 读取权限

### Q: 返回空内容
A: 检查 page_id 是否正确，页面是否存在
