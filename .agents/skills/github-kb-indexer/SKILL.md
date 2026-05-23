---
name: github-kb-indexer
description: Consume GitHub repository URLs from the queue and append project-agnostic findings.
---

# GitHub KB Indexer Skill

## Precondition

`wiki/0_Raw/queues/github-repos.md` contains unprocessed GitHub repository URLs.

## Execution

For each URL:

1. Verify it is a canonical GitHub repository URL.
2. Use metadata first; ask before cloning into `github-kb/repos/`.
3. Append an entry to `github-kb/INDEX.md`.
4. Record:
   - `GitHub: https://github.com/<owner>/<repo>`
   - `Local: not cloned` or `Local: github-kb/repos/<repo>`
5. Append reusable, project-agnostic findings to `github-kb/MEMORY.md`.
6. End each new memory item with `[待内化]`.
7. Remove processed URLs from the queue.

## Postcondition

- queue is clean
- index entries include `GitHub:` and `Local:`
- memory entries include `[待内化]`
- `wiki/log.md` has a `github-kb-indexer` entry
