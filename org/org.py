"""
/org skill - 智能目录整理
自主整理目录结构，生成 AI 可读的 .repomap 文件
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict


# ============== 配置 ==============

# 项目标识文件
PROJECT_MARKERS = [".git", "package.json", "CLAUDE.md", ".kiro", "pom.xml", "Cargo.toml", "pyproject.toml"]

# 危险目录模式
DANGEROUS_DIRS = [
    r"^[A-Z]:/Users/[^/]+/?$",  # C:/Users/xxx/
    r"^[A-Z]:/?$",               # C:/
    r"^/home/[^/]+/?$",          # /home/xxx/
    r"^~/?$",                    # ~/
]

# 永不触碰
NEVER_TOUCH = [
    ".git", "node_modules", "__pycache__", ".venv", "venv",
    ".env", ".env.*", "*.lock", ".DS_Store", "Thumbs.db",
]

# 版本号模式
VERSION_PATTERN = re.compile(r'[-_]v?(\d+\.?\d*)(?:\.[a-z]+)?$', re.IGNORECASE)
DATE_PATTERN = re.compile(r'(\d{4})[-_]?(\d{2})[-_]?(\d{2})')
COPY_PATTERN = re.compile(r'\s*\(\d+\)|[-_](copy|副本|复制|backup|bak|old|new|draft|final|temp)', re.IGNORECASE)


# ============== 路径解析 ==============

def resolve_path(arg: str, cwd: str) -> str:
    """解析相对路径"""
    if not arg or arg.strip() == "":
        return None  # 需要确认

    if arg == "root":
        return cwd

    # 直接拼接
    direct = os.path.join(cwd, arg)
    if os.path.isdir(direct):
        return direct

    # 递归搜索
    for root, dirs, _ in os.walk(cwd):
        # 跳过隐藏目录和 node_modules
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in NEVER_TOUCH]
        if arg in dirs:
            return os.path.join(root, arg)

    return None


def is_project_dir(path: str) -> bool:
    """检查是否是项目目录"""
    for marker in PROJECT_MARKERS:
        if os.path.exists(os.path.join(path, marker)):
            return True
    return False


def is_dangerous_dir(path: str) -> bool:
    """检查是否是危险目录"""
    normalized = path.replace("\\", "/")
    for pattern in DANGEROUS_DIRS:
        if re.match(pattern, normalized):
            return True
    return False


# ============== 文件过滤 ==============

def should_ignore(path: str) -> bool:
    """检查是否应该忽略"""
    name = os.path.basename(path)

    for pattern in NEVER_TOUCH:
        if pattern.startswith("*"):
            if name.endswith(pattern[1:]):
                return True
        elif name == pattern or name.startswith(pattern):
            return True

    # 临时文件
    if name.startswith("~$"):
        return True

    return False


def should_organize(file_path: str, all_files: list) -> bool:
    """判断文件是否需要整理"""
    name = os.path.basename(file_path)
    name_no_ext = os.path.splitext(name)[0]

    # 1. 版本号文件
    if VERSION_PATTERN.search(name_no_ext):
        return True

    # 2. 批量复制特征
    if COPY_PATTERN.search(name_no_ext):
        return True

    # 3. 同前缀文件 >= 3 个
    prefix = get_prefix(name_no_ext)
    if prefix:
        same_prefix = [f for f in all_files if get_prefix(os.path.splitext(os.path.basename(f))[0]) == prefix]
        if len(same_prefix) >= 3:
            return True

    return False


def get_prefix(name: str) -> str:
    """提取文件名前缀"""
    # 去掉版本号后缀
    name = VERSION_PATTERN.sub('', name)
    name = COPY_PATTERN.sub('', name)

    # 按 - 或 _ 分割，取第一部分
    parts = re.split(r'[-_]', name)
    if parts:
        return parts[0]
    return name


# ============== 文件分类 ==============

def classify_by_name(file_path: str) -> tuple:
    """按文件名分类，返回 (group, new_name)"""
    name = os.path.basename(file_path)
    name_no_ext = os.path.splitext(name)[0]
    ext = os.path.splitext(name)[1]

    # 版本号
    match = VERSION_PATTERN.search(name_no_ext)
    if match:
        version = match.group(1)
        # 规范化版本号
        if '.' in version:
            folder = f"v{version}"
        else:
            folder = f"v{version}"

        # 新文件名：去掉版本号后缀
        new_name = VERSION_PATTERN.sub('', name_no_ext) + ext
        return (folder, new_name)

    return (None, name)


def classify_by_content(file_path: str) -> str:
    """按文件内容分类"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(5000)  # 只读前 5000 字符
    except:
        return None

    content_lower = content.lower()

    # PRD/需求文档
    if any(kw in content for kw in ["用户故事", "验收标准", "产品范围", "PRD", "需求文档"]):
        return "prd"

    # 技术文档
    if any(kw in content for kw in ["架构", "技术方案", "API", "接口设计", "数据流"]):
        return "tech"

    # 数据分析
    if any(kw in content for kw in ["数据分析", "统计", "分布", "样本", "清洗"]):
        return "research"

    # Prompt 文件
    if any(kw in content for kw in ["你是", "输出格式", "约束规则", "## 示例", "role: system"]):
        return "prompts"

    # Workflow
    if any(kw in content_lower for kw in ["workflow", "nodes:", "edges:", "graph:"]):
        return "workflows"

    return None


