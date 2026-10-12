from __future__ import annotations

from pydantic_knowledge import (
    RelationKind,
    Role,
    build,
    concept,
    definition,
    docs,
    example_phrase,
    job,
    journey,
    ontology_projection,
    relates,
    step,
)
from pydantic_knowledge.ontology import concept_map, implementations


def knowledge(extra=()):
    def page(id, title, domain=None, role=Role.CONCEPT, family=None):
        return concept(
            id, title, f"About {title}.", definition(f"{id}.def", title),
            domain=domain, role=role, family=family,
        )

    pages = [
        page("start", "Start", role=Role.START),
        page("model", "Model", "Models"),
        page("provider", "Provider", "Models"),
        page("openai", "OpenAI", "Models", Role.INTEGRATION, "Providers"),
        page("ollama", "Ollama", "Models", Role.INTEGRATION, "Providers"),
        page("choosing", "Choosing a model", "Models", Role.GUIDE),
        page("api-models", "models", "Models", Role.REFERENCE),
        page("agent", "Agent", "Agents"),
        page("realtime", "Realtime", "Agents"),
        page("audio", "Audio", "Agents", Role.GUIDE, "Realtime"),
        page("ex", "Weather agent", role=Role.EXAMPLE, family="Getting started"),
        *extra,
    ]
    return docs(
        "Example",
        concepts=pages,
        relationships=[
            relates("agent", RelationKind.USES, "model"),
            relates("provider", RelationKind.PROVIDES, "model"),
            relates("agent", RelationKind.INSTANTIATES, "realtime"),
            relates("openai", RelationKind.IS_A, "provider"),
            relates("ollama", RelationKind.IS_A, "provider"),
        ],
        jobs=[job("pick", "Choose a model", "Pick one.", example_phrase("which model?"))],
        journeys=[journey("pick-path", "Picking", "pick", "Path.", step("model", "a"), step("provider", "b"))],
        domains=["Agents", "Models"],
        home="start",
    )


def labels(items):
    return [i.label for i in items]


def find(items, label):
    return next(i for i in items if i.label == label)


def test_sidebar_is_generated_from_domains_and_roles():
    nav = ontology_projection(knowledge()).items
    # Start pages, goals, then domains in declared order, then role-based tail groups.
    assert labels(nav) == ["Start", "By goal", "Agents", "Models", "Examples"]
    models = find(nav, "Models").children
    assert labels(models) == ["Model", "Provider", "Guides", "Providers", "API reference"]
    assert labels(find(models, "Providers").children) == ["OpenAI", "Ollama"]
    goals = find(nav, "By goal").children
    assert labels(goals) == ["Choose a model"]
    assert [i.concept_id for i in goals[0].children] == ["model", "provider"]


def test_concept_opens_the_group_of_the_same_name():
    agents = find(ontology_projection(knowledge()).items, "Agents").children
    assert labels(agents) == ["Agent", "Realtime"]
    realtime = find(agents, "Realtime")
    assert [i.concept_id for i in realtime.children] == ["realtime", "audio"]


def test_changing_the_model_changes_the_navigation():
    before = ontology_projection(knowledge()).items
    moved = concept("ollama-local", "Local models", "Local.", definition("l.def", "Local"),
                    domain="Agents", role=Role.GUIDE)
    after = ontology_projection(knowledge([moved])).items
    assert "Guides" not in labels(find(before, "Agents").children)
    assert "Guides" in labels(find(after, "Agents").children)


def test_map_shows_core_concepts_and_counts_implementations():
    kb = knowledge()
    graph = concept_map(kb)
    assert set(graph.nodes) == {"model", "provider", "agent", "realtime"}
    assert implementations(kb) == {"provider": ["openai", "ollama"]}


def test_implementation_pages_say_what_they_are(tmp_path):
    kb = knowledge()
    kb = kb.model_copy(update={"projections": (ontology_projection(kb),)})
    out = build(kb, tmp_path / "site")
    page = (out / "concepts" / "openai.html").read_text()
    assert "A kind of" in page and 'href="../concepts/provider.html">Provider</a>' in page
    provider = (out / "concepts" / "provider.html").read_text()
    assert "2 implementations" in provider
    # Only the canonical group of a page that appears twice is expanded.
    model = (out / "concepts" / "model.html").read_text()
    assert model.count("<details class=\"nav-group\" open>") == 1
    # Previous/next follow the domain order, not the goal shortcut that lists it first.
    assert 'rel="prev" href="../concepts/realtime.html"' in model or 'rel="prev" href="../concepts/audio.html"' in model


def test_notice_appears_above_the_header(tmp_path):
    from pydantic_knowledge.models import BrandLink

    kb = knowledge()
    branding = kb.branding.model_copy(
        update={"notice": "Unofficial <prototype>", "notice_link": BrandLink(label="Official", url="https://x.test/")}
    )
    out = build(kb.model_copy(update={"branding": branding}), tmp_path / "site")
    page = (out / "concepts" / "model.html").read_text()
    assert '<div class="site-notice" role="note">Unofficial &lt;prototype&gt; <a href="https://x.test/">Official</a></div>' in page
    assert page.index("site-notice") < page.index("<header")
