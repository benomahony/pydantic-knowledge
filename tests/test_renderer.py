from __future__ import annotations

import json
from pathlib import Path

from pydantic_knowledge import (
    BuildTarget,
    RelationKind,
    build,
    concept,
    definition,
    docs,
    example_phrase,
    job,
    journey,
    nav,
    projection,
    relates,
    render_html,
    step,
)
from pydantic_knowledge.ontology import concept_map


def kb():
    a = concept("a", "A", "Summary A", definition("a.def", "Definition A"))
    b = concept("b", "B", "Summary B", definition("b.def", "Definition B"))
    return docs(
        "Example",
        concepts=[a, b],
        relationships=[relates("a", RelationKind.USES, "b")],
        projections=[projection("main", "Main", nav("A", "a"), nav("B", "b"))],
        home="a",
    )


def test_renderer_outputs_single_static_html() -> None:
    html = render_html(kb())
    assert html.startswith("<!doctype html>")
    assert "PYDANTIC_KNOWLEDGE_DATA" in html
    assert "fetch(" not in html
    assert "<script src=" not in html
    assert "Definition A" in html


def test_site_is_default_and_splits_shared_assets(tmp_path: Path) -> None:
    out = build(kb(), tmp_path / "site")
    assert out == tmp_path / "site"
    assert (out / "index.html").exists()
    assert (out / "concepts" / "a.html").exists()
    assert (out / "concepts" / "b.html").exists()
    assert (out / "assets" / "docs.css").exists()
    assert (out / "assets" / "docs.js").exists()
    assert (out / "data" / "ontology.js").exists()
    page = (out / "concepts" / "a.html").read_text()
    assert "../assets/docs.css" in page
    assert "../data/ontology.js" in page
    assert "Definition A" in page


def test_offline_target_embeds_runtime_data_in_each_page(tmp_path: Path) -> None:
    out = build(kb(), tmp_path / "offline", target=BuildTarget.OFFLINE)
    page = (out / "concepts" / "a.html").read_text()
    assert "<script src=" not in page
    assert '<link rel="stylesheet"' not in page
    assert "PYDANTIC_KNOWLEDGE_DATA" in page
    assert "Definition A" in page
    assert not (out / "assets").exists()


def test_single_target_remains_explicit_export(tmp_path: Path) -> None:
    out = build(kb(), tmp_path / "demo.html", target="single")
    assert out == tmp_path / "demo.html"
    assert out.exists()
    assert "<script src=" not in out.read_text()


def test_manifest_describes_build(tmp_path: Path) -> None:
    out = build(kb(), tmp_path / "site")
    manifest = json.loads((out / "manifest.json").read_text())
    assert manifest == {
        "generator": "pydantic-knowledge",
        "title": "Example",
        "target": "site",
        "home": "index.html",
        "concepts": 2,
        "relationships": 1,
    }


def _mapped_knowledge(extra_relationships=()):
    a = concept("a", "A", "Summary A", definition("a.def", "Definition A"), domain="Domain one")
    b = concept("b", "B", "Summary B", definition("b.def", "Definition B"), domain="Domain two")
    c = concept("c", "C", "Summary C", definition("c.def", "Definition C"), domain="Domain two")
    about = concept(
        "about",
        "How these docs are organised",
        "The reader map.",
        definition("about.def", "About"),
        show_ontology=True,
    )
    return docs(
        "Example",
        concepts=[about, a, b, c],
        relationships=[
            relates("a", RelationKind.USES, "b", label="uses"),
            *extra_relationships,
        ],
        projections=[
            projection(
                "main", "Main", nav("About", "about"), nav("A", "a"), nav("B", "b"), nav("C", "c")
            )
        ],
        jobs=[job("j", "Do the thing", "Outcome.", example_phrase("help me", expected=["a"]))],
        journeys=[journey("p", "Path", "j", "Summary.", step("a", "First."), step("b", "Then."))],
        home="a",
        domains=["Domain two", "Domain one"],
    )


def test_ontology_page_is_live_view_of_knowledge_base(tmp_path: Path) -> None:
    out = build(_mapped_knowledge(), tmp_path / "site")
    about_page = (out / "concepts" / "about.html").read_text()
    normal_page = (out / "concepts" / "a.html").read_text()
    ontology_data = (out / "data" / "ontology.js").read_text()

    # The concept map is static SVG generated from the knowledge base.
    assert "data-ontology" in about_page and 'class="o-svg"' in about_page
    assert 'data-source="a" data-target="b"' in about_page
    assert 'data-ontology' not in normal_page
    assert 'class="o-job" data-job="j"' in about_page
    assert 'class="o-journey" data-journey="p"' in about_page
    assert "Jobs to be Done" in about_page and "1 job" in about_page
    # Ordinary concept pages show where they sit in the model.
    assert "In the ontology" in normal_page
    assert '"source":"a"' in ontology_data and '"label":"uses"' in ontology_data


def test_graph_follows_the_python_model(tmp_path: Path) -> None:
    before = render_html(_mapped_knowledge())
    after = render_html(
        _mapped_knowledge([relates("c", RelationKind.DEPENDS_ON, "a", label="needs")])
    )
    assert 'data-source="c" data-target="a"' not in before
    assert 'data-source="c" data-target="a"' in after
    # Geography is stable: new edges between mapped concepts never move them.
    graph_a, graph_b = concept_map(_mapped_knowledge()), concept_map(
        _mapped_knowledge([relates("b", RelationKind.DEPENDS_ON, "a")])
    )
    assert graph_a.nodes == graph_b.nodes
    # Declared domain order controls placement; the hub sits apart in the centre.
    assert graph_a.hub == "a"
    assert graph_a.domains[0].name == "Domain two"


def test_pages_are_readable_without_javascript(tmp_path: Path) -> None:
    out = build(_mapped_knowledge(), tmp_path / "site")
    page = (out / "concepts" / "b.html").read_text()
    assert "Definition B" in page
    assert '<a class="nav-link" href="../concepts/a.html" data-concept="a">A</a>' in page
    assert 'aria-current="page">B</a>' in page
    assert "<title>B · Example</title>" in page
    assert '<meta name="description" content="Summary B">' in page
    assert 'rel="prev" href="../concepts/a.html"' in page


def test_single_file_pages_work_without_javascript() -> None:
    html = render_html(_mapped_knowledge())
    assert '<div class="page is-home" id="a" data-concept="a"' in html
    assert 'id="b--top"' in html
    assert 'href="#b"' in html
    assert ".page:target" in html
    assert 'data-id="a"' in html and 'data-id="about--a"' not in html
    assert 'id="about--o-arrow"' in html and "url(#about--o-arrow)" in html
