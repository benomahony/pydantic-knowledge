"""Deterministic concept-map geometry and SVG, derived only from a KnowledgeBase.

The map has a stable geography: the most structurally connected concept sits in the
centre and each domain keeps a fixed cell around it. Nothing here is configured
separately from the knowledge base; changing concepts, relationships, jobs or journeys
and rebuilding changes the map.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass
from html import escape

from .models import Depth, Experience, Intent, KnowledgeBase, Preference, RelationKind, Role

WIDTH = 1000.0
COLUMNS = (170.0, 500.0, 830.0)
CELL_W = 320.0
NODE_H = 32.0
HUB_H = 44.0
GAP = 12.0
LABEL_H = 30.0
ROW_GAP = 64.0
CHAR_W = 6.3
JOB_H = 30.0


def _e(value: object) -> str:
    return escape(str(value), quote=True)


def humanise(kind: str) -> str:
    return kind.replace("_", " ")


def _n(value: float) -> str:
    return f"{value:.1f}".rstrip("0").rstrip(".")


@dataclass(frozen=True)
class Node:
    id: str
    title: str
    domain: str
    x: float
    y: float
    w: float
    h: float
    hub: bool = False

    @property
    def cx(self) -> float:
        return self.x + self.w / 2

    @property
    def cy(self) -> float:
        return self.y + self.h / 2


@dataclass(frozen=True)
class DomainLabel:
    name: str
    x: float
    y: float


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    kinds: tuple[str, ...]
    labels: tuple[str, ...]
    structural: bool
    core: bool


@dataclass(frozen=True)
class ConceptMap:
    nodes: dict[str, Node]
    domains: tuple[DomainLabel, ...]
    edges: tuple[Edge, ...]
    hub: str
    top: float
    bottom: float


def graph_concepts(kb: KnowledgeBase) -> list[str]:
    """Concepts that take part in relationships, jobs or journeys, in authored order."""
    wanted: set[str] = set()
    for relation in kb.relationships:
        wanted |= {relation.source, relation.target}
    for journey in kb.journeys:
        wanted |= {step.concept_id for step in journey.steps}
    for job in kb.jobs:
        wanted |= set(job.expected_concepts)
    return [
        c.id
        for c in kb.concepts
        if c.id in wanted and not c.show_ontology and c.role is Role.CONCEPT
    ]


IMPLEMENTS = (RelationKind.IS_A, RelationKind.PROVIDES)


def implementations(kb: KnowledgeBase) -> dict[str, list[str]]:
    """Pages outside the map that are kinds of (or provide) a mapped concept."""
    mapped = set(graph_concepts(kb))
    out: dict[str, list[str]] = {}
    for r in kb.relationships:
        if r.kind in IMPLEMENTS and r.target in mapped and r.source not in mapped:
            out.setdefault(r.target, [])
            if r.source not in out[r.target]:
                out[r.target].append(r.source)
    return out


def _node_w(title: str, *, hub: bool = False) -> float:
    return min(max(len(title) * (CHAR_W + (0.6 if hub else 0)) + (40 if hub else 28), 84), 230)


def _edges(kb: KnowledgeBase, ids: set[str]) -> tuple[Edge, ...]:
    grouped: dict[tuple[str, str], list] = {}
    for relation in kb.relationships:
        if relation.source in ids and relation.target in ids and relation.source != relation.target:
            grouped.setdefault((relation.source, relation.target), []).append(relation)
    edges = []
    for (source, target), relations in grouped.items():
        structural = [r for r in relations if r.kind is not RelationKind.RELATED_TO]
        named = structural or relations
        kinds = tuple(dict.fromkeys(r.kind.value for r in relations))
        labels = tuple(dict.fromkeys(r.label or humanise(r.kind.value) for r in named))
        edges.append(
            Edge(
                source=source,
                target=target,
                kinds=kinds,
                labels=labels,
                structural=bool(structural),
                core=any(r.weight >= 10 for r in structural),
            )
        )
    return tuple(edges)


def _hub(order: list[str], edges: tuple[Edge, ...]) -> str:
    def degree(concept_id: str, structural_only: bool) -> int:
        neighbours = {
            e.target if e.source == concept_id else e.source
            for e in edges
            if concept_id in (e.source, e.target) and (e.structural or not structural_only)
        }
        return len(neighbours)

    return max(order, key=lambda c: (degree(c, True), degree(c, False), -order.index(c)))


def _cell(titles: list[str]) -> tuple[list[tuple[float, float, float]], float]:
    widths = [_node_w(t) for t in titles]
    two = len(titles) >= 3 and max(widths) <= (CELL_W - GAP) / 2
    columns = 2 if two else 1
    column_w = (CELL_W - GAP) / 2 if two else CELL_W
    placed = []
    for index, width in enumerate(widths):
        column, row = index % columns, index // columns
        placed.append((column * (column_w + GAP), LABEL_H + row * (NODE_H + GAP), width))
    rows = math.ceil(len(titles) / columns)
    return placed, LABEL_H + rows * (NODE_H + GAP) - GAP


def concept_map(kb: KnowledgeBase) -> ConceptMap | None:
    order = graph_concepts(kb)
    if not order:
        return None
    ids = set(order)
    edges = _edges(kb, ids)
    counts = {k: len(v) for k, v in implementations(kb).items()}

    def label(concept_id: str) -> str:
        # Width estimate includes the implementation count drawn after the title.
        n = counts.get(concept_id)
        return concepts[concept_id].title + (f"  {n}" if n else "")

    hub = _hub(order, edges)
    concepts = {c.id: c for c in kb.concepts}

    members: dict[str, list[str]] = {}
    for concept_id in order:
        if concept_id != hub:
            members.setdefault(concepts[concept_id].domain or "Other", []).append(concept_id)
    domain_order = [d for d in kb.domains if d in members] + [
        d for d in members if d not in kb.domains
    ]

    # Perimeter slots: three across the top, one either side of the hub, then rows below.
    slots: list[list[tuple[str | None, float]]] = [[], [], []]
    for index, name in enumerate(domain_order):
        if index < 3:
            slots[0].append((name, COLUMNS[index]))
        elif index == 3:
            slots[1].append((name, COLUMNS[0]))
        elif index == 4:
            slots[1].append((name, COLUMNS[2]))
        else:
            slots[-1].append((name, 0.0))
            if len(slots[-1]) == 3 and index != len(domain_order) - 1:
                slots.append([])
    slots[1].append((None, COLUMNS[1]))
    for row in slots[2:]:
        spread = {1: [500.0], 2: [335.0, 665.0], 3: list(COLUMNS)}[len(row)] if row else []
        row[:] = [(name, x) for (name, _), x in zip(row, spread, strict=True)]

    nodes: dict[str, Node] = {}
    labels: list[DomainLabel] = []
    y = 0.0
    for row in slots:
        if not row:
            continue
        cells = {name: _cell([label(c) for c in members[name]]) for name, _ in row if name}
        height = max(
            [h for _, h in cells.values()] + ([LABEL_H + HUB_H] if row is slots[1] else [])
        )
        for name, cx in row:
            if name is None:
                title = concepts[hub].title
                w = _node_w(title, hub=True)
                nodes[hub] = Node(
                    hub,
                    title,
                    concepts[hub].domain or "Other",
                    cx - w / 2,
                    y + (height - HUB_H) / 2 + LABEL_H / 2,
                    w,
                    HUB_H,
                    hub=True,
                )
                continue
            left = cx - CELL_W / 2
            labels.append(DomainLabel(name, left, y + 12))
            placed, _ = cells[name]
            for concept_id, (dx, dy, w) in zip(members[name], placed, strict=True):
                nodes[concept_id] = Node(
                    concept_id, concepts[concept_id].title, name, left + dx, y + dy, w, NODE_H
                )
        y += height + ROW_GAP
    return ConceptMap(nodes, tuple(labels), edges, hub, 0.0, y - ROW_GAP)


def _anchor(node: Node, tx: float, ty: float, pad: float = 0.0) -> tuple[float, float]:
    dx, dy = tx - node.cx, ty - node.cy
    if not dx and not dy:
        return node.cx, node.cy
    sx = (node.w / 2 + pad) / abs(dx) if dx else math.inf
    sy = (node.h / 2 + pad) / abs(dy) if dy else math.inf
    scale = min(sx, sy)
    return node.cx + dx * scale, node.cy + dy * scale


def _curve(a: Node, b: Node, bend: float) -> tuple[str, float, float]:
    length = math.dist((a.cx, a.cy), (b.cx, b.cy)) or 1
    offset = min(length * bend, 70)
    nx, ny = -(b.cy - a.cy) / length, (b.cx - a.cx) / length
    qx, qy = (a.cx + b.cx) / 2 + nx * offset, (a.cy + b.cy) / 2 + ny * offset
    x1, y1 = _anchor(a, qx, qy, 1)
    x2, y2 = _anchor(b, qx, qy, 3)
    lx, ly = 0.25 * x1 + 0.5 * qx + 0.25 * x2, 0.25 * y1 + 0.5 * qy + 0.25 * y2
    return f"M{_n(x1)} {_n(y1)}Q{_n(qx)} {_n(qy)} {_n(x2)} {_n(y2)}", lx, ly


def _jobs_band(
    kb: KnowledgeBase, top: float
) -> tuple[dict[str, tuple[float, float, float]], float]:
    """Place jobs in centred rows above the map; returns positions and the band top."""
    widths = [_node_w(job.title) + 18 for job in kb.jobs]
    rows: list[list[int]] = [[]]
    used = 0.0
    for index, width in enumerate(widths):
        if rows[-1] and used + width + GAP > WIDTH:
            rows.append([])
            used = 0.0
        rows[-1].append(index)
        used += width + GAP
    band_top = top - 96 - (len(rows) - 1) * (JOB_H + GAP)
    placed = {}
    for r, row in enumerate(rows):
        total = sum(widths[i] for i in row) + GAP * (len(row) - 1)
        x = (WIDTH - total) / 2
        for i in row:
            placed[kb.jobs[i].id] = (x, band_top + r * (JOB_H + GAP), widths[i])
            x += widths[i] + GAP
    return placed, band_top


def _box(left: float, top: float, right: float, bottom: float, pad: float = 18) -> str:
    return " ".join(
        _n(v) for v in (left - pad, top - pad, right - left + 2 * pad, bottom - top + 2 * pad)
    )


def job_concepts(kb: KnowledgeBase, job_id: str) -> list[str]:
    job = kb.job(job_id)
    ids = list(job.expected_concepts)
    for journey in kb.journeys:
        if journey.job_id == job_id:
            ids += [s.concept_id for s in journey.steps]
    return list(dict.fromkeys(ids))


def ontology_svg(kb: KnowledgeBase, href: Callable[[str], str]) -> str:
    graph = concept_map(kb)
    if graph is None:
        return ""
    nodes = graph.nodes
    left = min(n.x for n in nodes.values())
    right = max(n.x + n.w for n in nodes.values())
    left = min([left] + [d.x for d in graph.domains])
    concepts_box = _box(min(left, 0), graph.top, max(right, WIDTH), graph.bottom)

    parts = [
        '<defs><marker id="o-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" '
        'markerHeight="7" orient="auto-start-reverse"><path d="M1 1.5 8 5 1 8.5" fill="none" '
        'stroke="context-stroke" stroke-width="1.6" stroke-linecap="round" '
        'stroke-linejoin="round"/></marker></defs>'
    ]
    parts.append('<g class="o-domains" aria-hidden="true">')
    for domain in graph.domains:
        parts.append(
            f'<text class="o-domain" x="{_n(domain.x)}" y="{_n(domain.y)}">{_e(domain.name)}</text>'
        )
    parts.append("</g>")

    edge_parts, label_parts = ['<g class="o-edges" aria-hidden="true">'], ['<g class="o-labels">']
    for index, edge in enumerate(graph.edges):
        a, b = nodes[edge.source], nodes[edge.target]
        d, lx, ly = _curve(a, b, 0.12)
        classes = "o-edge " + ("is-structural" if edge.structural else "is-route")
        classes += " is-core" if edge.core else ""
        text = " · ".join(edge.labels)
        edge_parts.append(
            f'<path class="{classes}" data-edge="{index}" data-source="{_e(edge.source)}" '
            f'data-target="{_e(edge.target)}" data-kinds="{_e(" ".join(edge.kinds))}" d="{d}" '
            f'marker-end="url(#o-arrow)"><title>{_e(a.title)} {_e(text)} {_e(b.title)}</title></path>'
        )
        label_parts.append(
            f'<text class="o-label{" is-core" if edge.core else ""}" data-edge="{index}" '
            f'x="{_n(lx)}" y="{_n(ly)}">{_e(text)}</text>'
        )
    edge_parts.append("</g>")
    label_parts.append("</g>")
    parts += edge_parts

    # Journeys: an ordered route through concepts, drawn only in the journeys view.
    parts.append('<g class="o-journeys" aria-hidden="true">')
    badges = ['<g class="o-journeys" aria-hidden="true">']
    for journey in kb.journeys:
        steps = [s.concept_id for s in journey.steps if s.concept_id in nodes]
        parts.append(f'<g class="o-journey" data-journey="{_e(journey.id)}">')
        badges.append(f'<g class="o-journey" data-journey="{_e(journey.id)}">')
        for first, second in zip(steps, steps[1:], strict=False):
            if first != second:
                d, _, _ = _curve(nodes[first], nodes[second], 0.2)
                parts.append(f'<path class="o-step" d="{d}" marker-end="url(#o-arrow)"/>')
        seen: dict[str, int] = {}
        for number, concept_id in enumerate(steps, start=1):
            node = nodes[concept_id]
            shift = seen.get(concept_id, 0) * 20
            seen[concept_id] = seen.get(concept_id, 0) + 1
            cx, cy = node.x + 2 + shift, node.y + 1
            badges.append(
                f'<g class="o-badge"><circle cx="{_n(cx)}" cy="{_n(cy)}" r="10"/>'
                f'<text x="{_n(cx)}" y="{_n(cy)}">{number}</text></g>'
            )
        parts.append("</g>")
        badges.append("</g>")
    parts.append("</g>")
    badges.append("</g>")

    jobs_box = concepts_box
    if kb.jobs:
        placed, band_top = _jobs_band(kb, graph.top)
        jobs_box = _box(min(left, 0), band_top, max(right, WIDTH), graph.bottom)
        parts.append('<g class="o-jobs">')
        for job in kb.jobs:
            x, y, w = placed[job.id]
            for concept_id in job_concepts(kb, job.id):
                if concept_id not in nodes:
                    continue
                node = nodes[concept_id]
                sx, sy, ex, ey = x + w / 2, y + JOB_H, node.cx, node.y
                bend = max((ey - sy) * 0.55, 30)
                parts.append(
                    f'<path class="o-joblink" data-job="{_e(job.id)}" data-concept="{_e(concept_id)}" '
                    f'd="M{_n(sx)} {_n(sy)}C{_n(sx)} {_n(sy + bend)} {_n(ex)} {_n(ey - bend)} '
                    f'{_n(ex)} {_n(ey - 2)}" aria-hidden="true"/>'
                )
        for job in kb.jobs:
            x, y, w = placed[job.id]
            parts.append(
                f'<g class="o-job" data-job="{_e(job.id)}" tabindex="0" role="button" '
                f'aria-pressed="false" aria-label="Job: {_e(job.title)}">'
                f'<rect x="{_n(x)}" y="{_n(y)}" width="{_n(w)}" height="{_n(JOB_H)}" rx="15"/>'
                f'<text x="{_n(x + w / 2)}" y="{_n(y + JOB_H / 2)}">{_e(job.title)}</text></g>'
            )
        parts.append("</g>")

    parts.append('<g class="o-nodes">')
    counts = {k: len(v) for k, v in implementations(kb).items()}
    for concept_id in graph_concepts(kb):
        node = nodes[concept_id]
        n = counts.get(concept_id)
        count = f'<tspan class="o-count" dx="6">{n}</tspan>' if n else ""
        cls = "o-node is-hub" if node.hub else "o-node"
        parts.append(
            f'<a class="{cls}" href="{_e(href(concept_id))}" data-id="{_e(concept_id)}" '
            f'aria-label="{_e(node.title)}, {_e(node.domain)}">'
            f'<rect x="{_n(node.x)}" y="{_n(node.y)}" width="{_n(node.w)}" height="{_n(node.h)}" '
            f'rx="{8 if node.hub else 6}"/>'
            f'<text x="{_n(node.cx)}" y="{_n(node.cy)}">{_e(node.title)}{count}</text></a>'
        )
    parts.append("</g>")
    parts += badges
    parts += label_parts
    return (
        f'<svg class="o-svg" viewBox="{concepts_box}" data-concepts-box="{concepts_box}" '
        f'data-jobs-box="{jobs_box}" role="group" aria-label="Concept map of {_e(kb.title)}" '
        f'preserveAspectRatio="xMidYMid meet">{"".join(parts)}</svg>'
    )


def layers_html(kb: KnowledgeBase) -> str:
    """The documentation layers, with counts read from this knowledge base."""
    graph_ids = graph_concepts(kb)
    blocks = sum(len(c.blocks) for c in kb.concepts)
    phrases = sum(len(j.examples) for j in kb.jobs)
    steps = sum(len(j.steps) for j in kb.journeys)
    contexts = len(Intent) * len(Experience) * len(Preference) * len(Depth)

    def plural(n: int, word: str) -> str:
        return f"{n:,} {word}{'' if n == 1 else 's'}"

    layers = [
        (
            "Jobs to be Done",
            f"{plural(len(kb.jobs), 'job')} · {plural(phrases, 'example phrase')}",
            "The outcome a reader wants, in their own words. Example phrases double as "
            "evaluation cases.",
            "realised by",
        ),
        (
            "User journeys",
            f"{plural(len(kb.journeys), 'journey')} · {plural(steps, 'step')}",
            "Ordered routes through concepts that accomplish a job, each step with a reason.",
            "visits",
        ),
        (
            "Ontology",
            f"{plural(len(graph_ids), 'concept')} · "
            f"{plural(len(kb.relationships), 'relationship')}",
            "Concepts and typed relationships. The sidebar is one projection of this graph.",
            "explained by",
        ),
        (
            "Authored knowledge blocks",
            f"{plural(blocks, 'block')} across {plural(len(kb.concepts), 'page')}",
            "Definitions, examples, procedures and complete source sections, written by people.",
            "composed into",
        ),
        (
            "Contextual composition",
            f"{plural(contexts, 'reading context')}",
            "Deterministic selection and ordering of authored blocks for intent, experience, "
            "style and depth.",
            None,
        ),
    ]
    items = []
    for name, count, description, link in layers:
        items.append(
            f'<li class="layer"><div class="layer-head"><span class="layer-name">{_e(name)}</span>'
            f'<span class="layer-count">{_e(count)}</span></div><p>{_e(description)}</p></li>'
        )
        if link:
            items.append(f'<li class="layer-link" aria-hidden="true"><span>{_e(link)}</span></li>')
    return (
        '<figure class="layers"><ol class="layers-list">'
        + "".join(items)
        + "</ol><figcaption>Counts are read from the knowledge base this page was built "
        "from.</figcaption></figure>"
    )
