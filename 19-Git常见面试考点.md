# Git 常见面试考点

> 适用于测试开发 / 自动化测试 / 后端测试岗位面试准备

---

## 一、Git 基础概念（必会）

### Git 是什么？

> Git 是一个**分布式版本控制系统**，每个开发者本地都有完整的代码仓库，不依赖中心服务器。

### Git vs SVN

| 对比项 | Git | SVN |
|--------|-----|-----|
| 架构 | **分布式** | 集中式 |
| 离线操作 | ✅ 支持（本地有完整仓库） | ❌ 不支持 |
| 分支 | 轻量快速 | 重量级（复制目录） |
| 速度 | 快 | 较慢 |
| 常见平台 | GitHub / GitLab / Gitee | SVN Server |

### 三个区域（核心概念）

```
工作区（Working Directory）    暂存区（Staging Area）    本地仓库（Repository）
        |                            |                          |
        |--- git add --------------->|                          |
        |                            |--- git commit ---------->|
        |                            |                          |--- git push ---> 远程仓库
        |<-------------------------- git checkout / restore ----|
```

> **口诀**：工作区写代码 → `add` 到暂存区 → `commit` 到本地仓库 → `push` 到远程仓库

---

## 二、常用命令（每个都要会）

### 初始化与克隆

```bash
git init                          # 初始化本地仓库
git clone <url>                   # 克隆远程仓库
```

### 日常操作

```bash
git status                        # 查看当前状态（最常用）
git add <file>                    # 添加文件到暂存区
git add .                         # 添加所有修改到暂存区
git commit -m "提交信息"           # 提交到本地仓库
git push origin main              # 推送到远程
git pull origin main              # 拉取远程最新代码（= fetch + merge）
```

### 查看信息

```bash
git log                           # 查看提交历史
git log --oneline                 # 简洁一行显示
git log --oneline --graph         # 图形化显示分支
git diff                          # 查看工作区与暂存区的差异
git diff --cached                 # 查看暂存区与本地仓库的差异
git show <commit_id>              # 查看某次提交的详细内容
```

### 撤销操作

```bash
git checkout -- <file>            # 撤销工作区的修改（恢复到暂存区/仓库版本）
git restore <file>                # 同上（新版推荐写法）

git reset HEAD <file>             # 取消暂存（从暂存区移回工作区）
git restore --staged <file>       # 同上（新版推荐写法）

git reset --soft HEAD~1           # 撤销上一次 commit，保留修改在暂存区
git reset --mixed HEAD~1          # 撤销上一次 commit，保留修改在工作区（默认）
git reset --hard HEAD~1           # 撤销上一次 commit，修改全部丢弃（慎用！）
```

### reset 三种模式对比（常考）

| 模式 | 本地仓库 | 暂存区 | 工作区 | 适用场景 |
|------|---------|--------|--------|---------|
| `--soft` | ✅ 回退 | 保留 | 保留 | 想重新写 commit 信息 |
| `--mixed` | ✅ 回退 | ✅ 清空 | 保留 | 想重新选择要提交的文件 |
| `--hard` | ✅ 回退 | ✅ 清空 | ✅ 清空 | 彻底丢弃（**危险**） |

---

## 三、分支操作（高频必考）

### 基本命令

```bash
git branch                        # 查看本地分支
git branch -a                     # 查看所有分支（含远程）
git branch <name>                 # 创建分支
git checkout <name>               # 切换分支
git checkout -b <name>            # 创建并切换（常用）
git switch <name>                 # 切换分支（新版推荐）
git switch -c <name>              # 创建并切换（新版推荐）
git branch -d <name>              # 删除已合并的分支
git branch -D <name>              # 强制删除分支
git push origin --delete <name>   # 删除远程分支
```

### 合并分支

```bash
# 方式一：merge（推荐）
git checkout main
git merge feature-branch          # 将 feature 合并到 main

# 方式二：rebase（变基）
git checkout feature-branch
git rebase main                   # 将 feature 的提交"移"到 main 最新提交之后
```

### merge vs rebase（必考）

| 对比项 | merge | rebase |
|--------|-------|--------|
| 历史记录 | 保留完整历史，有合并节点 | 线性历史，更整洁 |
| 安全性 | **安全**（不改变历史） | 有风险（重写历史） |
| 适用场景 | 合并到主分支 | 整理个人分支提交 |
| 冲突处理 | 一次性解决 | 可能逐个 commit 解决 |

> **面试一句话**：merge 安全保留历史，rebase 整洁但别在公共分支上用

### 分支策略（Git Flow）

```
main（主分支）           → 生产环境代码，稳定
  └── develop（开发分支） → 日常开发集成
       └── feature/*     → 功能分支（从 develop 创建）
       └── release/*     → 发版分支（从 develop 创建）
  └── hotfix/*           → 紧急修复（从 main 创建）
```

---

## 四、冲突解决（高频场景题）

### 什么时候会冲突？

