# GitHub Knowledge Base

A filesystem-first subsystem for researching GitHub repositories as durable local knowledge.

`github-kb` is optional. Use it when you want GitHub projects to feed your broader personal knowledge base without turning every repository into a full source card.

## What It Does

- search GitHub with `gh`
- record interesting repositories in `INDEX.md`
- optionally clone selected repositories into `repos/`
- write project-agnostic findings into `MEMORY.md`
- hand off reusable lessons to `wiki/2_Concepts/` through `[待内化]` tokens

## Quick Flow

```text
GitHub URL queue -> github-kb-indexer -> INDEX.md + MEMORY.md -> concept extraction
```

## Files

```text
github-kb/
├── CLAUDE.md
├── README.md
├── FOCUS.md
├── INDEX.md
├── MEMORY.md
├── docs/
│   └── ADR-001-architecture.md
├── repos/
└── .claude/
    ├── commands/
    ├── rules/
    └── skills/github-kb/
```

## Rules

- Keep GitHub URL as the primary identity.
- Record `GitHub:` and `Local:` for every entry.
- Ask before cloning repositories into `repos/`.
- Do not clone private repositories without explicit confirmation.
- End new reusable memory items with `[待内化]`.
- After concept extraction, replace `[待内化]` with `[已内化]`.

## Dependencies

- `git`
- `gh` CLI authenticated with `gh auth login`

## Privacy

Do not publish your real `INDEX.md`, `MEMORY.md`, `FOCUS.md`, or `repos/` directory if they contain private research directions, customer work, internal repositories, or personal strategy.
