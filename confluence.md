# Confluence 页面读取

当用户要求读取 Confluence 页面时，使用此命令。

## 触发条件
用户输入包含以下任意一种：
- "读取 confluence" 或 "读取confluence"
- "读取这个页面" + confluence URL
- "pmo.mcd.com.cn/confluence" URL

## 使用方法

从用户输入中提取 pageId（从 URL 参数 `pageId=xxx` 中提取），然后执行：

```bash
~/.claude/scripts/confluence-read.sh <pageId>
```

## 示例

用户输入: "读取这个页面 https://pmo.mcd.com.cn/confluence/pages/viewpage.action?pageId=261470646"

执行: `~/.claude/scripts/confluence-read.sh 261470646`

## 输出处理

脚本返回 JSON 格式的 Confluence 页面内容，包含：
- `title`: 页面标题
- `body.storage.value`: 页面 HTML 内容

请解析 JSON 并以易读的格式展示给用户。
