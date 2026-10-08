# pydantic-knowledge

A Python library for authored, typed documentation: concepts, knowledge blocks,
relationships, navigation, user journeys, and routing evaluations.

Pydantic AI is the worked example. Its logo, product links, documentation corpus,
and decision-model configuration live under `examples/`; the library works with
other subjects and brands.

**For the Pydantic team:** [docs/explainer.md](docs/explainer.md) covers what the prototype
does to the Pydantic AI docs and why, with screenshots against the live site.

## Install and run

```bash
uv sync --extra dev --extra evals
uv run pydantic-knowledge build examples/pydantic_ai_docs.py --out site
python -m http.server --directory site
```

Open the server URL to read the example. Light and dark modes are supported.

```bash
# Portable exports
uv run pydantic-knowledge build examples/pydantic_ai_docs.py --target offline --out outputs/offline
uv run pydantic-knowledge build examples/pydantic_ai_docs.py --target single --out outputs/pydantic-ai-single.html

# Routing and answer-content evaluations
uv run pydantic-knowledge eval examples/pydantic_ai_docs.py --out outputs/evals
uv run python examples/eval_docs.py

# Development checks
uv run pytest
uv run ruff check src tests examples/pydantic_ai_docs.py examples/eval_docs.py
```

## Author a knowledge base

```python
from pydantic_knowledge import (
    Branding, RelationKind, concept, definition, docs, example, relates,
)

request = concept(
    "request", "Request", "An incoming request.",
    definition("request.definition", "A request carries input to a service."),
    example("request.example", "response = service.handle(request)"),
)
response = concept(
    "response", "Response", "The result returned by the service.",
    definition("response.definition", "A response carries the service result."),
)
DOCS = docs(
    "Service documentation", concepts=[request, response],
    relationships=[relates("request", RelationKind.PRODUCES, "response")],
    branding=Branding(name="Service docs"), home="request",
)
```

Save this as `docs.py`, then run `uv run pydantic-knowledge build docs.py --out site`.
The CLI executes the authoring module; use authoring files you trust.

## Navigation is generated from the ontology

Give each concept a `domain`, a `role` (`Role.CONCEPT`, `GUIDE`, `INTEGRATION`, `REFERENCE`,
`EXAMPLE`, `PROJECT`, `START`) and optionally a `family` (`"A / B"` nests). Then:

```python
from pydantic_knowledge import ontology_projection

DOCS = DOCS.model_copy(update={"projections": (ontology_projection(DOCS),)})
```

Each domain lists its core concepts, then guides and integrations by family, then its API
reference. Jobs appear first as goal entry points. `is_a`/`provides` links from integrations
to a concept become counts on the concept map and "a kind of" context on each page.

## Complete documentation and heading chunks

```python
from pydantic_knowledge import docs, import_markdown_directory

pages = import_markdown_directory("content", base_url="https://example.org/docs/")
DOCS = docs("My documentation", concepts=pages)
```

Imported pages split at H2 headings. A heading and its H3–H6 subsections remain
together; fenced code is never split on a heading-looking line. Every section
retains its source prose and code. No summarisation or generated factual prose
occurs. `chunk_markdown(text, heading_level=2)` exposes the same lossless splitter.

The complete page is the default browser view and displays all its chunks in
source order. The explicitly selected tailored view filters authored blocks
using intent, experience, preference, and depth. `AudienceProfile.experience` and
`domain_experience` are subject-independent; the old constructor inputs
`pydantic_ai` and `ai_engineering` remain accepted as compatibility aliases.

## Local decision AI

`KnowledgeBase.decision` enables browser-local TAMEV Nano routing. It is optional;
ordinary navigation and search work without it. The model chooses among existing
concepts using the goal, journey, experience, and authored relationship hints.
It does not rewrite or summarise documentation.

The Pydantic AI example enables it with `DecisionConfig`. Model/runtime assets
are downloaded on the first journey; inference runs locally. A loading or
inference failure is reported explicitly. Offline exports retain all readable
content, but first-time AI loading needs a network connection.

Successful model loading does not establish routing quality. The deterministic
baseline and native Pydantic Evals reports record routing and answer assertions;
failed benchmark assertions are retained. The AI ship gate remains unapproved
until a scored AI experiment beats the baseline.

## Pydantic AI example snapshot

`examples/pydantic_ai_content/` contains the complete Markdown corpus from the
local upstream checkout, with its upstream licence. `examples/SNAPSHOT.json`
records the original Markdown checksums. API directives are expanded from local
source signatures and docstrings without executing upstream modules. The
curated blocks from the earlier adaptive prototype are retained separately in
`examples/assets/adaptive-content.json`.

This is a source snapshot, not a continuously updated mirror. The custom renderer
supports headings, code, tables, callouts, tabs, and internal links. Upstream
site-specific interactive media may still link to the upstream site.

## Project structure

```text
src/pydantic_knowledge/   models, authoring DSL, composition, routing, importer,
                         compiler, CLI, evaluations, and packaged browser assets
examples/                Pydantic AI authoring model, source corpus, and eval task
tests/                   model, rendering, composition, and recovery safeguards
site/                    generated multi-page example (ignored by Git)
outputs/                 portable exports and evaluation artifacts (ignored)
```

Builds refuse an unowned, nonempty destination. Rebuilding an owned output folder
updates generated files without recursively deleting the directory or unrelated
files. Use separate output folders for the site and offline targets. If an old
prototype folder has no generator marker, build to a new empty directory.
