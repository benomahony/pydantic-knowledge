from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from enum import StrEnum
from html import escape, unescape
from importlib.resources import files
from pathlib import Path

import markdown

from .models import (
    BlockKind,
    Concept,
    Depth,
    DocsContext,
    Experience,
    Intent,
    KnowledgeBase,
    KnowledgeBlock,
    NavItem,
    Preference,
    RelationKind,
)
from .ontology import (
    IMPLEMENTS,
    ConceptMap,
    concept_map,
    graph_concepts,
    humanise,
    implementations,
    job_concepts,
    layers_html,
    ontology_svg,
)


class BuildTarget(StrEnum):
    SITE = "site"
    OFFLINE = "offline"
    SINGLE = "single"


def _e(value: object) -> str:
    return escape(str(value), quote=True)


def _asset(name: str) -> str:
    return files("pydantic_knowledge").joinpath("assets", name).read_text(encoding="utf-8").strip()


CSS = _asset("docs.css")
THEME_SCRIPT = _asset("theme.js")
DECISION_JS = _asset("decision.js")
JS = _asset("docs.js")

_MARKDOWN_EXTENSIONS = [
    "extra",
    "toc",
    "admonition",
    "pymdownx.highlight",
    "pymdownx.inlinehilite",
    "pymdownx.superfences",
    "pymdownx.tabbed",
    "pymdownx.details",
]
_MARKDOWN_CONFIG = {
    "pymdownx.highlight": {"use_pygments": True, "guess_lang": False},
    "pymdownx.tabbed": {"alternate_style": True},
}

# Human labels for reading-context values; the values themselves stay in the model.
CONTEXT_LABELS: dict[str, dict[str, str]] = {
    "intent": {
        Intent.LEARN: "Learning",
        Intent.BUILD: "Building",
        Intent.FIX: "Fixing a problem",
        Intent.CHOOSE: "Choosing an approach",
        Intent.MIGRATE: "Migrating",
        Intent.TEST: "Testing",
        Intent.OPERATE: "Running in production",
        Intent.EXTEND: "Extending",
        Intent.REFERENCE: "Looking something up",
    },
    "experience": {
        Experience.NEW: "New",
        Experience.FAMILIAR: "Familiar",
        Experience.EXPERT: "Expert",
    },
    "preference": {
        Preference.CODE_FIRST: "Code first",
        Preference.EXPLANATION_FIRST: "Explanation first",
        Preference.REFERENCE: "Reference",
    },
    "depth": {Depth.QUICK: "Concise", Depth.NORMAL: "Standard", Depth.DEEP: "In depth"},
}


def _markdown(text: str) -> str:
    return markdown.markdown(
        text, extensions=_MARKDOWN_EXTENSIONS, extension_configs=_MARKDOWN_CONFIG
    )


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "section"


def _complete_ids(concept: Concept) -> set[str]:
    """The complete page is the imported source when present, otherwise every block."""
    source = [b.id for b in concept.blocks if b.format == "markdown"]
    return set(source) if source else {b.id for b in concept.blocks}


def _is_adaptive(concept: Concept) -> bool:
    return any(
        b.format != "markdown" and (b.intents or b.experiences or b.preferences or b.depths)
        for b in concept.blocks
    )


def _block_html(block: KnowledgeBlock, index: int, *, complete: bool) -> str:
    attrs = [
        f'data-block="{_e(block.id)}"',
        f'data-kind="{block.kind.value}"',
        f'data-weight="{block.weight}"',
    ]
    for name, values in (
        ("intents", block.intents),
        ("experiences", block.experiences),
        ("preferences", block.preferences),
        ("depths", block.depths),
    ):
        if values:
            attrs.append(f'data-{name}="{" ".join(sorted(v.value for v in values))}"')
    if complete:
        attrs.append("data-complete")
    if block.format == "markdown":
        # Imported pages are content, not code: scripts from the source never run here.
        html = re.sub(r"<script\b.*?</script\s*>", "", _markdown(block.body), flags=re.S | re.I)
        html = _annotations(html, index)
        cls = "knowledge-block is-source"
    else:
        heading = f'<h2 id="{_slug(block.title)}">{_e(block.title)}</h2>' if block.title else ""
        if block.kind is BlockKind.EXAMPLE:
            fence = "`" * max(
                3, max((len(m) for m in re.findall(r"`+", block.body)), default=0) + 1
            )
            body = _markdown(f"{fence}{block.language or 'text'}\n{block.body}\n{fence}")
        else:
            body = "".join(f"<p>{_e(p)}</p>" for p in block.body.split("\n\n") if p.strip())
        html = heading + body
        cls = f"knowledge-block is-authored kind-{block.kind.value.replace('_', '-')}"
    # Per-block counters (tabs, footnotes) restart in each Markdown call; keep them distinct.
    html = re.sub(r'(?<=["#])__tabbed_', f"__tabbed_b{index}_", html)
    html = re.sub(r'(?<=["#])(fn|fnref):', rf"\1:b{index}-", html)
    return f'<section class="{cls}" {" ".join(attrs)}>{html}</section>'


