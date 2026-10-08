"""Navigation generated from the ontology: the sidebar is a projection, never a source.

Layout of the generated projection:

    start pages                      (Role.START, flat, in authored order)
    <goals label>                    one group per job, listing its journey's steps
    <domain> ...                     in KnowledgeBase.domains order, then any others
        core concepts                (Role.CONCEPT)
        Guides                       (Role.GUIDE without a family)
        <family> ...                 guide and integration families; "A / B" nests
        API reference                (Role.REFERENCE)
    Examples, Reference, Project     pages of those roles without a domain
"""

from __future__ import annotations

from .models import Concept, KnowledgeBase, NavItem, Projection, Role


def _leaf(concept: Concept) -> NavItem:
    return NavItem(label=concept.title, concept_id=concept.id)


def _families(concepts: list[Concept], ungrouped: str | dict | None) -> list[NavItem]:
    """Group pages by family, nesting on " / ".

    Pages without a family go under `ungrouped`: one label, a label per role, or flat.
    """
    tree: dict = {}
    loose: dict[str | None, list[Concept]] = {}
    for concept in concepts:
        if not concept.family:
            label = ungrouped.get(concept.role) if isinstance(ungrouped, dict) else ungrouped
            loose.setdefault(label, []).append(concept)
            continue
        node = tree
        for part in (p.strip() for p in concept.family.split("/")):
            node = node.setdefault(part, {})
        node.setdefault("", []).append(concept)

    def build(node: dict) -> list[NavItem]:
        items = [_leaf(c) for c in node.get("", [])]
        for label, child in node.items():
            if label:
                items.append(NavItem(label=label, children=tuple(build(child))))
        return items

    items = []
    for label, pages in loose.items():
        if label:
            items.append(NavItem(label=label, children=tuple(_leaf(c) for c in pages)))
        else:
            items += [_leaf(c) for c in pages]
    return items + build(tree)


def ontology_projection(
    kb: KnowledgeBase,
    *,
    id: str = "ontology",
    title: str = "Documentation",
    goals_label: str = "By goal",
    tail: tuple[tuple[Role, str], ...] = (
        (Role.EXAMPLE, "Examples"),
        (Role.REFERENCE, "Reference"),
        (Role.PROJECT, "Project"),
    ),
) -> Projection:
    pages = [c for c in kb.concepts if not c.show_ontology]
    items: list[NavItem] = [_leaf(c) for c in pages if c.role is Role.START]

    goals = []
    for job in kb.jobs:
        journey = next((j for j in kb.journeys if j.job_id == job.id), None)
        steps = [s.concept_id for s in journey.steps] if journey else list(job.expected_concepts)
        if steps:
            titles = {c.id: c.title for c in kb.concepts}
            children = tuple(NavItem(label=titles[s], concept_id=s) for s in dict.fromkeys(steps))
            goals.append(NavItem(label=job.title, children=children))
    if goals:
        items.append(NavItem(label=goals_label, children=tuple(goals)))

    domained = [c for c in pages if c.domain and c.role is not Role.START]
    order = list(kb.domains) + [d for d in dict.fromkeys(c.domain for c in domained) if d not in kb.domains]
    for domain in order:
        members = [c for c in domained if c.domain == domain]
        if not members:
            continue
        concepts = [c for c in members if c.role is Role.CONCEPT]
        # Guides and integrations of one family share a group, guides first.
        practical = [c for c in members if c.role is Role.GUIDE] + [
            c for c in members if c.role is Role.INTEGRATION
        ]
        groups = _families(practical, {Role.GUIDE: "Guides", Role.INTEGRATION: "Integrations"})
        # A concept with a group of the same name opens that group instead of standing apart.
        titled = {c.title: c for c in concepts}
        folded = set()
        for i, item in enumerate(groups):
            if item.children and item.label in titled:
                concept = titled[item.label]
                folded.add(concept.id)
                groups[i] = NavItem(label=item.label, children=(_leaf(concept), *item.children))
        children = [_leaf(c) for c in concepts if c.id not in folded] + groups
        children += _families([c for c in members if c.role is Role.EXAMPLE], "Examples")
        reference = [c for c in members if c.role in (Role.REFERENCE, Role.PROJECT)]
        if reference:
            children.append(NavItem(label="API reference", children=tuple(_leaf(c) for c in reference)))
        items.append(NavItem(label=domain, children=tuple(children)))

    for role, label in tail:
        rest = [c for c in pages if c.role is role and not c.domain]
        if rest:
            items.append(NavItem(label=label, children=tuple(_families(rest, None))))
    leftovers = [c for c in pages if not c.domain and c.role not in {r for r, _ in tail} | {Role.START}]
    if leftovers:
        items.append(NavItem(label="More", children=tuple(_leaf(c) for c in leftovers)))
    about = [c for c in kb.concepts if c.show_ontology]
    items += [_leaf(c) for c in about]
    return Projection(id=id, title=title, items=tuple(items))
