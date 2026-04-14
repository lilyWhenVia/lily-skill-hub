# /tidy - 智能目录整理

自主整理目录结构，生成 AI 可读的 .repomap 文件。

## 用法

```
/tidy                  # 无路径 → 强制确认目标
/tidy <path>           # 整理指定目录（相对于工作目录）
/tidy <path> -p        # preview 模式，先确认再执行
/tidy root             # 整理整个工作目录
```

## 参数

- `path`: 目标目录（相对路径），如 `tech`, `workflows`, `docs`
- `root`: 特殊值，表示整个工作目录
- `-p`: preview 模式，执行前展示结构并确认

## 行为规则

### 路径解析
- 相对路径基于当前工作目录解析
- `/tidy tech` → 找工作目录下第一个名为 `tech` 的目录
- 多个匹配时选最浅层级

### 确认机制
- `/tidy` 无参数 → 强制询问目标目录
- `/tidy root` 在非项目目录 → 强制确认
- `/tidy <path>` → 直接执行
- `-p` 参数 → 预览后确认

### 文件过滤（只整理 AI 生成/批量复制的文件）
- 版本号文件: `*-v1.md`, `*_v2.py`
- 批量复制: `file (1).txt`, `*_副本.*`
- 迭代标记: `*-draft`, `*-final`, `*-old`
- 同前缀 ≥3 个文件

### 分类优先级
1. 文件名模式（版本号/日期/前缀）
2. 目录结构暗示
3. 文件内容分析（兜底）

### 永不触碰
- `.git/`, `node_modules/`, `.env*`, `*.lock`, 根目录 `README.md`

## 输出

- 整理后的目录结构
- `.repomap` 文件（目标目录根）

## 示例

```
> /tidy tech

[org] 解析: tech → docs/tech/
[org] 扫描文件...
[org] 按文件名分类: 8 files
[org] 按内容分类: 4 files

整理完成:
├── 移动: 10 files
├── 创建: 4 folders
└── 生成: docs/tech/.repomap
```
