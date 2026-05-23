---
name: github-kb
description: >
  Manage a local GitHub Knowledge Base using a filesystem-first approach.
  Use gh CLI to search repositories, issues, pull requests, and actions,
  then clone selected projects into a local KB directory.
  Maintain a human-readable catalog (INDEX.md) as the primary index.
  Treat the filesystem as long-term memory (RAG without vectors).
---

# GitHub Knowledge Base Skill

将 GitHub 转化为可搜索、可拥有的本地知识系统。

## When to Activate

当用户询问以下内容时触发：

- 查找 GitHub 仓库或替代方案
- 研究工具、框架或开源项目
- 检查 Issues 或 Pull Requests
- 追踪最近的 PR 变更或合并功能
- 克隆仓库到本地
- 查询本地知识库中的项目
- 将 GitHub 作为知识源进行搜索

## Core Workflow

### 1. DISCOVER (远程搜索)

使用 gh CLI 搜索 GitHub：

```bash
# 搜索仓库
gh search repos "<query>" --limit 10

# 搜索 Issues
gh search issues "<query>" --limit 20

# 查看 PR
gh pr list --repo <owner/repo>
gh pr view <number> --repo <owner/repo> --comments
```

**常用搜索限定符**：
- `language:<lang>` - 按语言过滤
- `stars:>n` - 按 star 数过滤
- `topic:<name>` - 按主题过滤
- `user:<owner>` - 按用户过滤
- `org:<org>` - 按组织过滤

### 2. ACQUIRE (本地获取)

克隆仓库到知识库：

```bash
git clone https://github.com/<owner>/<name>.git ./github-kb/repos/<name>
```

**命名规则**：
- 默认使用 `<name>` 作为目录名
- 冲突时使用 `<owner>__<name>`

### 3. RETRIEVE (深度检索)

使用本地工具检索：

- `Read` - 阅读 README、关键文件
- `Glob` - 发现目录结构
- `Grep` - 搜索 API、配置、关键词

### 4. CATALOG (索引维护)

更新 INDEX.md 索引：

```markdown
#### [owner/repo](https://github.com/owner/repo)

- GitHub: https://github.com/owner/repo
- Local: not cloned
- Category: <category>
- Status: LATER
- Why it matters: <one sentence>
- Notes: <one or two verified notes>
```

## Intent Routing

根据用户请求匹配意图：

| 意图 | 触发词 | 执行阶段 |
|------|--------|----------|
| 搜索仓库 | 找、搜、有没有、替代方案、对比 | DISCOVER |
| 搜索 Issues | 问题、bug、解决方案、讨论 | DISCOVER |
| 查看 PR | 最近更新、合并、PR、变更 | DISCOVER |
| 检查 CI | Actions、构建、工作流 | DISCOVER |
| 克隆仓库 | 克隆、下载、获取、添加到 KB | ACQUIRE |
| 查询本地 | 查看、分析、这个项目、怎么用 | RETRIEVE |
| 更新索引 | 更新 catalog、添加到知识库 | CATALOG |

## Output Format

每个 github-kb 任务应产出：

1. **远程发现**：链接、候选项、选择理由
2. **本地状态**：路径、文件、命令
3. **Catalog 更新**：INDEX.md / MEMORY.md 条目

## Philosophy

**低复杂度，高可控性**。

不依赖：
- 向量数据库
- 嵌入模型
- 自动摘要

依赖：
- 文件系统所有权
- 显式结构
- 人工策展摘要
- CLI 搜索

结果：持久、可移植、可检查的个人 GitHub 知识系统。
