from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class Intent(StrEnum):
    LEARN = "learn"
    BUILD = "build"
    FIX = "fix"
    CHOOSE = "choose"
    MIGRATE = "migrate"
    TEST = "test"
    OPERATE = "operate"
    EXTEND = "extend"
    REFERENCE = "reference"


class Experience(StrEnum):
    NEW = "new"
    FAMILIAR = "familiar"
    EXPERT = "expert"


class Preference(StrEnum):
    CODE_FIRST = "code_first"
    EXPLANATION_FIRST = "explanation_first"
    REFERENCE = "reference"


class Depth(StrEnum):
    QUICK = "quick"
    NORMAL = "normal"
    DEEP = "deep"


class BlockKind(StrEnum):
    DEFINITION = "definition"
    MENTAL_MODEL = "mental_model"
    EXAMPLE = "example"
    PROCEDURE = "procedure"
    TRADEOFF = "tradeoff"
    FAILURE = "failure"
    REFERENCE = "reference"
    NOTE = "note"


class ConceptKind(StrEnum):
    CONCEPT = "concept"
    ABSTRACTION = "abstraction"
    RUNTIME = "runtime"
    PROVIDER = "provider"
    PRODUCT = "product"
    INTERFACE = "interface"
    ASSURANCE = "assurance"


class Role(StrEnum):
    """What a page does for the reader; independent of its place in the ontology."""

    START = "start"
    CONCEPT = "concept"
    GUIDE = "guide"
    INTEGRATION = "integration"
    REFERENCE = "reference"
    EXAMPLE = "example"
    PROJECT = "project"


class RelationKind(StrEnum):
    IS_A = "is_a"
    HAS = "has"
    USES = "uses"
    PROVIDES = "provides"
    CONTRIBUTES = "contributes"
    CONTAINS = "contains"
    INSTANTIATES = "instantiates"
    PRODUCES = "produces"
    RECORDS = "records"
    EMITS = "emits"
    PERSISTS = "persists"
    RESUMES = "resumes"
    OBSERVES = "observes"
    EVALUATES = "evaluates"
    ORCHESTRATES = "orchestrates"
    DEPENDS_ON = "depends_on"
    RELATED_TO = "related_to"


class AudienceProfile(StrictModel):
    experience: Experience = Field(
        default=Experience.FAMILIAR, validation_alias=AliasChoices("experience", "pydantic_ai")
    )
    domain_experience: Experience = Field(
        default=Experience.FAMILIAR,
        validation_alias=AliasChoices("domain_experience", "ai_engineering"),
    )
    preference: Preference = Preference.EXPLANATION_FIRST
    depth: Depth = Depth.QUICK


class DocsContext(StrictModel):
    intent: Intent = Intent.LEARN
    audience: AudienceProfile = Field(default_factory=AudienceProfile)
    runtime: frozenset[str] = frozenset()
    constraints: frozenset[str] = frozenset()


class KnowledgeBlock(StrictModel):
    id: str
    kind: BlockKind
    title: str | None = None
    body: str
    language: str | None = None
    format: Literal["text", "markdown"] = "text"
    intents: frozenset[Intent] = frozenset()
    experiences: frozenset[Experience] = frozenset()
    preferences: frozenset[Preference] = frozenset()
    depths: frozenset[Depth] = frozenset()
    weight: int = Field(default=0, ge=-100, le=100)

    def score(self, context: DocsContext) -> int:
        score = self.weight
        if self.intents:
            score += 8 if context.intent in self.intents else -20
        if self.experiences:
            score += 4 if context.audience.experience in self.experiences else -4
        if self.preferences:
            score += 3 if context.audience.preference in self.preferences else -2
        if self.depths:
            score += 3 if context.audience.depth in self.depths else -2
        return score


class Relationship(StrictModel):
    source: str
    target: str
    kind: RelationKind
    label: str | None = None
    route_when: str | None = None
    weight: int = Field(default=0, ge=-100, le=100)


class Concept(StrictModel):
    id: str = Field(pattern=r"^[a-zA-Z0-9][a-zA-Z0-9_-]*$")
    title: str
    summary: str
    kind: ConceptKind = ConceptKind.CONCEPT
    aliases: frozenset[str] = frozenset()
    blocks: tuple[KnowledgeBlock, ...] = ()
    source_url: str | None = None
    domain: str | None = None
    show_ontology: bool = False
    hide_title: bool = False
    """Keep the title for assistive technology and search, but do not show it."""
    role: Role = Role.CONCEPT
    family: str | None = None
    """Grouping within a role, e.g. "Providers"; "A / B" nests B inside A in navigation."""

    def with_blocks(self, *blocks: KnowledgeBlock) -> Concept:
        return self.model_copy(update={"blocks": (*self.blocks, *blocks)})


class JobExample(StrictModel):
    phrase: str
    expected_concepts: tuple[str, ...] = ()
    answer_must_contain: tuple[str, ...] = ()
    answer_must_not_contain: tuple[str, ...] = ()
    current_concept: str | None = None


