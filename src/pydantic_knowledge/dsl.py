from __future__ import annotations

from collections.abc import Iterable

from .models import (
    Branding,
    Concept,
    ConceptKind,
    JobExample,
    JobToBeDone,
    JourneyStep,
    KnowledgeBase,
    KnowledgeBlock,
    NavItem,
    Projection,
    RelationKind,
    Relationship,
    Role,
    UserJourney,
)


def concept(
    id: str,
    title: str,
    summary: str,
    *blocks: KnowledgeBlock,
    kind: ConceptKind = ConceptKind.CONCEPT,
    aliases: Iterable[str] = (),
    source_url: str | None = None,
    domain: str | None = None,
    show_ontology: bool = False,
    role: Role = Role.CONCEPT,
    family: str | None = None,
) -> Concept:
    return Concept(
        id=id,
        title=title,
        summary=summary,
        kind=kind,
        aliases=frozenset(aliases),
        blocks=blocks,
        source_url=source_url,
        domain=domain,
        show_ontology=show_ontology,
        role=role,
        family=family,
    )


def relates(
    source: str,
    kind: RelationKind,
    target: str,
    *,
    label: str | None = None,
    route_when: str | None = None,
    weight: int = 0,
) -> Relationship:
    return Relationship(
        source=source,
        target=target,
        kind=kind,
        label=label,
        route_when=route_when,
        weight=weight,
    )


def example_phrase(
    phrase: str,
    *,
    expected: Iterable[str] = (),
    answer_must_contain: Iterable[str] = (),
    answer_must_not_contain: Iterable[str] = (),
    current: str | None = None,
) -> JobExample:
    return JobExample(
        phrase=phrase,
        expected_concepts=tuple(expected),
        answer_must_contain=tuple(answer_must_contain),
        answer_must_not_contain=tuple(answer_must_not_contain),
        current_concept=current,
    )


def job(
    id: str,
    title: str,
    outcome: str,
    *examples: JobExample,
    expected: Iterable[str] = (),
) -> JobToBeDone:
    assert examples, "a job must include at least one example phrase"
    return JobToBeDone(
        id=id,
        title=title,
        outcome=outcome,
        examples=examples,
        expected_concepts=tuple(expected),
    )


def step(concept_id: str, reason: str) -> JourneyStep:
    return JourneyStep(concept_id=concept_id, reason=reason)


def journey(id: str, title: str, job_id: str, summary: str, *steps: JourneyStep) -> UserJourney:
    assert steps, "a journey must contain at least one step"
    return UserJourney(id=id, title=title, job_id=job_id, summary=summary, steps=steps)


def nav(label: str, concept_id: str) -> NavItem:
    return NavItem(label=label, concept_id=concept_id)


def group(label: str, *items: NavItem) -> NavItem:
    assert items, "a navigation group must contain at least one item"
    return NavItem(label=label, children=items)


def projection(id: str, title: str, *items: NavItem) -> Projection:
    return Projection(id=id, title=title, items=items)


def docs(
    title: str,
    *,
    concepts: Iterable[Concept],
    relationships: Iterable[Relationship] = (),
    projections: Iterable[Projection] = (),
    jobs: Iterable[JobToBeDone] = (),
    journeys: Iterable[UserJourney] = (),
    branding: Branding | None = None,
    home: str | None = None,
    domains: Iterable[str] = (),
) -> KnowledgeBase:
    return KnowledgeBase(
        title=title,
        concepts=tuple(concepts),
        relationships=tuple(relationships),
        projections=tuple(projections),
        jobs=tuple(jobs),
        journeys=tuple(journeys),
        branding=branding or Branding(name=title),
        home_concept=home,
        domains=tuple(domains),
    )