def classify_files(files: list, base_dir: str) -> dict:
    """
    分类所有文件
    返回: {target_folder: [(src_path, new_name), ...]}
    """
    result = defaultdict(list)
    unclassified = []

    for f in files:
        # 1. 按文件名分类
        folder, new_name = classify_by_name(f)
        if folder:
            result[folder].append((f, new_name))
            continue

        unclassified.append(f)

    # 2. 按内容分类（兜底）
    for f in unclassified:
        folder = classify_by_content(f)
        if folder:
            result[folder].append((f, os.path.basename(f)))
        else:
            # 无法分类，保持原位
            result["_unchanged"].append((f, os.path.basename(f)))

    return dict(result)


# ============== 执行整理 ==============

def organize_directory(target_dir: str, preview: bool = False) -> dict:
    """
    整理目录
    返回: {
        "moved": [(src, dst), ...],
        "created": [folder, ...],
        "skipped": [file, ...],
        "structure": str
    }
    """
    result = {
        "moved": [],
        "created": [],
        "skipped": [],
        "renamed": [],
        "structure": ""
    }

    # 1. 扫描文件
    all_files = []
    for root, dirs, files in os.walk(target_dir):
        # 跳过已有的版本目录和隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in NEVER_TOUCH and not re.match(r'^v\d', d)]

        for f in files:
            file_path = os.path.join(root, f)
            if not should_ignore(file_path):
                all_files.append(file_path)

    # 2. 过滤需要整理的文件
    to_organize = [f for f in all_files if should_organize(f, all_files)]
    result["skipped"] = [f for f in all_files if f not in to_organize]

    if not to_organize:
        return result

    # 3. 分类
    classified = classify_files(to_organize, target_dir)

    # 4. 执行移动
    for folder, files in classified.items():
        if folder == "_unchanged":
            continue

        target_folder = os.path.join(target_dir, folder)

        if not preview:
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
                result["created"].append(folder)
        else:
            if not os.path.exists(target_folder):
                result["created"].append(folder)

        for src_path, new_name in files:
            dst_path = os.path.join(target_folder, new_name)

            # 处理重名
            if os.path.exists(dst_path) and src_path != dst_path:
                base, ext = os.path.splitext(new_name)
                counter = 1
                while os.path.exists(dst_path):
                    new_name = f"{base}_{counter}{ext}"
                    dst_path = os.path.join(target_folder, new_name)
                    counter += 1

            if src_path != dst_path:
                if not preview:
                    shutil.move(src_path, dst_path)
                result["moved"].append((src_path, dst_path))

                if os.path.basename(src_path) != new_name:
                    result["renamed"].append((os.path.basename(src_path), new_name))

    return result


# ============== 生成 .repomap ==============