def _top_level_items(html: str) -> list[str]:
    """Contents of each top-level <li> in a list body, respecting nested lists."""
    items, depth, start = [], 0, 0
    for m in re.finditer(r"<li\b[^>]*>|</li>", html):
        if m[0].startswith("<li"):
            if depth == 0:
                start = m.end()
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                items.append(html[start : m.start()])
    return items


_ANNOTATED = re.compile(
    r'(<div class="highlight">(?:(?!<div class="highlight">).)*?</div>)\s*<ol>(.*?)</ol>',
    flags=re.S,
)
_MARKER = re.compile(r'<span class="c[a-z0-9]*">#\s*\((\d+)\)!</span>')


def _annotations(html: str, block: int) -> str:
    """Code annotations (`# (1)!` plus the following list) become popovers, as upstream."""
    counter = 0

    def replace(match: re.Match) -> str:
        nonlocal counter
        code, listing = match[1], match[2]
        if not _MARKER.search(code):
            return match[0]
        counter += 1
        notes = _top_level_items(listing)
        base = f"ann-b{block}-{counter}"

        def marker(m: re.Match) -> str:
            n = int(m[1])
            if n > len(notes):
                return m[0]
            return (
                f'<button type="button" class="code-annotation" popovertarget="{base}-{n}" '
                f'aria-label="Annotation {n}" style="anchor-name:--{base}-{n}"></button>'
            )

        popovers = "".join(
            f'<div class="annotation-popover" popover id="{base}-{n}" '
            f'style="position-anchor:--{base}-{n}">{note}</div>'
            for n, note in enumerate(notes, start=1)
        )
        return _MARKER.sub(marker, code) + popovers

    return _ANNOTATED.sub(replace, html)


_ID = re.compile(r'(?<![\w-])id="([^"]+)"')


def _scope_ids(html: str, prefix: str) -> str:
    """Make element IDs unique within a page and optionally namespace them."""
    seen: set[str] = set()
    mapping: dict[str, str] = {}

    def rename(match: re.Match) -> str:
        old = match[1]
        new, n = old, 1
        while new in seen:
            new, n = f"{old}_{n}", n + 1
        seen.add(new)
        mapping.setdefault(old, prefix + new)
        return f'id="{prefix + new}"'

    html = _ID.sub(rename, html)
    if not prefix:
        return html
    html = re.sub(r'(?<![\w-])for="([^"]+)"', lambda m: f'for="{mapping.get(m[1], m[1])}"', html)
    html = re.sub(
        r'popovertarget="([^"]+)"', lambda m: f'popovertarget="{mapping.get(m[1], m[1])}"', html
    )
    html = html.replace("--ann-", f"--{prefix}ann-")
    html = re.sub(r'\bname="(__tabbed_[^"]+)"', lambda m: f'name="{prefix}{m[1]}"', html)
    html = re.sub(
        r"url\(#([^)]+)\)", lambda m: f"url(#{mapping.get(m[1], m[1])})", html
    )
    return re.sub(
        r'href="#([^"]+)"',
        lambda m: f'href="#{mapping[m[1]]}"' if m[1] in mapping else m[0],
        html,
    )


@dataclass
class _Ctx:
    """How one build target addresses pages."""

    kb: KnowledgeBase
    target: BuildTarget
    prefix: str = ""
    graph: ConceptMap | None = field(init=False)

    def __post_init__(self) -> None:
        self.graph = concept_map(self.kb)

    @property
    def single(self) -> bool:
        return self.target is BuildTarget.SINGLE

    def href(self, concept_id: str, fragment: str | None = None) -> str:
        if self.single:
            return f"#{concept_id}--{fragment}" if fragment else f"#{concept_id}"
        page = f"{self.prefix}concepts/{concept_id}.html"
        return f"{page}#{fragment}" if fragment else page

    def root_href(self, concept_id: str) -> str:
        """Address relative to the site root, for shared data."""
        return f"#{concept_id}" if self.single else f"concepts/{concept_id}.html"

    def home_href(self) -> str:
        home = self.kb.home_concept or self.kb.concepts[0].id
        return f"#{home}" if self.single else f"{self.prefix}index.html"


def _resolve_links(html: str, ctx: _Ctx, known: set[str]) -> str:
    def link(match: re.Match) -> str:
        concept_id, fragment = match[1], match[2]
        if concept_id not in known:
            return 'href="#"'
        return f'href="{_e(ctx.href(concept_id, fragment))}"'

    return re.sub(r'href="knowledge:([^"#]+)(?:#([^"]*))?"', link, html)


def _strip_tags(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html).strip()


_TOP_LEVEL = re.compile(
    r'<(?:section class="(knowledge-block[^"]*|ontology|related)"([^>]*)>|figure )'
)


