#!/usr/bin/env python3
"""
Generate structural graph insights for the local Agent-driven knowledge vault.

Phase-1 prototype:
- no external dependencies
- parses wikilinks from concept cards and synthesis reports
- detects isolated pages, hubs, bridge nodes, connected components, and dimension coverage
"""

from __future__ import annotations

import argparse
import re
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CONCEPTS = ROOT / "wiki" / "2_Concepts"
SYNTHESIS = ROOT / "wiki" / "3_Synthesis"
MASTER_INDEX = ROOT / "wiki" / "1_Index" / "master_index.md"


DIMENSION_MARKERS = {
    "AI Engineering": "## AI Engineering",
    "Knowledge Systems": "## Knowledge Systems",
    "Product & Business": "## Product & Business",
    "Distribution & Brand": "## Distribution & Brand",
    "Finance & Investing": "## Finance & Investing",
}


@dataclass
class Node:
    slug: str
    title: str
    path: Path
    kind: str
    dimension: str
    outlinks: set[str]
    inlinks: set[str]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")
    except FileNotFoundError:
        return ""


def extract_title(path: Path, text: str) -> str:
    heading = re.search(r"^#\s+(.+)$", text, re.M)
    if heading:
        return heading.group(1).strip()
    return path.stem


def extract_links(text: str) -> set[str]:
    links = set()
    for match in re.finditer(r"\[\[([^\]]+)\]\]", text):
        target = match.group(1).split("|", 1)[0].strip()
        if target:
            links.add(Path(target).stem)
    return links


def parse_master_dimensions() -> dict[str, str]:
    text = read_text(MASTER_INDEX)
    dimensions: dict[str, str] = {}
    current = "UNKNOWN"
    for line in text.splitlines():
        for dim, marker in DIMENSION_MARKERS.items():
            if line.startswith(marker):
                current = dim
                break
        for target in re.findall(r"\[\[([^\]]+)\]\]", line):
            dimensions[Path(target.split("|", 1)[0]).stem] = current
    return dimensions


def collect_nodes(include_synthesis: bool) -> dict[str, Node]:
    dim_map = parse_master_dimensions()
    roots = [(CONCEPTS, "concept")]
    if include_synthesis:
        roots.append((SYNTHESIS, "synthesis"))
    nodes: dict[str, Node] = {}
    for root, kind in roots:
        if not root.exists():
            continue
        for path in sorted(root.glob("*.md")):
            text = read_text(path)
            slug = path.stem
            nodes[slug] = Node(
                slug=slug,
                title=extract_title(path, text),
                path=path,
                kind=kind,
                dimension=dim_map.get(slug, "UNKNOWN" if kind == "concept" else "Synthesis"),
                outlinks=extract_links(text),
                inlinks=set(),
            )

    for slug, node in nodes.items():
        for target in node.outlinks:
            if target in nodes and target != slug:
                nodes[target].inlinks.add(slug)
    return nodes


def undirected_neighbors(nodes: dict[str, Node]) -> dict[str, set[str]]:
    neighbors: dict[str, set[str]] = {slug: set() for slug in nodes}
    for slug, node in nodes.items():
        for target in node.outlinks:
            if target in nodes and target != slug:
                neighbors[slug].add(target)
                neighbors[target].add(slug)
    return neighbors


def connected_components(nodes: dict[str, Node]) -> list[set[str]]:
    neighbors = undirected_neighbors(nodes)
    seen: set[str] = set()
    comps: list[set[str]] = []
    for slug in nodes:
        if slug in seen:
            continue
        comp: set[str] = set()
        queue = deque([slug])
        seen.add(slug)
        while queue:
            cur = queue.popleft()
            comp.add(cur)
            for nxt in neighbors[cur]:
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
        comps.append(comp)
    comps.sort(key=len, reverse=True)
    return comps


def degree(node: Node) -> int:
    return len(node.outlinks) + len(node.inlinks)


