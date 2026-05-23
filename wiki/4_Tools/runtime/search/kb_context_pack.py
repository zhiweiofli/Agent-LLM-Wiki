#!/usr/bin/env python3
"""
Build a compact context pack from the local Agent-driven knowledge vault.

Phase-1 prototype:
- no external dependencies
- searches USER.md when present, master_index.md, concept cards, synthesis reports, github-kb
- ranks by query tokens, title hits, dimension hints, and wikilink overlap
- emits Markdown suitable for a general Agent prompt
"""

from __future__ import annotations

import argparse
import os
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CONCEPTS = ROOT / "wiki" / "2_Concepts"
SYNTHESIS = ROOT / "wiki" / "3_Synthesis"
MASTER_INDEX = ROOT / "wiki" / "1_Index" / "master_index.md"
USER = ROOT / "USER.md"
GITHUB_INDEX = ROOT / "github-kb" / "INDEX.md"
GITHUB_MEMORY = ROOT / "github-kb" / "MEMORY.md"


STOP_WORDS = {
    "the", "and", "for", "with", "this", "that", "from", "into", "how", "what",
    "为什么", "怎么", "如何", "这个", "那个", "以及", "一个", "当前", "我的",
}

DIMENSION_HINTS = {
    "AI Engineering": ["agent", "llm", "mcp", "harness", "skill", "workflow", "automation", "model", "tool"],
    "Knowledge Systems": ["wiki", "pkm", "obsidian", "knowledge", "learning", "thinking", "decision", "second brain"],
    "Product & Business": ["product", "business", "side project", "pmf", "growth", "pricing", "startup", "monetization"],
    "Distribution & Brand": ["content", "distribution", "brand", "writing", "audience", "publishing"],
    "Finance & Investing": ["finance", "investing", "macro", "valuation", "portfolio", "risk", "cash flow"],
}


@dataclass
class Page:
    path: Path
    rel: str
    kind: str
    title: str
    body: str
    links: list[str]
    dimension: str = "UNKNOWN"


@dataclass
class ScoredPage:
    page: Page
    score: float
    reasons: list[str]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")
    except FileNotFoundError:
        return ""


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4 :].lstrip()
    return text


def extract_title(path: Path, text: str) -> str:
    fm_title = re.search(r"^title:\s*[\"']?(.+?)[\"']?\s*$", text, re.M)
    if fm_title:
        return fm_title.group(1).strip()
    heading = re.search(r"^#\s+(.+)$", text, re.M)
    if heading:
        return heading.group(1).strip()
    return path.stem


def extract_links(text: str) -> list[str]:
    return sorted(set(m.group(1).split("|", 1)[0].strip() for m in re.finditer(r"\[\[([^\]]+)\]\]", text)))


def tokenize(query: str) -> list[str]:
    lowered = query.lower()
    raw = re.split(r"[\s,，。！？、；：:()（）\[\]{}<>\"'`/\\|]+", lowered)
    tokens: list[str] = []
    for token in raw:
        token = token.strip("-_.")
        if len(token) > 1 and token not in STOP_WORDS:
            tokens.append(token)
        if re.search(r"[\u4e00-\u9fff]", token):
            chars = [c for c in token if re.match(r"[\u4e00-\u9fff]", c)]
            tokens.extend("".join(chars[i : i + 2]) for i in range(max(0, len(chars) - 1)))
            tokens.extend("".join(chars[i : i + 3]) for i in range(max(0, len(chars) - 2)))
    return sorted(set(t for t in tokens if t and t not in STOP_WORDS))


def infer_dimensions(query: str) -> list[str]:
    q = query.lower()
    hits: list[tuple[int, str]] = []
    for dim, hints in DIMENSION_HINTS.items():
        score = sum(1 for hint in hints if hint.lower() in q)
        if score:
            hits.append((score, dim))
    return [dim for _, dim in sorted(hits, reverse=True)]


def parse_master_dimensions() -> dict[str, str]:
    text = read_text(MASTER_INDEX)
    markers = {
        "AI Engineering": "## AI Engineering",
        "Knowledge Systems": "## Knowledge Systems",
        "Product & Business": "## Product & Business",
        "Distribution & Brand": "## Distribution & Brand",
        "Finance & Investing": "## Finance & Investing",
    }
    current = "UNKNOWN"
    dimensions: dict[str, str] = {}
    for line in text.splitlines():
        for dim, marker in markers.items():
            if line.startswith(marker):
                current = dim
        for target in re.findall(r"\[\[([^\]]+)\]\]", line):
            dimensions[Path(target.split("|", 1)[0]).stem] = current
    return dimensions


def collect_pages() -> list[Page]:
    pages: list[Page] = []
    dim_map = parse_master_dimensions()
    for root, kind in [(CONCEPTS, "concept"), (SYNTHESIS, "synthesis")]:
        if not root.exists():
            continue
        for path in sorted(root.glob("*.md")):
            text = read_text(path)
            pages.append(
                Page(
                    path=path,
                    rel=str(path.relative_to(ROOT)),
                    kind=kind,
                    title=extract_title(path, text),
                    body=strip_frontmatter(text),
                    links=extract_links(text),
                    dimension=dim_map.get(path.stem, "Synthesis" if kind == "synthesis" else "UNKNOWN"),
                )
            )
    for path, kind in [(MASTER_INDEX, "index"), (GITHUB_INDEX, "github-index"), (GITHUB_MEMORY, "github-memory")]:
        if path.exists():
            text = read_text(path)
            pages.append(
                Page(
                    path=path,
                    rel=str(path.relative_to(ROOT)),
                    kind=kind,
                    title=extract_title(path, text),
                    body=strip_frontmatter(text),
                    links=extract_links(text),
                    dimension="Index" if kind == "index" else "GitHub",
                )
            )
    return pages


