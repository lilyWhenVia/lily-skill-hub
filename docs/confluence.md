# /confluence - Confluence 页面读取

读取并解析 Confluence 页面内容。

## 功能

- 从 Confluence URL 中提取 pageId
- 调用 Confluence API 获取页面内容
- 解析并展示页面信息

## 使用方法

直接提供 Confluence 页面 URL：

```
/confluence https://pmo.mcd.com.cn/confluence/pages/viewpage.action?pageId=261470646
```

或者直接说：

```
读取这个 confluence 页面 <URL>
```

## 触发条件

以下输入会触发此 skill：

- "读取 confluence" 或 "读取confluence"
- " confluence URL
- 包含 `pmo.mcd.com.cn/confluence` 的 URL

## 前置要求

需要配置 Confluence 访问脚本：

```bash
~/.claude/scripts/confluence-read.sh
```

## 输出内容

返回 JSON 格式的页面信息：

| 字段 | 说明 |
|------|------|
| `title` | 页面标题 |
| `body.storage.value` | 页面 HTML 内容 |

## 示例

输入：
```
读取这个页面 https://pmo.mcd.com.cn/confluence/pages/viewpage.action?pageId=261470646
```

输出：
```
页面标题: XXX 技术方案
页面内容: ...
```
