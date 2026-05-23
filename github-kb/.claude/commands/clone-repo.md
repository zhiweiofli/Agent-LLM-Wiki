---
description: Clone a GitHub repository into the local knowledge base
---

# /clone-repo

克隆 GitHub 仓库到本地知识库。

## Usage

```
/clone-repo <github-url-or-owner/repo>
```

## Examples

```
/clone-repo anthropics/claude-code
/clone-repo https://github.com/anthropics/claude-code
```

## Workflow

1. 解析仓库地址，提取 owner/name
2. 检查本地是否已存在
3. 执行 `git clone` 到 `./github-kb/repos/<name>`
4. 阅读 README，理解项目
5. 生成 INDEX.md 条目
6. 更新 INDEX.md / MEMORY.md

## Output

- 确认克隆位置
- 项目简要摘要
- INDEX 条目预览