class JobToBeDone(StrictModel):
    id: str
    title: str
    outcome: str
    examples: tuple[JobExample, ...]
    expected_concepts: tuple[str, ...] = ()


class JourneyStep(StrictModel):
    concept_id: str
    reason: str


class UserJourney(StrictModel):
    id: str
    title: str
    job_id: str
    summary: str
    steps: tuple[JourneyStep, ...]


class NavItem(StrictModel):
    label: str
    concept_id: str | None = None
    children: tuple[NavItem, ...] = ()

    @model_validator(mode="after")
    def leaf_or_group(self) -> NavItem:
        if not (self.concept_id is not None or self.children):
            raise ValueError("nav item must target a concept or contain children")
        return self


class Projection(StrictModel):
    id: str
    title: str
    items: tuple[NavItem, ...]


class BrandLink(StrictModel):
    label: str
    url: str
    current: bool = False


class Branding(StrictModel):
    name: str
    accent: str = "#E520E9"
    ink: str = "#061314"
    paper: str = "#ffffff"
    logo_svg: str | None = None
    logo_svg_dark: str | None = None
    links: tuple[BrandLink, ...] = ()
    # A one-line notice above the header, e.g. to mark an unofficial build.
    notice: str | None = None
    notice_link: BrandLink | None = None


class DecisionConfig(StrictModel):
    """Optional browser-local routing; factual content always remains authored."""

    model_base: str = "https://huggingface.co/Tamkimd/tamev-nano-tinybert/resolve/main"
    runtime_url: str = "https://cdn.jsdelivr.net/npm/onnxruntime-web@1.30.0/dist/ort.min.js"
    wasm_path: str = "https://cdn.jsdelivr.net/npm/onnxruntime-web@1.30.0/dist/"
    entry_concepts: tuple[str, ...] = ()


class KnowledgeBase(StrictModel):
    title: str
    concepts: tuple[Concept, ...] = Field(min_length=1)
    relationships: tuple[Relationship, ...] = ()
    projections: tuple[Projection, ...] = ()
    jobs: tuple[JobToBeDone, ...] = ()
    journeys: tuple[UserJourney, ...] = ()
    branding: Branding = Field(default_factory=lambda: Branding(name="Docs"))
    domains: tuple[str, ...] = ()
    """Preferred placement order of ontology domains in diagrams; others follow."""
    home_concept: str | None = None
    decision: DecisionConfig | None = None

    @model_validator(mode="after")
    def validate_graph(self) -> KnowledgeBase:
        ids = [c.id for c in self.concepts]
        if not (len(ids) == len(set(ids))):
            raise ValueError("concept IDs must be unique")
        known = set(ids)
        for relation in self.relationships:
            if relation.source not in known:
                raise ValueError(f"unknown relation source: {relation.source}")
            if relation.target not in known:
                raise ValueError(f"unknown relation target: {relation.target}")
        for projection in self.projections:
            self._check_nav(projection.items, known)
        if len(self.domains) != len(set(self.domains)):
            raise ValueError("domains must be unique")
        if self.home_concept is not None and self.home_concept not in known:
            raise ValueError("home concept must exist")

        job_ids = [j.id for j in self.jobs]
        if not (len(job_ids) == len(set(job_ids))):
            raise ValueError("job IDs must be unique")
        known_jobs = set(job_ids)
        for job in self.jobs:
            for concept_id in job.expected_concepts:
                if concept_id not in known:
                    raise ValueError(f"unknown job expected concept: {concept_id}")
            for example in job.examples:
                if example.current_concept is not None and example.current_concept not in known:
                    raise ValueError(f"unknown example current concept: {example.current_concept}")
                for concept_id in example.expected_concepts:
                    if concept_id not in known:
                        raise ValueError(f"unknown example expected concept: {concept_id}")
        journey_ids = [j.id for j in self.journeys]
        if not (len(journey_ids) == len(set(journey_ids))):
            raise ValueError("journey IDs must be unique")
        for journey in self.journeys:
            if journey.job_id not in known_jobs:
                raise ValueError(f"unknown journey job: {journey.job_id}")
            for step in journey.steps:
                if step.concept_id not in known:
                    raise ValueError(f"unknown journey concept: {step.concept_id}")
        return self

    @staticmethod
    def _check_nav(items: tuple[NavItem, ...], known: set[str]) -> None:
        for item in items:
            if item.concept_id is not None and item.concept_id not in known:
                raise ValueError(f"unknown nav concept: {item.concept_id}")
            KnowledgeBase._check_nav(item.children, known)

    def concept(self, concept_id: str) -> Concept:
        for concept in self.concepts:
            if concept.id == concept_id:
                return concept
        raise KeyError(concept_id)

    def job(self, job_id: str) -> JobToBeDone:
        for job in self.jobs:
            if job.id == job_id:
                return job
        raise KeyError(job_id)


LiteralPreference = Literal["code_first", "explanation_first", "reference"]