> 两个人修改了**同一文件的同一行**，Git 无法自动合并时就会产生冲突。

### 冲突标记

```
<<<<<<< HEAD
你的修改内容
=======
别人的修改内容
>>>>>>> feature-branch
```

### 解决步骤

```bash
1. git pull / git merge → 发现冲突
2. 打开冲突文件，手动选择保留哪部分
3. 删除冲突标记（<<<<<<< ======= >>>>>>>）
4. git add <file>
5. git commit -m "resolve conflict"
```

> **面试回答模板**：先 pull 拉取最新代码 → 如果冲突，手动编辑文件解决 → add + commit → push

---

## 五、其他高频命令

### stash 暂存

```bash
git stash                         # 暂存当前工作区的修改
git stash list                    # 查看暂存列表
git stash pop                     # 恢复最近一次暂存并删除记录
git stash apply                   # 恢复最近一次暂存但不删除记录
git stash drop                    # 删除最近一次暂存记录
```

> **使用场景**：正在开发 feature A，突然要切到 hotfix 分支修 bug → 先 stash 保存 → 切分支修 bug → 切回来 stash pop 恢复

### cherry-pick 摘取提交

```bash
git cherry-pick <commit_id>       # 把某个 commit 复制到当前分支
```

> **使用场景**：只需要某个分支的某一个 commit，不想合并整个分支

### revert 安全回退

```bash
git revert <commit_id>            # 创建一个新提交来撤销指定 commit
```

### reset vs revert（必考）

| 对比项 | reset | revert |
|--------|-------|--------|
| 原理 | **移动 HEAD 指针**，丢弃提交 | **创建新提交**来撤销 |
| 历史 | 改写历史 | 保留历史 |
| 安全性 | 危险（已推送的不能用） | **安全**（可用于已推送的） |
| 适用 | 本地未推送的提交 | 已推送到远程的提交 |

> **口诀**：没 push 用 reset，已 push 用 revert

### tag 标签

```bash
git tag v1.0.0                    # 创建轻量标签
git tag -a v1.0.0 -m "版本1.0"    # 创建附注标签
git push origin v1.0.0            # 推送标签到远程
git tag                           # 查看所有标签
```

---

## 六、.gitignore 文件

```bash
# 忽略规则示例
*.log              # 忽略所有 .log 文件
node_modules/      # 忽略 node_modules 目录
.env               # 忽略环境变量文件
__pycache__/       # 忽略 Python 缓存
*.pyc              # 忽略编译文件
.idea/             # 忽略 IDE 配置
dist/              # 忽略构建产物
```

> **面试常问**：已经被 Git 追踪的文件加入 .gitignore 不会生效，需要先 `git rm --cached <file>` 取消追踪

---

## 七、常见面试题及参考答案

### Q1：git fetch 和 git pull 的区别？

> `git fetch` 只拉取远程代码到本地仓库，不自动合并；`git pull` = `git fetch` + `git merge`，会自动合并。建议先 fetch 再手动 merge 更安全。

### Q2：git merge 和 git rebase 的区别？

> merge 保留完整分支历史（有合并节点），rebase 让历史变成线性更整洁。不要在公共分支上 rebase。

### Q3：git reset 和 git revert 的区别？

> reset 移动 HEAD 丢弃提交（改写历史），适合本地；revert 创建新提交来撤销（保留历史），适合已推送的。

### Q4：如何解决 Git 冲突？

> pull 时发现冲突 → 打开冲突文件 → 手动编辑选择保留内容 → 删除冲突标记 → add + commit。

### Q5：git stash 的使用场景？

> 当前工作未完成但需要切换分支时，用 `git stash` 暂存修改，处理完切回来用 `git stash pop` 恢复。

### Q6：如何回退到上一个版本？

> 本地未推送：`git reset --hard HEAD~1`；已推送到远程：`git revert HEAD`。

### Q7：git reset 的三种模式？
11111

> --soft 保留暂存区和工作区；--mixed（默认）清空暂存区保留工作区；--hard 全部清空（慎用）。

### Q8：什么是 Git Flow？

> 一种分支管理策略：main（生产）+ develop（开发）+ feature（功能）+ release（发版）+ hotfix（热修复）。

---

## 速记口诀

```
三区：工作区 → add → 暂存区 → commit → 本地仓库 → push → 远程

日常四连：status 看状态 → add 加暂存 → commit 提交 → push 推送
拉取代码：pull = fetch + merge

分支：checkout -b 创建切换，merge 合并，-d 删除
merge 安全保留历史，rebase 线性但别用在公共分支

冲突：手动编辑 → 删标记 → add → commit

reset soft 留暂存，mixed 留工作区，hard 全丢（慎用）
没 push 用 reset，已 push 用 revert

stash 临时保存，pop 恢复
cherry-pick 摘取单个 commit
tag 标签标记版本号
```

---

*可与《05-CI_CD常见面试题.md》搭配复习，Git 是 CI/CD 的基础，也是团队协作的核心工具。*
