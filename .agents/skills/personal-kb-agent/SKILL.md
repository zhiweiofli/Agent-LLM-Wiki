---
name: personal-kb-agent
description: Read-only local access to context packs and graph insights from the current vault.
---

# Personal KB Agent Skill

## Commands

### Context Pack

Use when the user asks to search the knowledge base or assemble context.

```bash
python3 wiki/4_Tools/runtime/search/kb_context_pack.py "<query>" --top 8
```

Return the useful parts: retrieved pages, concept cards, synthesis reports, gaps, and suggested next reads.

### Graph Insights

Use when the user asks about graph health, bridge nodes, orphan concepts, or coverage.

```bash
python3 wiki/4_Tools/runtime/graph/kb_graph_insights.py
```

## Safety

- read-only by default
- do not write concept cards from this Skill
- mark unsupported claims as `UNKNOWN`
- ask before saving reusable conversational insights
