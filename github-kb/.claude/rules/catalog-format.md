# Catalog Format Rules

知识库索引文件 (INDEX.md) 的格式规范。

## Structure

```markdown
# GitHub Knowledge Base

简短描述本知识库的用途和范围。

---

## Category Name

#### [owner/repo](https://github.com/owner/repo)

- GitHub: https://github.com/owner/repo
- Local: not cloned
- Category: <category>
- Status: LATER
- Why it matters: <one sentence>
- Notes: <one or two verified notes>
```

## Rules

### 1. 分类组织

- 按领域/用途分类，不按语言或技术
- 分类名称简洁明确
- 相关项目放在同一分类下

### 2. 条目格式

每个条目必须包含：

| 元素 | 要求 |
|------|------|
| 标题链接 | `#### [owner/repo](https://github.com/owner/repo)` |
| GitHub | canonical GitHub URL |
| Local | `not cloned` or `github-kb/repos/<name>` |
| Why / Notes | verified, concise notes |

### 3. 内容规范

**DO**:
- 保持简洁，便于扫描
- 使用一致的描述风格
- 以 GitHub URL 作为主身份
- 明确记录本地是否 clone

**DON'T**:
- 写长篇介绍
- 复制 README 内容
- 编造未验证功能

### 4. 更新规则

- 新仓库克隆后必须添加条目
- 删除仓库后必须移除条目
- 定期检查链接有效性

## Example

```markdown
## AI & LLM Tools

### Category: agent-framework

#### [owner/example-agent](https://github.com/owner/example-agent)

- GitHub: https://github.com/owner/example-agent
- Local: not cloned
- Category: agent-framework
- Status: LATER
- Why it matters: Example placeholder.
- Notes: Replace with verified notes.
```
