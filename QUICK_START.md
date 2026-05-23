# Quick Start

This guide gets your Personal Knowledge Base running in a local Agent environment, with Codex integration as the baseline example.

## 1. Dependencies

Required:

- `git`
- `python3` 3.9+
- an Agent that reads repository instructions from `AGENTS.md`

Recommended:

- Codex CLI or Codex desktop app
- Claude Code, if you want to use `.claude/skills/`
- `gh` CLI, if you want to use `github-kb`
- Obsidian, if you want to browse the Markdown vault visually

Optional:

- Mermaid-capable Markdown renderer

## 2. Environment Check

Run from the repository root:

```bash
git --version
python3 --version
find .agents/skills -maxdepth 2 -name SKILL.md | sort
test -f AGENTS.md
test -f wiki/1_Index/master_index.md
```

If you use GitHub KB:

```bash
gh --version
gh auth status
```

If `gh auth status` fails, authenticate:

```bash
gh auth login
```

## 3. Initialize Local Private Files

Create your private profile:

```bash
cp config/user_profile.example.md USER.md
```

Create your taxonomy:

```bash
cp config/taxonomy.example.yaml config/taxonomy.yaml
```

From this point on, treat the repository as your private working knowledge base if it contains real profile data or sources.

## 4. Codex Integration

Codex should automatically read `AGENTS.md` when working inside the repository. To verify integration:

1. Open this repository as the Codex workspace.
2. Ask Codex:

```text
Read AGENTS.md and summarize the wiki pipeline in 5 bullets.
```

3. Then ask:

```text
Use /personal-kb-agent to build a context pack for "agent workflow".
```

Expected behavior:

- Codex reads local instructions.
- It uses the `personal-kb-agent` Skill when relevant.
- It runs the local runtime script rather than inventing results.

Equivalent manual command:

```bash
python3 wiki/4_Tools/runtime/search/kb_context_pack.py "agent workflow" --top 3
```

## 5. Basic Test Flow

### Test 1: Context Pack

```bash
python3 wiki/4_Tools/runtime/search/kb_context_pack.py "agent workflow" --top 3
```

Expected output includes:

- `Example_Agent_Workflow_State_Machine`
- `Master Index`
- context assembly guidance

### Test 2: Graph Insights

```bash
python3 wiki/4_Tools/runtime/graph/kb_graph_insights.py
```

Expected output includes:

- node count
- dimension coverage
- hub or weak-node section

### Test 3: Syntax Check Without Cache Writes

Some sandboxes block Python bytecode cache writes. Use AST parsing instead of `py_compile`:

```bash
python3 -c "import ast, pathlib; [ast.parse(pathlib.Path(p).read_text()) for p in ['wiki/4_Tools/runtime/search/kb_context_pack.py','wiki/4_Tools/runtime/graph/kb_graph_insights.py']]; print('syntax ok')"
```

Expected output:

```text
syntax ok
```

## 6. First Real Ingest

Add a small Markdown source:

```bash
cat > wiki/0_Raw/inbox/example-source.md <<'EOF'
---
source: local-example
---

# Example Source

Agent-maintained knowledge bases need explicit processing states to avoid duplicate work.
EOF
```

Then ask your Agent:

```text
/wiki-ingest-raw
```

Continue with:

```text
/wiki-update-index
/wiki-extract-concept
```

If the test source contains real material, keep the repository private or remove the file before sharing a clean copy.

## 7. GitHub KB Smoke Test

Add a public repository URL:

```text
https://github.com/owner/repo
```

to:

```text
wiki/0_Raw/queues/github-repos.md
```

Then ask:

```text
/github-kb-indexer
```

Expected behavior:

- Agent verifies the URL.
- Agent records `GitHub:` and `Local: not cloned`.
- Agent asks before cloning.
- Agent appends reusable findings to `github-kb/MEMORY.md` with `[待内化]`.

## 8. Sharing Checklist

If you later create a public or shared copy, check:

```bash
find . -maxdepth 4 -type f | sort
rg -n "secret|token|password|private|customer|internal|YOUR_NAME|USER.md" .
```

Also inspect:

- `wiki/0_Raw/`
- `wiki/2_Concepts/`
- `wiki/3_Synthesis/`
- `github-kb/INDEX.md`
- `github-kb/MEMORY.md`
- `github-kb/FOCUS.md`
- `github-kb/repos/`

Shared copies should contain only examples, placeholders, and generic operating rules.
