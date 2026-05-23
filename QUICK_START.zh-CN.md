# 快速开始

这份指南用于把你的 Personal Knowledge Base 在本地 Agent 环境中跑起来。这里以 Codex 集成为基准示例，同时兼容 Claude Code 的 `.claude/skills/` 入口。

## 1. 依赖

必需：

- `git`
- `python3` 3.9+
- 一个能读取仓库 `AGENTS.md` 的 Agent 环境

推荐：

- Codex CLI 或 Codex 桌面版
- Claude Code，如果你希望使用 `.claude/skills/`
- `gh` CLI，如果你希望使用 `github-kb`
- Obsidian，如果你希望用图形化方式浏览 Markdown vault

可选：

- 支持 Mermaid 的 Markdown 渲染器

## 2. 环境检查

在仓库根目录执行：

```bash
git --version
python3 --version
find .agents/skills -maxdepth 2 -name SKILL.md | sort
test -f AGENTS.md
test -f wiki/1_Index/master_index.md
```

如果要使用 GitHub KB：

```bash
gh --version
gh auth status
```

如果 `gh auth status` 失败，先登录：

```bash
gh auth login
```

## 3. 初始化本地私有配置

创建你的私人用户画像：

```bash
cp config/user_profile.example.md USER.md
```

创建你的分类体系：

```bash
cp config/taxonomy.example.yaml config/taxonomy.yaml
```

从这一步开始，只要你填入了真实画像或资料，就应把这个仓库当作私人工作知识库处理。

## 4. Codex 集成

Codex 在仓库内工作时，应自动读取 `AGENTS.md`。可以这样验证：

1. 在 Codex 中打开这个仓库。
2. 对 Codex 说：

```text
Read AGENTS.md and summarize the wiki pipeline in 5 bullets.
```

3. 再说：

```text
Use /personal-kb-agent to build a context pack for "agent workflow".
```

预期行为：

- Codex 会读取本地仓库指令。
- 当问题匹配时，会使用 `personal-kb-agent` Skill。
- 会运行本地 runtime 脚本，而不是凭空编造结果。

等价的手动命令：

```bash
python3 wiki/4_Tools/runtime/search/kb_context_pack.py "agent workflow" --top 3
```

## 5. 基础测试流程

### 测试 1：Context Pack

```bash
python3 wiki/4_Tools/runtime/search/kb_context_pack.py "agent workflow" --top 3
```

预期输出包含：

- `Example_Agent_Workflow_State_Machine`
- `Master Index`
- context assembly guidance

### 测试 2：知识图谱检查

```bash
python3 wiki/4_Tools/runtime/graph/kb_graph_insights.py
```

预期输出包含：

- 节点数量
- 维度覆盖情况
- hub 或 weak-node 相关章节

### 测试 3：不写缓存的语法检查

有些沙箱会禁止 Python 写入 bytecode cache。可以用 AST 解析代替 `py_compile`：

```bash
python3 -c "import ast, pathlib; [ast.parse(pathlib.Path(p).read_text()) for p in ['wiki/4_Tools/runtime/search/kb_context_pack.py','wiki/4_Tools/runtime/graph/kb_graph_insights.py']]; print('syntax ok')"
```

预期输出：

```text
syntax ok
```

## 6. 第一次真实摄入

添加一个小的 Markdown 源文件：

```bash
cat > wiki/0_Raw/inbox/example-source.md <<'EOF'
---
source: local-example
---

# Example Source

Agent-maintained knowledge bases need explicit processing states to avoid duplicate work.
EOF
```

然后让 Agent 执行：

```text
/wiki-ingest-raw
```

继续执行：

```text
/wiki-update-index
/wiki-extract-concept
```

如果测试文件中包含真实资料，请保持仓库私有；若要分享干净副本，先删除这些内容。

## 7. GitHub KB 冒烟测试

把一个公开仓库 URL 加入：

```text
wiki/0_Raw/queues/github-repos.md
```

例如：

```text
https://github.com/owner/repo
```

然后让 Agent 执行：

```text
/github-kb-indexer
```

预期行为：

- Agent 验证 URL 是否为合法 GitHub 仓库。
- Agent 记录 `GitHub:` 和 `Local: not cloned`。
- 如需 clone，Agent 会先询问确认。
- Agent 将可复用结论追加到 `github-kb/MEMORY.md`，并以 `[待内化]` 结尾。

## 8. 分享前检查

如果未来要创建公开或共享副本，建议执行：

```bash
find . -maxdepth 4 -type f | sort
rg -n "secret|token|password|private|customer|internal|YOUR_NAME|USER.md" .
```

重点人工检查：

- `wiki/0_Raw/`
- `wiki/2_Concepts/`
- `wiki/3_Synthesis/`
- `github-kb/INDEX.md`
- `github-kb/MEMORY.md`
- `github-kb/FOCUS.md`
- `github-kb/repos/`

共享副本里应只包含示例、占位符和通用操作规则。
