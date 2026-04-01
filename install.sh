#!/bin/bash
# Lily Skill Hub 一键安装脚本
# 用法: curl -fsSL https://raw.githubusercontent.com/lilyWhenVia/lily-skill-hub/main/install.sh | bash

set -e

echo "🚀 开始安装 Lily Skill Hub..."

# 1. 克隆仓库
COMMANDS_DIR="$HOME/.claude/commands"
if [ -d "$COMMANDS_DIR/.git" ]; then
    echo "📦 更新已有仓库..."
    cd "$COMMANDS_DIR" && git pull origin main
else
    echo "📦 克隆仓库..."
    mkdir -p "$HOME/.claude"
    git clone https://github.com/lilyWhenVia/lily-skill-hub.git "$COMMANDS_DIR"
fi

# 2. 复制脚本
SCRIPTS_DIR="$HOME/.claude/scripts"
mkdir -p "$SCRIPTS_DIR"
cp "$COMMANDS_DIR/scripts/"*.sh "$SCRIPTS_DIR/" 2>/dev/null || true
chmod +x "$SCRIPTS_DIR/"*.sh 2>/dev/null || true

echo ""
echo "✅ 安装完成！"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 下一步：配置 Confluence（可选）"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "在 ~/.bashrc 或 ~/.zshrc 中添加："
echo ""
echo "  export CONFLUENCE_URL=\"https://your-domain.atlassian.net/wiki\""
echo "  export CONFLUENCE_PAT=\"your-personal-access-token\""
echo ""
echo "然后执行: source ~/.bashrc"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 可用的 Skills："
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  /sit         - 提交代码到 SIT 环境"
echo "  /confluence  - 读写 Confluence 页面"
echo ""
echo "在 Claude Code 中直接输入命令即可使用！"
