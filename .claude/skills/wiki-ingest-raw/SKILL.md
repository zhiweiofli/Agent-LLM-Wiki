---
name: wiki-ingest-raw
description: Process files from wiki/0_Raw/inbox/ and prepare them for indexing.
---

# Wiki Raw Ingestion Skill

## Precondition

1. List files in `wiki/0_Raw/inbox/`.
2. If no files exist, exit with: `0_Raw/inbox has no files to process`.
3. Skip files that already have `status: raw-ingested` or higher.

## Execution

For each unprocessed file:

1. Produce a short analysis note:
   - core thesis
   - evidence quality
   - taxonomy classification guess from `config/taxonomy.yaml`
   - likely links to existing `wiki/2_Concepts/`
   - duplicate, stale, unsafe, or low-value risks
2. Parse the file:
   - Markdown: read directly
   - PDF/Image: use the Agent's native file or vision capabilities
3. If the source contains a live URL, perform semantic diff:
   - ignore cosmetic page changes
   - compare core claims, APIs, structure, and conclusions
   - if semantic difference is greater than 20%, pause and ask the user
   - if unreachable, add `decay: unreachable`
4. Add or update frontmatter:

```yaml
---
status: raw-ingested
source: <original URI or filename>
ingest_stage: analyzed
---
```

5. Preserve useful analysis under `## Ingest Analysis`.

## Postcondition

- processed files have `status: raw-ingested`
- stale or unreachable URLs are marked
- no file is silently skipped
- `wiki/log.md` has an `ingest` entry