def score_page(page: Page, tokens: list[str], dimensions: list[str]) -> ScoredPage:
    haystack = f"{page.title}\n{page.body}".lower()
    title = page.title.lower()
    score = 0.0
    reasons: list[str] = []

    for token in tokens:
        count = haystack.count(token)
        if count:
            token_score = min(count, 8) * 1.0
            if token in title:
                token_score += 5.0
                reasons.append(f"title:{token}")
            score += token_score

    for dim in dimensions:
        if page.dimension == dim:
            score += 10.0
            reasons.append(f"dimension-match:{dim}")
        if dim in page.body or dim in page.title:
            score += 4.0
            reasons.append(f"dimension:{dim}")

    if page.kind == "concept":
        score *= 1.25
    elif page.kind == "synthesis":
        score *= 1.1

    if page.links:
        score += min(len(page.links), 8) * 0.15

    return ScoredPage(page=page, score=score, reasons=reasons[:5])


def excerpt(text: str, tokens: list[str], limit: int = 420) -> str:
    clean = re.sub(r"\n{3,}", "\n\n", text.strip())
    lower = clean.lower()
    positions = [lower.find(t) for t in tokens if lower.find(t) >= 0]
    if positions:
        start = max(0, min(positions) - 120)
    else:
        start = 0
    snippet = clean[start : start + limit].strip()
    return re.sub(r"\s+", " ", snippet)


def user_profile_summary() -> str:
    text = read_text(USER)
    if not text:
        return "- USER.md not found"
    wanted = []
    capture = False
    for line in text.splitlines():
        if line.startswith("## 当前阶段") or line.startswith("## 高关注主题") or line.startswith("## 协作期望"):
            capture = True
            wanted.append(line)
            continue
        if capture and line.startswith("## "):
            capture = False
        if capture and line.strip():
            wanted.append(line)
    return "\n".join(wanted[:60])


def build_pack(query: str, top: int) -> str:
    tokens = tokenize(query)
    dimensions = infer_dimensions(query)
    pages = collect_pages()
    scored = [score_page(page, tokens, dimensions) for page in pages]
    scored = [item for item in scored if item.score > 0]
    scored.sort(key=lambda item: item.score, reverse=True)
    top_pages = scored[:top]

    concept_hits = [item for item in top_pages if item.page.kind == "concept"]
    synthesis_hits = [item for item in top_pages if item.page.kind == "synthesis"]

    out: list[str] = []
    out.append(f"# KB Context Pack: {query}")
    out.append("")
    out.append("## Query Understanding")
    out.append(f"- Tokens: {', '.join(tokens) if tokens else '(none)'}")
    out.append(f"- Dimension hints: {', '.join(dimensions) if dimensions else 'UNKNOWN'}")
    out.append("")
    out.append("## User Profile Anchors")
    out.append(user_profile_summary())
    out.append("")
    out.append("## Retrieved Pages")
    if not top_pages:
        out.append("- No direct matches. Read `wiki/1_Index/master_index.md` and ask for a broader query.")
    for i, item in enumerate(top_pages, 1):
        page = item.page
        reason = f" reasons={', '.join(item.reasons)}" if item.reasons else ""
        out.append(f"{i}. **{page.title}** (`{page.rel}`, {page.kind}, score={item.score:.1f}{reason})")
        out.append(f"   - Excerpt: {excerpt(page.body, tokens)}")
        if page.links:
            out.append(f"   - Links: {', '.join(page.links[:8])}")
    out.append("")
    out.append("## Context Assembly Guidance")
    out.append("- Read the top concept cards before answering; use synthesis reports for cross-dimensional judgment.")
    out.append("- Preserve uncertainty: if a feature or claim is not in retrieved files, mark it UNKNOWN.")
    out.append("- If the answer creates a reusable insight across 2+ concept cards, ask whether to write back to `wiki/3_Synthesis/`.")
    if concept_hits:
        out.append(f"- Primary concept cards: {', '.join(f'[[{Path(item.page.rel).stem}]]' for item in concept_hits[:6])}")
    if synthesis_hits:
        out.append(f"- Useful synthesis reports: {', '.join(f'[[{Path(item.page.rel).stem}]]' for item in synthesis_hits[:4])}")
    out.append("")
    out.append("## Gaps / Follow-up")
    if dimensions:
        out.append(f"- Check `master_index.md` gaps for: {', '.join(dimensions)}")
    else:
        out.append("- Dimension is unclear; classify the query against the five-dimension tree before acting.")
    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a knowledge-vault context pack for a query.")
    parser.add_argument("query", help="Topic or question to retrieve context for")
    parser.add_argument("--top", type=int, default=8, help="Number of pages to include")
    args = parser.parse_args()
    print(build_pack(args.query, args.top))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