def _toc(html: str) -> list[tuple[int, str, str, bool]]:
    """Headings with a flag saying whether they are visible in the complete page."""
    starts = [
        (m.start(), not (m[1] or "").startswith("knowledge-block") or "data-complete" in m[2])
        for m in _TOP_LEVEL.finditer(html)
    ]
    out = []
    for m in re.finditer(r'<h([23]) id="([^"]+)"[^>]*>(.*?)</h\1>', html, flags=re.S):
        visible = next((flag for pos, flag in reversed(starts) if pos < m.start()), True)
        out.append((int(m[1]), m[2], unescape(_strip_tags(m[3])), visible))
    return out


# --- Navigation --------------------------------------------------------------


def _leaves(items: tuple[NavItem, ...]) -> list[NavItem]:
    out = []
    for item in items:
        if item.concept_id:
            out.append(item)
        out += _leaves(item.children)
    return out


def _contains(item: NavItem, concept_id: str) -> bool:
    return item.concept_id == concept_id or any(_contains(c, concept_id) for c in item.children)


def _trail(items: tuple[NavItem, ...], concept_id: str) -> list[str]:
    for item in items:
        if item.concept_id == concept_id:
            return []
        if item.children and _contains(item, concept_id):
            return [item.label, *_trail(item.children, concept_id)]
    return []


def _nav_items(kb: KnowledgeBase) -> tuple[NavItem, ...]:
    if kb.projections:
        return kb.projections[0].items
    return tuple(NavItem(label=c.title, concept_id=c.id) for c in kb.concepts)


def _nav_tree(
    items: tuple[NavItem, ...], ctx: _Ctx, current: str | None, expand: bool = True
) -> str:
    rows = []
    # A page can appear in several groups (a goal and its domain); open only the last,
    # which is its canonical place.
    holders = [i for i in items if i.children and current and _contains(i, current)]
    for item in items:
        if item.children:
            is_open = " open" if expand and holders and item is holders[-1] else ""
            rows.append(
                f'<li><details class="nav-group"{is_open}><summary>{_e(item.label)}</summary>'
                f"{_nav_tree(item.children, ctx, current, bool(is_open))}</details></li>"
            )
        elif item.concept_id:
            here = ' aria-current="page"' if item.concept_id == current else ""
            rows.append(
                f'<li><a class="nav-link" href="{_e(ctx.href(item.concept_id))}" '
                f'data-concept="{_e(item.concept_id)}"{here}>{_e(item.label)}</a></li>'
            )
    return '<ul class="nav-list">' + "".join(rows) + "</ul>"


# --- Page parts ----------------------------------------------------------------


@dataclass
class _Context:
    """Where a page sits in the knowledge model."""

    domain: str
    relations: list[tuple[bool, str, str, bool]]  # outbound, other, labels, structural
    jobs: list
    journeys: list[tuple[object, int]]
    about: Concept | None
    implements: list[str] = field(default_factory=list)  # mapped concepts this page is a kind of
    instances: list[str] = field(default_factory=list)  # pages that are kinds of this concept


def _context(kb: KnowledgeBase, concept: Concept, ctx: _Ctx) -> _Context | None:
    graph = ctx.graph
    if graph is None:
        return None
    about = next((c for c in kb.concepts if c.show_ontology), None)
    journeys = [
        (j, next(i for i, s in enumerate(j.steps) if s.concept_id == concept.id))
        for j in kb.journeys
        if any(s.concept_id == concept.id for s in j.steps)
    ]
    jobs = [j for j in kb.jobs if concept.id in job_concepts(kb, j.id)]
    if concept.id not in graph.nodes:
        implements = list(
            dict.fromkeys(
                r.target
                for r in kb.relationships
                if r.source == concept.id and r.kind in IMPLEMENTS and r.target in graph.nodes
            )
        )
        if not implements and not concept.domain:
            return None
        return _Context(
            domain=concept.domain or graph.nodes[implements[0]].domain,
            relations=[],
            jobs=jobs,
            journeys=journeys,
            about=about,
            implements=implements,
        )
    instances = implementations(kb).get(concept.id, [])
    rows: dict[tuple[bool, str], list[str]] = {}
    structural: set[tuple[bool, str]] = set()
    for r in kb.relationships:
        if concept.id not in (r.source, r.target) or r.source == r.target:
            continue
        key = (r.source == concept.id, r.target if r.source == concept.id else r.source)
        if key[1] in instances:
            continue
        label = r.label or humanise(r.kind.value)
        if r.kind is not RelationKind.RELATED_TO:
            if key not in structural:
                rows[key] = []
            structural.add(key)
        elif key in structural:
            continue
        if label not in rows.setdefault(key, []):
            rows[key].append(label)
    ordered = sorted(rows, key=lambda k: (k not in structural, not k[0]))
    return _Context(
        domain=concept.domain or graph.nodes[concept.id].domain,
        relations=[
            (out, other, " · ".join(rows[(out, other)]), (out, other) in structural)
            for out, other in ordered
        ],
        jobs=jobs,
        journeys=journeys,
        about=about,
        instances=instances,
    )