def dimension_counts(nodes: dict[str, Node]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for node in nodes.values():
        counts[node.dimension] += 1
    return dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))


def find_bridges(nodes: dict[str, Node]) -> list[tuple[Node, set[str]]]:
    bridges: list[tuple[Node, set[str]]] = []
    for node in nodes.values():
        dims = set()
        for linked in node.outlinks | node.inlinks:
            if linked in nodes:
                dims.add(nodes[linked].dimension)
        dims.discard(node.dimension)
        if len(dims) >= 2:
            bridges.append((node, dims))
    bridges.sort(key=lambda item: (len(item[1]), degree(item[0])), reverse=True)
    return bridges


def render_report(nodes: dict[str, Node]) -> str:
    comps = connected_components(nodes)
    isolated = sorted((n for n in nodes.values() if degree(n) == 0), key=lambda n: n.slug)
    weak = sorted((n for n in nodes.values() if degree(n) == 1), key=lambda n: n.slug)
    hubs = sorted(nodes.values(), key=degree, reverse=True)[:10]
    bridges = find_bridges(nodes)[:10]
    dims = dimension_counts(nodes)

    out: list[str] = []
    out.append("# KB Graph Insights")
    out.append("")
    out.append("## Summary")
    out.append(f"- Nodes: {len(nodes)}")
    out.append(f"- Connected components: {len(comps)}")
    out.append(f"- Largest component: {len(comps[0]) if comps else 0} nodes")
    out.append(f"- Isolated nodes: {len(isolated)}")
    out.append(f"- Weakly connected nodes (degree=1): {len(weak)}")
    out.append("")
    out.append("## Dimension Coverage")
    for dim, count in dims.items():
        out.append(f"- {dim}: {count}")
    out.append("")
    out.append("## Hub Nodes")
    for node in hubs:
        out.append(f"- [[{node.slug}]] ({node.dimension}, degree={degree(node)}, out={len(node.outlinks)}, in={len(node.inlinks)})")
    out.append("")
    out.append("## Bridge Candidates")
    if not bridges:
        out.append("- No cross-dimension bridge candidates found.")
    for node, bridge_dims in bridges:
        out.append(f"- [[{node.slug}]] bridges {node.dimension} ↔ {', '.join(sorted(bridge_dims))} (degree={degree(node)})")
    out.append("")
    out.append("## Isolated Nodes")
    if not isolated:
        out.append("- None.")
    for node in isolated:
        out.append(f"- [[{node.slug}]] ({node.dimension})")
    out.append("")
    out.append("## Weakly Connected Nodes")
    if not weak:
        out.append("- None.")
    for node in weak[:30]:
        out.append(f"- [[{node.slug}]] ({node.dimension}, degree=1)")
    if len(weak) > 30:
        out.append(f"- ...and {len(weak) - 30} more")
    out.append("")
    out.append("## Components")
    for i, comp in enumerate(comps[:10], 1):
        members = sorted(comp)
        dims_in_comp = sorted(set(nodes[m].dimension for m in members))
        out.append(f"{i}. size={len(members)} dims={', '.join(dims_in_comp)}")
        out.append(f"   - {', '.join(f'[[{m}]]' for m in members[:12])}")
        if len(members) > 12:
            out.append(f"   - ...and {len(members) - 12} more")
    out.append("")
    out.append("## Suggested Actions")
    out.append("- Add links from isolated/weak nodes to at least 2 related concept cards.")
    out.append("- Review bridge candidates as possible context-pack anchors.")
    out.append("- If a component is large but single-dimension, look for cross-dimension synthesis opportunities.")
    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate knowledge-vault graph insights.")
    parser.add_argument("--include-synthesis", action="store_true", help="Include wiki/3_Synthesis pages as graph nodes")
    args = parser.parse_args()
    nodes = collect_nodes(include_synthesis=args.include_synthesis)
    print(render_report(nodes))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
