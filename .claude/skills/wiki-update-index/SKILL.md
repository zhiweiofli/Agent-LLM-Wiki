---
name: wiki-update-index
description: Move raw-ingested files into structured index coverage.
---

# Wiki Indexing Skill

## Precondition

1. Search `wiki/0_Raw/inbox/` for files with `status: raw-ingested`.
2. If none exist, exit with: `No raw-ingested files to index`.

## Execution

For each eligible file:

1. Read its ingest analysis.
2. Classify using `config/taxonomy.yaml`.
3. If the source is duplicate, too tactical, or lacks reusable value, write a review note to `wiki/0_Raw/reviews/`.
4. Add or update an entry in `wiki/1_Index/master_index.md`:
   - topic name
   - one-line summary
   - source reference
   - tags or themes
5. Upgrade frontmatter:

```yaml
status: indexed
ingest_stage: indexed
```

## Postcondition

- processed files have `status: indexed`
- index entries link back to source files
- `wiki/log.md` has an `index` entry