def _context_line(kb: KnowledgeBase, info: _Context | None, ctx: _Ctx, prefix: str) -> str:
    """One quiet line under the title: the page's place in the model."""
    if info is None:
        return ""
    titles = {c.id: c.title for c in kb.concepts}
    parts = [f'<a href="#{prefix}in-the-ontology">{_e(info.domain)}</a>']
    if info.implements:
        links = ", ".join(f'<a href="{_e(ctx.href(i))}">{_e(titles[i])}</a>' for i in info.implements)
        parts.append(f"A kind of {links}")
    if info.relations:
        n = len(info.relations)
        parts.append(f"{n} related concept{'' if n == 1 else 's'}")
    if info.instances:
        n = len(info.instances)
        parts.append(f"{n} implementation{'' if n == 1 else 's'}")
    if info.journeys:
        journey, index = info.journeys[0]
        parts.append(f"{_e(journey.title)} journey, step {index + 1} of {len(journey.steps)}")
    return '<span class="kline">' + "<span>·</span>".join(parts) + "</span>"


def _context_section(kb: KnowledgeBase, concept: Concept, ctx: _Ctx, info: _Context | None) -> str:
    if info is None:
        return ""
    titles = {c.id: c.title for c in kb.concepts}
    rels = "".join(
        f'<li class="{"is-structural" if structural else "is-route"}">'
        f'<span class="k-rel">{"" if out else "← "}{_e(labels)}{" →" if out else ""}</span>'
        f'<a href="{_e(ctx.href(other))}">{_e(titles[other])}</a></li>'
        for out, other, labels, structural in info.relations
    )
    rels += "".join(
        f'<li class="is-structural"><span class="k-rel">is a kind of →</span>'
        f'<a href="{_e(ctx.href(i))}">{_e(titles[i])}</a></li>'
        for i in info.implements
    )
    if info.implements:
        siblings = [
            s for s in implementations(kb).get(info.implements[0], []) if s != concept.id
        ]
        if siblings:
            rels += (
                f'<li class="is-structural"><span class="k-rel">alternatives</span>'
                f'<details class="k-impl"><summary>{len(siblings)} other '
                f"{_e(titles[info.implements[0]].lower())} pages</summary><ul>"
                + "".join(f'<li><a href="{_e(ctx.href(o))}">{_e(titles[o])}</a></li>' for o in siblings)
                + "</ul></details></li>"
            )
    if info.instances:
        rels += (
            f'<li class="is-structural"><span class="k-rel">← implementations</span>'
            f'<details class="k-impl"><summary>{len(info.instances)} pages</summary><ul>'
            + "".join(f'<li><a href="{_e(ctx.href(o))}">{_e(titles[o])}</a></li>' for o in info.instances)
            + "</ul></details></li>"
        )
    about = info.about
    map_href = ctx.href(about.id, "concept-map") if about else None
    jobs = "".join(
        f'<li><a href="{_e(map_href)}" data-focus="job:{_e(j.id)}">{_e(j.title)}</a></li>'
        if map_href
        else f"<li>{_e(j.title)}</li>"
        for j in info.jobs
    )
    journeys = "".join(
        f'<li><a href="{_e(ctx.href(concept.id))}" data-start-journey="{_e(j.id)}">'
        f"{_e(j.title)}</a> <small>step {i + 1} of {len(j.steps)}</small></li>"
        for j, i in info.journeys
    )
    side = (
        f'<p class="k-sub">Jobs to be done</p><ul class="k-list">{jobs}</ul>' if jobs else ""
    ) + (f'<p class="k-sub">Journeys</p><ul class="k-list">{journeys}</ul>' if journeys else "")
    focus = info.implements[0] if info.implements else concept.id
    map_link = (
        f' <a href="{_e(map_href)}" data-focus="{_e(focus)}">See it in the concept map</a>'
        if map_href and (info.implements or info.relations or info.instances)
        else ""
    )
    if not rels and not side:
        return ""
    return (
        '<section class="related" aria-labelledby="in-the-ontology">'
        '<h2 id="in-the-ontology">In the ontology</h2>'
        f'<p class="k-intro">{_e(concept.title)} belongs to <strong>{_e(info.domain)}</strong>.'
        f"{map_link}</p>"
        f'<div class="k-grid"><ul class="k-rels">{rels}</ul>'
        + (f'<div class="k-side">{side}</div>' if side else "")
        + "</div></section>"
    )


