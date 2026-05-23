---
name: wiki-synthesize-report
description: Generate reports and cross-concept analysis from concept cards.
---

# Wiki Synthesis Skill

## Trigger Modes

- explicit report request
- user confirms conversational writeback
- periodic digest after enough concept changes

## Precondition

1. `wiki/2_Concepts/` contains at least one concept card.
2. A query, report request, or confirmed writeback exists.

## Execution

1. Retrieve relevant concept cards and index entries.
2. Analyze relationships, tensions, implications, and gaps.
3. Write the report to `wiki/3_Synthesis/` with frontmatter:

```yaml
---
type: periodic-digest | ad-hoc-report
query: <user query>
sources: [concept cards referenced]
date: <YYYY-MM-DD>
---
```

4. Use Mermaid diagrams and tables when they clarify the argument.
5. Do not cite concept cards that do not exist.

## Postcondition

- report exists in `wiki/3_Synthesis/`
- sources are valid
- `wiki/log.md` has a `synthesize` entry
