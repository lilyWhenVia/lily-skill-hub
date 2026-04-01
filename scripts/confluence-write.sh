#!/bin/bash
# Confluence 页面写入脚本
# 用法: confluence-write.sh <page_id> <title> <content> <version>

# ============ 配置区域 ============
# 请修改为你的 Confluence 地址和 PAT Token
CONFLUENCE_URL="${CONFLUENCE_URL:-https://your-domain.atlassian.net/wiki}"
CONFLUENCE_PAT="${CONFLUENCE_PAT:-your-personal-access-token}"
# ==================================

PAGE_ID="$1"
TITLE="$2"
CONTENT="$3"
VERSION="$4"

if [ -z "$PAGE_ID" ] || [ -z "$TITLE" ] || [ -z "$CONTENT" ] || [ -z "$VERSION" ]; then
    echo "用法: confluence-write.sh <page_id> <title> <content> <version>"
    echo "示例: confluence-write.sh 261470646 '页面标题' '<p>内容</p>' 5"
    exit 1
fi

# 构建 JSON 请求体
JSON_BODY=$(cat <<EOF
{
    "id": "${PAGE_ID}",
    "type": "page",
    "title": "${TITLE}",
    "body": {
        "storage": {
            "value": "${CONTENT}",
            "representation": "storage"
        }
    },
    "version": {
        "number": ${VERSION}
    }
}
EOF
)

# 调用 Confluence API 更新页面
curl -k -s -X PUT \
    -H "Authorization: Bearer $CONFLUENCE_PAT" \
    -H "Content-Type: application/json" \
    -d "$JSON_BODY" \
    "${CONFLUENCE_URL}/rest/api/content/${PAGE_ID}"
