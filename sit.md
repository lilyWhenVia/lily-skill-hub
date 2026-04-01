# 提交到 SIT 环境

将当前分支的改动提交并合并到 SIT 环境。

## 执行步骤

请按以下顺序执行：

### 1. 检查当前状态
- 运行 `git status` 查看当前分支和未提交的改动
- 运行 `git branch -r | grep "origin/F_" | sort -V | tail -1` 获取最新的 F 分支名称

### 2. 自动提交改动（如有未提交的改动）
- 运行 `git diff --staged` 和 `git diff` 查看所有改动
- 根据改动内容自动生成符合规范的 commit message：
  - 格式：`<type>(<scope>): <description>`
  - type: feat/fix/refactor/docs/style/test/chore
  - scope: 改动涉及的模块
  - description: 简洁描述改动内容
- 运行 `git add .` 暂存所有改动
- 运行 `git commit -m "<自动生成的commit message>"` 提交

### 3. 同步 F 分支最新代码
- 运行 `git fetch origin` 获取远程更新
- 运行 `git pull origin <最新F分支名> --no-edit` 从最新 F 分支拉取代码
- 如有冲突，提示用户解决后再继续

### 4. Push 当前分支
- 运行 `git push origin <当前分支名>` 推送当前分支

### 5. Merge 到 sit 分支
- 运行 `git checkout sit` 切换到 sit 分支
- 运行 `git pull origin sit` 拉取 sit 最新代码
- 运行 `git merge <原分支名> --no-edit` 合并原分支
- 运行 `git push origin sit` 推送 sit 分支
- 运行 `git checkout <原分支名>` 切回原分支

### 6. 完成报告
输出执行摘要：
- 提交的 commit message
- 合并的 F 分支版本
- 是否成功合并到 sit
