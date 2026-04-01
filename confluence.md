# Confluence 页面读写

读取和写入 Confluence 页面内容。

## 触发条件

用户输入包含以下任意一种：
- "读取 confluence" 或 "读取confluence"
- "写入 confluence" 或 "更新confluence"
- "读取这个页面" + confluence URL
- "pmo.mcd.com.cn/confluence" URL

## 读取页面

### 使用方法

从用户输入中提取 pageId（从 URL 参数 `pageId=xxx` 中提取），然后**直接执行脚本**（无需询问用户）：

```bash
~/.claude/scripts/confluence-read.sh <pageId>
```

### 自动执行规则

当用户输入包含 Confluence URL 时，**立即自动执行**读取脚本，不需要额外确认：
1. 从 URL 中提取 `pageId` 参数
2. 执行 `~/.claude/scripts/confluence-read.sh <pageId>`
3. 解析返回的 JSON 并以易读格式展示

### 示例

用户输入: "读取这个页面 https://pmo.mcd.com.cn/confluence/pages/viewpage.action?pageId=261470646"

**直接执行**: `~/.claude/scripts/confluence-read.sh 261470646`

### 输出处理

脚本返回 JSON 格式的 Confluence 页面内容，包含：
- `title`: 页面标题
- `body.storage.value`: 页面 HTML 内容

请解析 JSON 并以易读的 Markdown 格式展示给用户（转换 HTML 标签为 Markdown）。

## 写入页面

### 使用方法

1. 先读取页面获取当前版本号
2. 根据用户需求修改内容
3. 调用写入脚本更新页面

```bash
~/.claude/scripts/confluence-write.sh <pageId> <title> <content> <version>
```

参数说明：
- `pageId`: 页面 ID
- `title`: 页面标题
- `content`: 页面内容（Confluence Storage Format，即 XHTML）
- `version`: 当前版本号 + 1

### 写入流程

1. 读取页面获取当前 `version.number`
2. 确认用户要修改的内容
3. 生成新的页面内容（保持 Confluence Storage Format）
4. 调用写入脚本，version 参数为当前版本号 + 1
5. 返回更新结果

### 示例

用户输入: "在这个页面末尾添加一段内容：## 新增章节\n这是新内容"

执行流程：
1. `~/.claude/scripts/confluence-read.sh 261470646` 获取当前内容和版本号
2. 在 body 末尾追加用户指定的内容
3. `~/.claude/scripts/confluence-write.sh 261470646 "页面标题" "<新内容>" 5`

### 内容格式

Confluence 使用 Storage Format（XHTML），常用标签：
- `<p>段落</p>`
- `<h1>标题1</h1>` ~ `<h6>标题6</h6>`
- `<ul><li>列表项</li></ul>`
- `<ol><li>有序列表</li></ol>`
- `<table><tr><td>表格</td></tr></table>`
- `<ac:structured-macro ac:name="code">` 代码块

### 注意事项

- 写入前必须先读取页面获取最新版本号
- 版本号冲突会导致写入失败，需重新读取后再试
- 写入操作会覆盖整个页面内容，请确保内容完整
- 建议写入前先确认用户意图，避免误操作
