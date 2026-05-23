---
name: wiki-lint
description: Check knowledge base health, stale claims, orphan concepts, and missing links.
---

# Wiki Lint Skill

## Precondition

`wiki/2_Concepts/` contains at least two concept cards.

## Checks

- orphan concept cards
- one-way links that should be reciprocal
- contradictions between concept cards
- stale URL-backed claims
- concepts missing from `wiki/1_Index/master_index.md`
- taxonomy dimensions with sparse coverage
- GitHub KB handoff tokens not yet internalized

## Output

Return a concise health report with severity, file references, and suggested fixes.

Append a `lint` entry to `wiki/log.md`.