def _relationship_table(kb: KnowledgeBase, ctx: _Ctx) -> str:
    titles = {c.id: c.title for c in kb.concepts}
    rows = "".join(
        f'<tr><td><a href="{_e(ctx.href(r.source))}">{_e(titles[r.source])}</a></td>'
        f"<td>{_e(r.label or humanise(r.kind.value))}</td>"
        f'<td><a href="{_e(ctx.href(r.target))}">{_e(titles[r.target])}</a></td>'
        f"<td><code>{_e(r.kind.value)}</code></td></tr>"
        for r in kb.relationships
    )
    return (
        '<details class="o-text"><summary>All relationships as a table</summary>'
        "<table><thead><tr><th>From</th><th>Relationship</th><th>To</th><th>Kind</th></tr>"
        f"</thead><tbody>{rows}</tbody></table></details>"
    )


def _ontology_html(kb: KnowledgeBase, ctx: _Ctx) -> str:
    svg = ontology_svg(kb, ctx.href)
    if not svg:
        return ""
    kinds = list(dict.fromkeys(r.kind.value for r in kb.relationships))
    # Structural relationships are shown first; reading routes are one choice away.
    if RelationKind.RELATED_TO.value in kinds and len(kinds) > 1:
        options = [
            '<option value="structural" selected>Structural</option>',
            '<option value="all">Structural and reading routes</option>',
        ]
    else:
        options = ['<option value="all">All</option>']
    options += [f'<option value="{k}">{_e(humanise(k))}</option>' for k in kinds]
    views = [
        '<button type="button" role="tab" aria-selected="true" data-view="concepts">Concepts</button>'
    ]
    if kb.jobs:
        views.append(
            '<button type="button" role="tab" aria-selected="false" data-view="jobs">'
            "Jobs to be done</button>"
        )
    if kb.journeys:
        views.append(
            '<button type="button" role="tab" aria-selected="false" data-view="journeys">'
            "Journeys</button>"
        )
    journeys = "".join(
        f'<button type="button" aria-pressed="false" data-journey="{_e(j.id)}">{_e(j.title)}</button>'
        for j in kb.journeys
    )
    return f"""<section class="ontology" data-ontology aria-labelledby="concept-map">
<h2 id="concept-map">Concept map</h2>
<p class="o-intro">Each box is a page and each line a typed relationship, both read from the knowledge base. Domains keep fixed positions so the map stays recognisable as it grows.</p>
<div class="o-toolbar" hidden><div class="o-views" role="tablist" aria-label="Map layer">{"".join(views)}</div>
<div class="o-tools"><label class="o-filter">Relationships <select data-filter>{"".join(options)}</select></label>
<span class="o-zoom"><button type="button" data-zoom="out" aria-label="Zoom out">&minus;</button><button type="button" data-zoom="in" aria-label="Zoom in">+</button><button type="button" data-zoom="fit">Reset</button></span></div></div>
<div class="o-journey-picker" hidden aria-label="Journey">{journeys}</div>
<div class="o-canvas">{svg}</div>
<div class="o-detail" aria-live="polite"><p class="o-legend"><span class="lg lg-structural"></span>Structural relationship <span class="lg lg-route"></span>Reading route <span class="lg lg-hub"></span>Most connected concept</p><p class="o-hint">Select a concept to highlight its neighbourhood. Select it again, or use the link below, to open its page.</p></div>
{_relationship_table(kb, ctx)}
</section>"""


def _pagination(kb: KnowledgeBase, concept: Concept, ctx: _Ctx) -> str:
    # Reading order follows each page's canonical (last) place, not goal shortcuts.
    seen: dict[str, NavItem] = {}
    for item in reversed(_leaves(_nav_items(kb))):
        seen.setdefault(item.concept_id, item)
    leaves = list(reversed(seen.values()))
    ids = [item.concept_id for item in leaves]
    if concept.id not in ids:
        return ""
    i = ids.index(concept.id)
    links = []
    if i > 0:
        links.append(
            f'<a class="prev" rel="prev" href="{_e(ctx.href(ids[i - 1]))}"><span>Previous</span>'
            f"<strong>{_e(leaves[i - 1].label)}</strong></a>"
        )
    if i + 1 < len(ids):
        links.append(
            f'<a class="next" rel="next" href="{_e(ctx.href(ids[i + 1]))}"><span>Next</span>'
            f"<strong>{_e(leaves[i + 1].label)}</strong></a>"
        )
    return f'<nav class="pagination" aria-label="Previous and next pages">{"".join(links)}</nav>'


@dataclass
class _Page:
    concept: Concept
    html: str
    sections: list[tuple[str, str]] = field(default_factory=list)


