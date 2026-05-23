---
name: wiki-extract-concept
description: Extract evergreen concept cards from indexed sources and GitHub KB handoff tokens.
---

# Wiki Concept Extraction Skill

## Precondition

1. Search `github-kb/MEMORY.md` for `[待内化]`.
2. Search `wiki/0_Raw/inbox/`, `wiki/0_Raw/archive/`, and `wiki/1_Index/` for `status: indexed`.
3. If neither exists, exit with: `No material to conceptualize`.

## Execution

For each source:

1. Review the ingest/index analysis.
2. Check concept worthiness:
   - reusable beyond the original source
   - evergreen enough to matter later
   - relevant to one taxonomy dimension
   - not already covered by an existing card unless it can enrich it
3. Create or update `wiki/2_Concepts/<Concept_Name>.md`.
4. Use this structure:

```yaml
---
status: conceptualized
source: <origin file or section>
ingest_stage: conceptualized
---
```

Sections:

- `Core Insight`
- `Mechanism`
- `When To Use / When Not To Use`
- `Related Concepts`
- `Source Reference`

5. Cross-update related cards:
   - add backlinks
   - merge overlapping insights
   - mark contradictions clearly
6. Update `wiki/1_Index/master_index.md`.
7. Mark processed sources `status: extracted`.
8. Move processed inbox sources to `wiki/0_Raw/archive/<dimension>/<topic>/`.
9. Replace processed `[待内化]` with `[已内化]`.

## Postcondition

- concept cards exist and link back to sources
- processed sources are extracted and archived
- related cards are cross-linked
- `wiki/log.md` has an `extract-concept` entry
