# Agent Context & Personal Knowledge Base Constitution

This repository is an Agent-driven personal knowledge base. The Agent operates as a curator, indexer, concept extractor, and maintenance worker for a local Markdown vault.

Before doing knowledge work, read:

1. `AGENTS.md` — operating rules and Skill routing
2. `USER.md` if present — private user profile and collaboration preferences
3. `config/taxonomy.yaml` if present, otherwise `config/taxonomy.example.yaml`
4. `wiki/1_Index/master_index.md`
5. `wiki/log.md` if present

## Directory Architecture

### Core Workflow: `wiki/`

- `wiki/0_Raw/inbox/`: the only manual input path for new sources
- `wiki/0_Raw/archive/`: processed source archive
- `wiki/0_Raw/attachments/`: binary files such as images and PDFs
- `wiki/0_Raw/queues/`: automation queues, such as GitHub URLs
- `wiki/0_Raw/reviews/`: dry-run reviews and batch review notes
- `wiki/1_Index/`: structured maps and master indices
- `wiki/2_Concepts/`: evergreen concept cards
- `wiki/3_Synthesis/`: reports, comparisons, decisions, and cross-concept analysis
- `wiki/4_Tools/`: scripts, queries, and runtime helpers

### Optional GitHub Feeder: `github-kb/`

- `github-kb/INDEX.md`: append-only repository index
- `github-kb/MEMORY.md`: reusable conclusions and gotchas
- `github-kb/repos/`: optional local clones; ask before cloning

## YAML State Machine

Every Markdown source file processed or moved by the Agent must contain frontmatter:

```yaml
---
status: raw-ingested | indexed | conceptualized | extracted
source: <original URI or local path>
---
```

State flow:

```text
inbox -> raw-ingested -> indexed -> extracted -> archive
                              \
                               -> conceptualized concept cards
```

Rules:

- source files eventually become `status: extracted`
- concept cards use `status: conceptualized`
- processed inbox files move to `wiki/0_Raw/archive/<dimension>/<topic>/`
- when moving a source, preserve `origin_path`, `archive_path`, and `archived_at`
- never delete original evidence unless the user explicitly asks

## Semantic Diff

When processing a source that contains a live URL:

1. Fetch the live URL if network access is available.
2. Ignore cosmetic layout changes.
3. Compare core claims, API behavior, structure, and conclusions.
4. If semantic difference is greater than 20%, pause and ask the user.
5. If unreachable, mark `decay: unreachable` and proceed from local content.

## Taxonomy

Use `config/taxonomy.yaml` as the canonical classification system. If missing, copy `config/taxonomy.example.yaml` to `config/taxonomy.yaml` and adapt it before serious use.

Classify by the source's core thesis, not surface keywords.

## Command Routing

| Trigger | Skill | Output |
|---|---|---|
| `/wiki-ingest-raw` or "process raw files" | `wiki-ingest-raw` | source files become `raw-ingested` |
| `/wiki-update-index` or "update index" | `wiki-update-index` | sources become `indexed`; master index updated |
| `/wiki-extract-concept` or "extract concepts" | `wiki-extract-concept` | concept cards created or updated |
| `/wiki-synthesize-report` or "generate report" | `wiki-synthesize-report` | report written to `wiki/3_Synthesis/` |
| `/wiki-lint` or "check wiki health" | `wiki-lint` | health findings and log entry |
| `/personal-kb-agent` or "search my KB" | `personal-kb-agent` | read-only context pack or graph insights |
| `/github-kb-indexer` or "process GitHub URLs" | `github-kb-indexer` | GitHub project index and memory updates |
| "run the full pipeline" | Pipeline | all applicable stages in order |

Full pipeline order:

```text
github-kb-indexer -> wiki-ingest-raw -> wiki-update-index -> wiki-extract-concept -> wiki-lint -> wiki-synthesize-report
```

Skip stages with no eligible input.

## Logging

After each Skill execution, append to `wiki/log.md`:

```markdown
## [YYYY-MM-DD] <operation> | <summary>
- Source: <source>
- Touched: <affected files>
```

## Output Principles

- verify before generalizing
- mark unknowns as `UNKNOWN`
- keep concepts evergreen and reusable
- use Mermaid diagrams when they clarify structure
- prefer concise synthesis over dumping raw retrieval output