def _page(kb: KnowledgeBase, concept: Concept, ctx: _Ctx, known: set[str]) -> _Page:
    complete = _complete_ids(concept)
    blocks = [
        _block_html(block, i, complete=block.id in complete)
        for i, block in enumerate(concept.blocks)
    ]
    wide = concept.show_ontology and ctx.graph is not None
    if wide:
        figures = _ontology_html(kb, ctx) + layers_html(kb)
        blocks.insert(1 if blocks else 0, figures)
        blocks.append('<div class="decision-slot"></div>')
    info = _context(kb, concept, ctx)
    body = "".join(blocks) + _context_section(kb, concept, ctx, info)
    single_prefix = f"{concept.id}--" if ctx.single else ""
    body = _scope_ids(_resolve_links(body, ctx, known), single_prefix)
    toc = _toc(body)
    imported = any(b.format == "markdown" for b in concept.blocks)
    lead = (
        f'<p class="lead">{_e(concept.summary)}</p>' if concept.summary and not imported else ""
    )
    source = (
        f'<a href="{_e(concept.source_url)}">View the upstream page</a>'
        if concept.source_url
        else ""
    )
    toc_html = "".join(
        f'<li class="toc-l{level}"{"" if visible else " hidden"}>'
        f'<a href="#{_e(anchor)}">{_e(text)}</a></li>'
        for level, anchor, text, visible in toc
    )
    aside = (
        ""
        if wide
        else '<aside class="toc" aria-label="On this page"><h2>On this page</h2>'
        f'<ul><li class="toc-l2"><a href="#{single_prefix}top">Overview</a></li>{toc_html}</ul>'
        "</aside>"
    )
    mobile_toc = (
        ""
        if wide or not toc
        else '<details class="toc-mobile"><summary>On this page <span class="toc-current">Overview</span></summary>'
        f'<ul><li class="toc-l2"><a href="#{single_prefix}top">Overview</a></li>{toc_html}</ul>'
        "</details>"
    )
    home = concept.id == (kb.home_concept or kb.concepts[0].id)
    classes = "page" + (" is-wide" if wide else "") + (" is-home" if home else "")
    page_id = concept.id if ctx.single else "page"
    html = f"""<div class="{classes}" id="{_e(page_id)}" data-concept="{_e(concept.id)}"{" data-adaptive" if _is_adaptive(concept) else ""}>
<article class="doc" aria-labelledby="{single_prefix}top">
{mobile_toc}<header class="doc-header{" is-title-hidden" if concept.hide_title else ""}"><div class="journey-slot"></div><h1 id="{single_prefix}top">{_e(concept.title)}</h1>{lead}<div class="doc-meta">{_context_line(kb, info, ctx, single_prefix)}<div class="profile-slot"></div></div></header>
<div class="doc-body" data-view="complete">{body}</div>
<div class="next-slot"></div>
{_pagination(kb, concept, ctx)}
<footer class="doc-footer">{source}<span>Compiled from typed Python knowledge objects.</span></footer>
</article>{aside}
</div>"""
    sections = [(text, anchor) for level, anchor, text, _ in toc if level == 2]
    return _Page(concept, html, sections)


def _select(name: str, current: str) -> str:
    options = "".join(
        f'<option value="{value}"{" selected" if value == current else ""}>{_e(label)}</option>'
        for value, label in CONTEXT_LABELS[name].items()
    )
    return f'<select id="{name}" data-context="{name}">{options}</select>'


def _widgets(kb: KnowledgeBase, context: DocsContext) -> str:
    """Progressive enhancements mounted by the runtime; invisible without JavaScript."""
    profile = f"""<div id="profile" class="profile"><span id="profile-summary">Complete page</span>
<details class="profile-change"><summary>Tailor this page</summary><div class="profile-panel">
<label>I'm {_select("intent", context.intent.value)}</label>
<label>Experience {_select("experience", context.audience.experience.value)}</label>
<label>Show {_select("preference", context.audience.preference.value)}</label>
<label>Length {_select("depth", context.audience.depth.value)}</label>
<p>Only authored blocks are selected and reordered; nothing is generated.</p>
</div></details><button type="button" id="profile-complete" hidden>Show complete page</button></div>"""
    decision = (
        '<details id="decision" class="decision"><summary>Not sure where to start?</summary>'
        '<form id="journey-form" class="journey-form"><label for="journey-goal">Describe what '
        'you are trying to do</label><textarea id="journey-goal" rows="3" required '
        'placeholder="My agent returns valid JSON but the citations are made up"></textarea>'
        '<button type="submit">Suggest a page</button><p id="decision-status" role="status">'
        "A small model runs in your browser and chooses between authored pages.</p></form>"
        "</details>"
        if kb.decision
        else ""
    )
    return (
        f'<div id="widgets" hidden>{profile}{decision}'
        '<nav id="journey-strip" class="journey-strip" aria-label="Current journey"></nav>'
        '<section id="journey-next" class="journey-next" aria-live="polite"></section></div>'
    )


# --- Shared data ----------------------------------------------------------------


