#!/bin/bash
# Confluence 页面读取脚本
# 用法: confluence-read.sh <page_id> 或 confluence-read.sh <url>

# ============ 配置区域 ============
# 请修改为你的 Confluence 地址和 PAT Token
CONFLUENCE_URL="${CONFLUENCE_URL:-https://your-domain.atlassian.net/wiki}"
CONFLUENCE_PAT="${CONFLUENCE_PAT:-your-personal-access-token}"
# ==================================

# 从参数中提取 page_id
INPUT="$1"

if [ -z "$INPUT" ]; then
    echo "用法: confluence-read.sh <page_id> 或 confluence-read.sh <url>"
    echo "示例: confluence-read.sh 261470646"
    echo "示例: confluence-read.sh https://your-domain/confluence/pages/viewpage.action?pageId=261470646"
    exit 1
fi

# 如果输入是 URL，提取 pageId
if [[ "$INPUT" == *"pageId="* ]]; then
    PAGE_ID=$(echo "$INPUT" | sed -n 's/.*pageId=\([0-9]*\).*/\1/p')
else
    PAGE_ID="$INPUT"
fi

if [ -z "$PAGE_ID" ]; then
    echo "错误: 无法解析 page_id"
    exit 1
fi

# 调用 Confluence API，直接输出 JSON
curl -k -s -H "Authorization: Bearer $CONFLUENCE_PAT" \
    "${CONFLUENCE_URL}/rest/api/content/${PAGE_ID}?expand=body.storage,version"
