from pathlib import Path

import pytest
from pydantic import ValidationError

from pydantic_knowledge import (
    AudienceProfile,
    Branding,
    Experience,
    KnowledgeBase,
    build,
    chunk_markdown,
    concept,
    docs,
    import_markdown_directory,
    render_html,
)


def test_nonempty_output_is_never_deleted(tmp_path: Path):
    sentinel = tmp_path / "important.py"
    sentinel.write_text("keep me")
    with pytest.raises(ValueError, match="nonempty"):
        build(docs("Demo", concepts=[concept("demo", "Demo", "Demo")]), tmp_path)
    assert sentinel.read_text() == "keep me"


def test_rebuild_preserves_unrelated_files(tmp_path: Path):
    knowledge = docs("Demo", concepts=[concept("demo", "Demo", "Demo")])
    build(knowledge, tmp_path / "site")
    sentinel = tmp_path / "site" / "notes.txt"
    sentinel.write_text("keep me")
    build(knowledge, tmp_path / "site")
    assert sentinel.read_text() == "keep me"


def test_library_has_no_example_branding():
    html = render_html(
        docs("Example", concepts=[concept("demo", "Demo", "Demo")], branding=Branding(name="Acme"))
    )
    assert "Acme" in html
    assert "Pydantic AI" not in html
    assert "Explore connections" not in html
    assert "fetch(" not in html


def test_heading_chunks_preserve_content_and_code():
    source = "Intro\n\n## First\nText\n```python\n## not a section\nx = 1\n```\n### Subsection\nMore\n## Second\nEnd\n"
    chunks = chunk_markdown(source)
    assert [title for title, _ in chunks] == ["Introduction", "First", "Second"]
    assert "".join(body for _, body in chunks) == source
    assert "### Subsection" in chunks[1][1]


def test_imported_markdown_keeps_complete_sections_and_links(tmp_path: Path):
    (tmp_path / "one.md").write_text(
        "# One\nIntro\n\n## Detailed\n[Two](two.md)\n```python\nx = 1\n```\n"
    )
    (tmp_path / "two.md").write_text("# Two\nEvery detail.\n")
    pages = import_markdown_directory(tmp_path, base_url="https://example.org/docs/")
    first = next(c for c in pages if c.title == "One")
    assert len(first.blocks) == 2
    assert "knowledge:reference-two" in first.blocks[1].body
    html = render_html(docs("Demo", concepts=pages))
    assert "Detailed" in html
    assert "x = 1" in first.blocks[1].body


def test_audience_is_generic_with_compatible_inputs():
    assert AudienceProfile(experience=Experience.EXPERT).experience is Experience.EXPERT
    assert AudienceProfile(pydantic_ai=Experience.EXPERT).experience is Experience.EXPERT


def test_unsafe_ids_and_empty_knowledge_are_rejected():
    with pytest.raises(ValidationError):
        concept("../escape", "Escape", "Escape")
    with pytest.raises(ValidationError):
        KnowledgeBase(title="Empty", concepts=())


def test_imported_markdown_scripts_are_inert(tmp_path: Path):
    (tmp_path / "page.md").write_text("# Page\nText\n\n<script>fetch('/x')</script>\n")
    html = render_html(docs("Demo", concepts=import_markdown_directory(tmp_path, base_url="x/")))
    assert "fetch('/x')" not in html
    assert "Text" in html