def _shared_payload(kb: KnowledgeBase, ctx: _Ctx, pages: list[_Page]) -> dict[str, object]:
    index = {c.id: i for i, c in enumerate(kb.concepts)}
    sections = [
        [index[page.concept.id], text, ctx.root_href(page.concept.id).split("#")[0] + "#" + anchor]
        for page in pages
        for text, anchor in page.sections
    ]
    return {
        "title": kb.title,
        "home": kb.home_concept or kb.concepts[0].id,
        "concepts": [
            {
                "id": c.id,
                "title": c.title,
                "summary": c.summary,
                "kind": c.kind.value,
                "domain": c.domain,
                "aliases": sorted(c.aliases),
                "show_ontology": c.show_ontology,
                "href": ctx.root_href(c.id),
            }
            for c in kb.concepts
        ],
        "sections": sections,
        "graph": graph_concepts(kb),
        "relationships": [r.model_dump(mode="json") for r in kb.relationships],
        "jobs": [j.model_dump(mode="json") for j in kb.jobs],
        "journeys": [j.model_dump(mode="json") for j in kb.journeys],
        "labels": CONTEXT_LABELS,
        "decision": kb.decision.model_dump(mode="json") if kb.decision else None,
    }


def _json(data: object) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


# --- Shell ----------------------------------------------------------------------

_MENU_ICON = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
_SEARCH_ICON = '<svg class="search-icon" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><circle cx="11" cy="11" r="6.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="m16 16 4 4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
_THEME_ICONS = (
    '<svg class="icon-moon" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5Z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg>'
    '<svg class="icon-sun" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5.3 5.3l1.6 1.6M17.1 17.1l1.6 1.6M5.3 18.7l1.6-1.6M17.1 6.9l1.6-1.6" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>'
)


def _brand_html(kb: KnowledgeBase, ctx: _Ctx) -> str:
    brand = kb.branding
    if brand.logo_svg:
        logo = f'<span class="logo logo-light">{brand.logo_svg}</span>'
        if brand.logo_svg_dark:
            logo += f'<span class="logo logo-dark">{brand.logo_svg_dark}</span>'
    else:
        logo = f'<span class="brand-word">{_e(brand.name)}</span>'
    return f'<a class="brand" href="{_e(ctx.home_href())}" aria-label="{_e(brand.name)} home">{logo}</a>'


def _product_nav(kb: KnowledgeBase) -> str:
    current = ' aria-current="true"'
    links = "".join(
        f'<a href="{_e(link.url)}"{current if link.current else ""}>{_e(link.label)}</a>'
        for link in kb.branding.links
    )
    return f'<nav class="product-nav" aria-label="Products">{links}</nav>' if links else ""


def _brand_style(kb: KnowledgeBase) -> str:
    brand = kb.branding
    return f":root{{--accent:{brand.accent};--brand-ink:{brand.ink}}}"


def _document(
    kb: KnowledgeBase,
    ctx: _Ctx,
    *,
    title: str,
    description: str,
    current: str | None,
    pages_html: str,
    shared_js: str,
    context: DocsContext,
    inline: bool,
) -> str:
    css = (
        f"<style>{CSS}</style>"
        if inline
        else f'<link rel="stylesheet" href="{ctx.prefix}assets/docs.css">'
    )
    js = (
        f"<script>{JS}</script>"
        if inline
        else f'<script src="{ctx.prefix}assets/docs.js"></script>'
    )
    decision = f"<script>{DECISION_JS}</script>" if kb.decision else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_e(title)}</title>
