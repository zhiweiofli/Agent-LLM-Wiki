---
description: Update the knowledge base catalog (INDEX.md) with new or modified entries
---

# /update-catalog

更新知识库索引文件 INDEX.md。

## Usage

```
/update-catalog [repo-name]
```

## Examples

```
/update-catalog                    # 扫描所有仓库，更新整个 catalog
/update-catalog claude-code        # 只更新指定仓库的条目
```

## Workflow

1. 读取当前 INDEX.md
2. 扫描 `./github-kb/repos/` 目录
3. 对比现有条目和实际仓库
4. 生成新条目或更新现有条目
5. 保持分类结构

## Catalog Entry Format

```markdown
#### [owner/repo](https://github.com/owner/repo)

- GitHub: https://github.com/owner/repo
- Local: not cloned
- Category: <category>
- Status: LATER
- Why it matters: <one sentence>
- Notes: <one or two verified notes>
```

## Rules

- 保持条目简洁（1-3 行）
- 按类别组织
- 不写长篇说明
- 保持人类可读
