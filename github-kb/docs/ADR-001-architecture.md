# ADR-001: GitHub Knowledge Base Architecture

**Status**: Accepted

## Context

GitHub repositories often contain practical knowledge that is hard to preserve through browser bookmarks alone. A local GitHub KB gives the Agent a durable place to index repositories, inspect code, and turn reusable findings into concept cards.

## Decision

Use a filesystem-first subsystem:

- `INDEX.md` for repository catalog entries
- `MEMORY.md` for project-agnostic findings
- `FOCUS.md` for short-term research priorities
- `repos/` for optional local clones
- `.claude/` for Claude Code commands, rules, and Skill definitions

## Workflow

```text
1. DISCOVER
   gh search repos/issues/prs

2. ACQUIRE
   optional git clone into github-kb/repos/

3. RETRIEVE
   read / glob / grep local files

4. INDEX
   update INDEX.md and MEMORY.md

5. HANDOFF
   mark reusable findings with [待内化]
```

## Non-Goals

- no mass crawling
- no automatic private repository access
- no vector database requirement
- no unverified summaries

## Consequences

Positive:

- portable
- inspectable
- easy to version
- works with standard CLI tools

Tradeoffs:

- requires manual curation
- large repositories can take disk space
- `gh` authentication is required for richer search
