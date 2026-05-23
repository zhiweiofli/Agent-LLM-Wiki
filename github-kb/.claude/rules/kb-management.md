# Knowledge Base Management Rules

知识库管理的核心规则和约束。

## Directory Structure

```
github-kb/
├── INDEX.md           # Repo catalog
├── MEMORY.md          # Reusable findings
├── FOCUS.md           # Short-term review board
├── repos/             # 克隆的仓库
│   ├── project-a/
│   ├── project-b/
│   └── ...
└── .claude/           # Claude Code 配置
```

## Core Rules

### 1. 单一真相源

INDEX.md 是 repo catalog 的主索引；MEMORY.md 是可内化结论的沉淀区。

### 2. 显式优于隐式

- 每个仓库必须有 INDEX 条目
- 不依赖自动发现
- 人工策展优于自动生成

### 3. 克隆规范

| 场景 | 目录名 |
|------|--------|
| 默认 | `<repo-name>` |
| 名称冲突 | `<owner>__<repo-name>` |
| 私有仓库 | 需显式授权 |

### 4. 检索优先级

1. 先查 INDEX.md 确认仓库存在
2. 再进入仓库目录检索
3. 使用 Read/Glob/Grep 工具

### 5. 更新纪律

- 克隆后立即更新 INDEX.md
- 删除后立即更新 Local 字段或移除条目
- 保持 INDEX 与文件系统同步

## Prohibited Actions

- ❌ 批量爬取或自动克隆
- ❌ 未经确认访问私有仓库
- ❌ 在 INDEX 中编造不存在的项目
- ❌ 跳过 INDEX 更新步骤

## Quality Checks

每次操作后验证：

- [ ] 仓库目录存在且完整
- [ ] INDEX 条目链接有效
- [ ] 描述准确反映项目功能