<meta name="description" content="{_e(description)}">
<meta name="generator" content="pydantic-knowledge">
<script>{THEME_SCRIPT}</script>
{css}
<style>{_brand_style(kb)}</style>
</head>
<body data-target="{ctx.target.value}" data-prefix="{_e(ctx.prefix)}" data-page="{_e(current or "")}">
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="header-inner">
<label class="menu-button" for="nav-toggle" aria-label="Toggle navigation">{_MENU_ICON}</label>
{_brand_html(kb, ctx)}{_product_nav(kb)}
<div class="header-tools"><button type="button" class="search-trigger" id="search-open" aria-haspopup="dialog" aria-label="Search the documentation">{_SEARCH_ICON}<span>Search</span><kbd>⌘K</kbd></button>
<button id="theme-toggle" class="icon-button theme-toggle" type="button" aria-label="Switch theme">{_THEME_ICONS}</button></div>
</div></header>
<input type="checkbox" id="nav-toggle" class="nav-toggle" aria-hidden="true" tabindex="-1">
<div class="layout">
<nav class="sidebar" id="sidebar" aria-label="Documentation">{_product_nav(kb).replace('class="product-nav"', 'class="product-nav mobile-products"')}{_nav_tree(_nav_items(kb), ctx, current)}</nav>
<main class="pages" id="main">{pages_html}</main>
</div>
<dialog id="search-dialog" class="search-dialog" aria-label="Search the documentation"><div class="sd-head">{_SEARCH_ICON}<input id="search" type="search" placeholder="Search the docs" aria-label="Search the documentation" autocomplete="off" aria-controls="search-results"><button type="button" class="sd-close" aria-label="Close search">&times;</button></div><div id="search-results" class="search-results" role="listbox" aria-label="Search results"><p class="empty">Search pages and sections by title.</p></div></dialog>
{_widgets(kb, context)}
{shared_js}
{js}
{decision}
</body>
</html>"""


def _render_pages(kb: KnowledgeBase, ctx: _Ctx) -> list[_Page]:
    known = {c.id for c in kb.concepts}
    return [_page(kb, concept, ctx, known) for concept in kb.concepts]


def render_html(kb: KnowledgeBase, *, context: DocsContext | None = None) -> str:
    """Render a self-contained single-file export; every page is readable without JS."""
    context = context or DocsContext()
    ctx = _Ctx(kb, BuildTarget.SINGLE)
    pages = _render_pages(kb, ctx)
    shared = (
        f"<script>window.PYDANTIC_KNOWLEDGE_DATA={_json(_shared_payload(kb, ctx, pages))};</script>"
    )
    return _document(
        kb,
        ctx,
        title=kb.title,
        description=kb.concept(kb.home_concept or kb.concepts[0].id).summary,
        current=None,
        pages_html="".join(page.html for page in pages),
        shared_js=shared,
        context=context,
        inline=True,
    )


def write_html(
    kb: KnowledgeBase, output: str | Path, *, context: DocsContext | None = None
) -> Path:
    """Write a self-contained single-file export."""
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_html(kb, context=context), encoding="utf-8")
    return path


def _prepare_dir(output: Path) -> None:
    """Refuse unowned nonempty folders; never recursively delete user files."""
    if output.exists():
        if not output.is_dir():
            raise ValueError(f"output path is a file: {output}")
        if any(output.iterdir()):
            manifest = output / "manifest.json"
            try:
                data = json.loads(manifest.read_text(encoding="utf-8"))
            except (OSError, ValueError) as exc:
                raise ValueError(f"refusing to build into nonempty folder: {output}") from exc
            if data.get("generator") != "pydantic-knowledge":
                raise ValueError(f"folder is not owned by pydantic-knowledge: {output}")
    output.mkdir(parents=True, exist_ok=True)


def write_site(
    kb: KnowledgeBase,
    output: str | Path,
    *,
    context: DocsContext | None = None,
    offline: bool = False,
) -> Path:
    """Write a multi-page static site.

    `offline=False` shares CSS, JS, and ontology data across pages for browser caching.
    `offline=True` embeds those assets into every HTML page so any page can be opened directly.
    """
    context = context or DocsContext()
    target = BuildTarget.OFFLINE if offline else BuildTarget.SITE
    root = Path(output)
    _prepare_dir(root)
    (root / "concepts").mkdir(exist_ok=True)

    def render(prefix: str, concepts: list[Concept]) -> list[_Page]:
        ctx = _Ctx(kb, target, prefix)
        known = {c.id for c in kb.concepts}
        return [_page(kb, c, ctx, known) for c in concepts]

    pages = render("../", list(kb.concepts))
    home_id = kb.home_concept or kb.concepts[0].id
    data = _json(_shared_payload(kb, _Ctx(kb, target), pages))
    if not offline:
        (root / "assets").mkdir(exist_ok=True)
        (root / "data").mkdir(exist_ok=True)
        (root / "assets" / "docs.css").write_text(CSS + "\n", encoding="utf-8")
        (root / "assets" / "docs.js").write_text(JS + "\n", encoding="utf-8")
        (root / "data" / "ontology.js").write_text(
            f"window.PYDANTIC_KNOWLEDGE_DATA={data};\n", encoding="utf-8"
        )

    def write(path: Path, page: _Page, prefix: str) -> None:
        ctx = _Ctx(kb, target, prefix)
        shared = (
            f"<script>window.PYDANTIC_KNOWLEDGE_DATA={data};</script>"
            if offline
            else f'<script src="{prefix}data/ontology.js"></script>'
        )
        concept = page.concept
        html = _document(
            kb,
            ctx,
            title=f"{concept.title} · {kb.title}",
            description=concept.summary or kb.title,
            current=concept.id,
            pages_html=page.html,
            shared_js=shared,
            context=context,
            inline=offline,
        )
        path.write_text(html, encoding="utf-8")

    for page in pages:
        write(root / "concepts" / f"{page.concept.id}.html", page, "../")
    (index_page,) = render("", [kb.concept(home_id)])
    write(root / "index.html", index_page, "")
    manifest = {
        "generator": "pydantic-knowledge",
        "title": kb.title,
        "target": target.value,
        "home": "index.html",
        "concepts": len(kb.concepts),
        "relationships": len(kb.relationships),
    }
    (root / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return root


def build(
    kb: KnowledgeBase,
    output: str | Path,
    *,
    target: BuildTarget | str = BuildTarget.SITE,
    context: DocsContext | None = None,
) -> Path:
    target = BuildTarget(target)
    if target is BuildTarget.SINGLE:
        path = Path(output)
        if path.suffix.lower() != ".html":
            path = path / "docs.html"
        return write_html(kb, path, context=context)
    return write_site(kb, output, context=context, offline=target is BuildTarget.OFFLINE)