def generate_repomap(target_dir: str, result: dict) -> str:
    """生成 .repomap 文件"""

    # 构建目录树
    tree_lines = []

    def build_tree(path: str, prefix: str = "", is_last: bool = True):
        name = os.path.basename(path) or path
        connector = "└── " if is_last else "├── "

        # 检测是否是最新版本
        latest_marker = ""
        if re.match(r'^v\d', name):
            # 检查是否是同级最大版本
            parent = os.path.dirname(path)
            siblings = [d for d in os.listdir(parent) if os.path.isdir(os.path.join(parent, d)) and re.match(r'^v\d', d)]
            if siblings:
                versions = sorted(siblings, key=lambda x: [int(n) for n in re.findall(r'\d+', x)], reverse=True)
                if name == versions[0]:
                    latest_marker = "  # ← Latest"

        tree_lines.append(f"{prefix}{connector}{name}/{latest_marker}" if os.path.isdir(path) else f"{prefix}{connector}{name}")

        if os.path.isdir(path):
            children = sorted(os.listdir(path))
            children = [c for c in children if not c.startswith('.') and c not in NEVER_TOUCH]
            dirs = [c for c in children if os.path.isdir(os.path.join(path, c))]
            files = [c for c in children if not os.path.isdir(os.path.join(path, c))]

            all_children = dirs + files[:5]  # 只显示前 5 个文件
            if len(files) > 5:
                all_children.append(f"... ({len(files) - 5} more files)")

            for i, child in enumerate(all_children):
                is_last_child = (i == len(all_children) - 1)
                new_prefix = prefix + ("    " if is_last else "│   ")
                if isinstance(child, str) and child.startswith("..."):
                    tree_lines.append(f"{new_prefix}{'└── ' if is_last_child else '├── '}{child}")
                else:
                    build_tree(os.path.join(path, child), new_prefix, is_last_child)

    # 构建树
    root_name = os.path.basename(target_dir) or "root"
    tree_lines.append(f"{root_name}/")

    children = sorted(os.listdir(target_dir))
    children = [c for c in children if not c.startswith('.') and c not in NEVER_TOUCH]

    for i, child in enumerate(children):
        is_last = (i == len(children) - 1)
        build_tree(os.path.join(target_dir, child), "", is_last)

    tree_str = "\n".join(tree_lines)

    # 找最新版本
    latest_versions = find_latest_versions(target_dir)
    latest_table = "\n".join([f"| {name} | {path} |" for name, path in latest_versions])

    # 生成 .repomap
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")

    repomap = f'''# .repomap
<!--
  Repository structure map for AI assistants.
  Auto-generated by /org skill.

  AI Instructions:
  - Read this file FIRST when entering workspace
  - Use structure info to locate relevant files
  - Check "Latest" section for current working version
  - Respect "Do Not Modify" section
-->

## Meta

- Generated: {now}
- Directory: {target_dir}
- Tool: /org skill

## Structure

```
{tree_str}
```

## Latest (当前最新版本)

| 模块 | 路径 |
|-----|------|
{latest_table}

## Version Convention

- `v1/`, `v2/`, `v3/` - 主版本迭代
- `v1.1/`, `v1.2/` - 小版本调试迭代
- `← Latest` 标记当前使用版本

## Do Not Modify

- `.git/`
- `node_modules/`
- `.env*`
- `*.lock`

## Organization Summary

- Moved: {len(result["moved"])} files
- Created: {len(result["created"])} folders
- Renamed: {len(result["renamed"])} files
- Skipped: {len(result["skipped"])} files (not AI-generated)
'''

    # 写入文件
    repomap_path = os.path.join(target_dir, ".repomap")
    with open(repomap_path, 'w', encoding='utf-8') as f:
        f.write(repomap)

    return repomap_path


def find_latest_versions(target_dir: str) -> list:
    """找到所有最新版本目录"""
    latest = []

    for root, dirs, _ in os.walk(target_dir):
        version_dirs = [d for d in dirs if re.match(r'^v\d', d)]
        if version_dirs:
            # 排序找最新
            versions = sorted(version_dirs, key=lambda x: [int(n) for n in re.findall(r'\d+', x)], reverse=True)
            latest_dir = versions[0]
            rel_path = os.path.relpath(os.path.join(root, latest_dir), target_dir)
            parent_name = os.path.basename(root)
            latest.append((parent_name, rel_path))

    return latest


# ============== 主入口 ==============

def run_org(args: str, cwd: str, preview: bool = False):
    """
    运行 /org 命令

    args: 路径参数
    cwd: 当前工作目录
    preview: 是否预览模式
    """
    # 1. 解析路径
    target = resolve_path(args, cwd)

    if target is None:
        return {"error": "path_required", "message": "请指定要整理的目录"}

    if not os.path.isdir(target):
        return {"error": "not_found", "message": f"目录不存在: {args}"}

    # 2. 安全检查
    if args == "root":
        if is_dangerous_dir(cwd) and not is_project_dir(cwd):
            return {"error": "confirm_required", "message": f"当前在 {cwd}，不是项目目录。确认整理？"}

    # 3. 执行整理
    result = organize_directory(target, preview=preview)

    if preview:
        return {"preview": True, "result": result, "target": target}

    # 4. 生成 .repomap
    if result["moved"]:
        repomap_path = generate_repomap(target, result)
        result["repomap"] = repomap_path

    return {"success": True, "result": result, "target": target}


if __name__ == "__main__":
    import sys

    args = sys.argv[1] if len(sys.argv) > 1 else ""
    preview = "-p" in sys.argv

    if preview and args == "-p":
        args = sys.argv[2] if len(sys.argv) > 2 else ""

    cwd = os.getcwd()
    result = run_org(args, cwd, preview)

    print(result)
