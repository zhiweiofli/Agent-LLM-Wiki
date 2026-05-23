---
description: Search GitHub for repositories, issues, or pull requests using gh CLI
---

# /search-github

搜索 GitHub 仓库、Issues 或 Pull Requests。

## Usage

```
/search-github <query>
```

## Examples

```
/search-github chatbot framework python
/search-github topic:mcp stars:>100
/search-github "memory leak" repo:anthropics/claude-code
```

## Workflow

1. 解析用户查询，识别搜索类型（repos/issues/prs）
2. 构建 gh CLI 命令
3. 执行搜索并格式化结果
4. 询问用户是否需要克隆感兴趣的仓库

## Output

返回格式化的搜索结果列表，包含：
- 仓库名称和链接
- 描述
- Stars / Forks / 语言
- 最近更新时间
