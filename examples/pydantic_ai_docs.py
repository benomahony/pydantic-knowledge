"""Pydantic AI documentation example; the library itself is domain independent."""

import json
from pathlib import Path

import yaml

from pydantic_knowledge import (
    BlockKind,
    Branding,
    BrandLink,
    Concept,
    ConceptKind,
    DecisionConfig,
    Experience,
    Intent,
    KnowledgeBlock,
    Preference,
    RelationKind,
    Relationship,
    Role,
    concept,
    definition,
    docs,
    example,
    example_phrase,
    failure,
    group,
    import_markdown_directory,
    job,
    journey,
    mental_model,
    nav,
    note,
    ontology_projection,
    projection,
    reference,
    relates,
    step,
)

about_docs = concept(
    "how-docs-are-organised",
    "How these docs are organised",
    "The knowledge model underneath these pages, and where AI is and is not used.",
    definition(
        "how-docs.principle",
        "These docs have an ontology underneath them rather than treating the sidebar as the "
        "source of truth. Every page is placed once: in a domain, with a role (concept, guide, "
        "integration, reference) and typed relationships to the concepts it explains. The "
        "sidebar is generated from those placements: core concepts first in each domain, then "
        "their guides and integrations, then API reference. The upstream order is kept only as "
        "a second projection.\n\n"
        "Integrations stay out of the way until you need them. Provider pages are kinds "
        "of Provider; durable backends are kinds of Durable Execution; harness capabilities "
        "are kinds of Capability. The map shows them as counts on the concept they "
        "implement, and each of their pages says what it is a kind of.\n\n"
        "Because the structure is explicit Python, it can be checked, rendered and evaluated. "
        "The map below is drawn from the same objects the compiler uses to build these pages; "
        "change the ontology, rebuild, and the map changes with it.",
        title="An ontology, not a sidebar",
        weight=10,
    ),
    mental_model(
        "how-docs.layers",
        "Jobs to be Done describe why someone arrives. User journeys realise a job as an "
        "ordered route through concepts, with a reason for each step. The ontology connects "
        "those concepts with typed relationships. Authored knowledge blocks hold the facts. "
        "Contextual composition selects and orders those blocks for the reader's intent, "
        "experience, style and depth.\n\n"
        "Each layer is optional and independent of the visual design. Navigation, search, "
        "journeys and the concept map are all views over the same knowledge base.",
        title="Reading the layers",
        weight=9,
    ),
    note(
        "how-docs.ai",
        "AI does not write the documentation. Every sentence and code sample on these pages "
        "was authored by people.\n\n"
        "AI is used only where there is genuine uncertainty: inferring what a reader is "
        "trying to do and choosing between valid, authored routes. Search remains ordinary "
        "search. Known relationships remain deterministic. Page composition remains "
        "deterministic.\n\n"
        "The routing model runs locally in your browser, and it is only justified while "
        "evaluations built from the Jobs to be Done show it routes better than deterministic "
        "baselines.",
        title="Where AI is used",
        weight=8,
    ),
    reference(
        "how-docs.rules",
        "Ontology decides what is related. Jobs to be Done explain why readers arrive. "
        "Journeys connect outcomes to concepts. Navigation projects the ontology. Search finds "
        "pages. Context composes authored blocks. Decision models must earn their place "
        "through evals.",
        title="Design rules",
        weight=7,
    ),
    domain="About these docs",
    show_ontology=True,
)

agent_run = concept(
    "agent-run",
    "Agent Run",
    "One coherent execution of an agent with context, model interaction, tools, and a result.",
    definition(
        "agent-run.definition",
        "An agent run turns an agent definition into behaviour. It receives input, creates run context, interacts with a model, may invoke tools, and produces a result.",
        weight=10,
    ),
    mental_model(
        "agent-run.mental-model",
        "Use the run as the centre of the runtime mental model: configuration flows into it; messages, events, usage, output, and traces flow out of it.",
        intents=[Intent.LEARN],
        experiences=[Experience.NEW, Experience.FAMILIAR],
    ),
    example(
        "agent-run.example",
        """from pydantic_ai import Agent\n\nagent = Agent('openai:gpt-5')\nresult = agent.run_sync('What is 2 + 2?')\nprint(result.output)""",
        intents=[Intent.BUILD, Intent.LEARN],
        preferences=[Preference.CODE_FIRST],
    ),
    kind=ConceptKind.RUNTIME,
    aliases=["run", "execution"],
    domain="Run & interaction",
)

agent = concept(
    "agent",
    "Agent",
    "The reusable definition of behaviour: instructions, model policy, dependencies, output, tools, and capabilities.",
    definition(
        "agent.definition",
        "An Agent defines how a model-powered component behaves across runs. The definition can be reused while each run gets its own input, context, events, messages, and result.",
        weight=10,
    ),
    example(
        "agent.example",
        """from pydantic_ai import Agent\n\nagent = Agent('openai:gpt-5', instructions='Answer concisely.')""",
        intents=[Intent.BUILD],
        preferences=[Preference.CODE_FIRST],
    ),
    kind=ConceptKind.ABSTRACTION,
    domain="Agent definition",
)

output = concept(
    "output",
    "Output",
    "The typed contract that defines what a successful run returns.",
    definition(
        "output.definition",
        "Output is the typed contract at the end of a run. Structural validation belongs here; semantic acceptance rules can be layered on with output validators.",
        weight=10,
    ),
    example(
        "output.example",
        """from pydantic import BaseModel\nfrom pydantic_ai import Agent\n\nclass Answer(BaseModel):\n    answer: str\n\nagent = Agent('openai:gpt-5', output_type=Answer)""",
        intents=[Intent.BUILD, Intent.LEARN],
        preferences=[Preference.CODE_FIRST],
    ),
    failure(
        "output.failure",
        "If the structure is correct but the content is unacceptable, use output validation rather than making the schema increasingly contorted.",
        intents=[Intent.FIX],
        weight=8,
    ),
    aliases=["structured output", "typed response", "json response"],
    domain="Agent definition",
)

output_validation = concept(
    "output-validation",
    "Output Validation",
    "Semantic checks that reject structurally valid but unacceptable model output.",
    definition(
        "output-validation.definition",
        "Output validation checks whether a valid typed result is acceptable for the application. A validator can request a retry when content violates a semantic rule.",
        weight=10,
    ),
    failure(
        "output-validation.failure",
        "Use this when the schema is valid but the answer is wrong, unsupported, unsafe, incomplete, or otherwise unacceptable.",
        intents=[Intent.FIX, Intent.OPERATE],
        weight=8,
    ),
    aliases=["validators", "semantic validation", "citations"],
    domain="Agent definition",
)

retries = concept(
    "retries",
    "Retries",
    "How an agent asks the model to try again after recoverable validation or tool failures.",
    definition(
        "retries.definition",
        "Retries let a run recover from model output or tool-call problems by feeding a targeted error back to the model and requesting another attempt.",
        weight=10,
    ),
    domain="Run & interaction",
)

dependencies = concept(
    "dependencies",
    "Dependencies",
    "Typed application context and services supplied to a run and its tools.",
    definition(
        "dependencies.definition",
        "Dependencies carry application services and state into the run without hiding them in global variables. Tools and validators can access them through RunContext.",
        weight=10,
    ),
    aliases=["database", "services", "api client", "run context"],
    domain="Agent definition",
)

capability = concept(
    "capability",
    "Capability",
    "Composable behaviour that can contribute tools, hooks, instructions, settings, or model selection.",
    definition(
        "capability.definition",
        "A capability packages reusable behaviour around the agent loop. It may contribute a toolset, instructions, hooks, settings, or model selection.",
        weight=10,
    ),
    domain="Capability & action",
)

tool = concept(
    "tool",
    "Tool",
    "An action exposed to the model during a run.",
    definition("tool.definition", "A tool gives the model a typed action it may choose to invoke."),
    example(
        "tool.example",
        """@agent.tool_plain\ndef weather(city: str) -> str:\n    return f'Weather for {city}'""",
        intents=[Intent.BUILD],
        preferences=[Preference.CODE_FIRST],
    ),
    aliases=["function tool", "actions", "system access"],
    domain="Capability & action",
)

model = concept(
    "model",
    "Model",
    "The inference abstraction used by a run.",
    definition(
        "model.definition",
        "A model is the inference abstraction. Provider is separate: providers make models available, while agents and runs consume models.",
        weight=10,
    ),
    aliases=["llm", "language model", "choose model"],
    domain="Models & providers",
)

provider = concept(
    "provider",
    "Provider",
    "A service or runtime that provides one or more models.",
    definition(
        "provider.definition",
        "OpenAI, Anthropic, Google, Ollama, and similar integrations are instances of Provider rather than peer conceptual categories.",
    ),
    kind=ConceptKind.PROVIDER,
    domain="Models & providers",
)

persistence = concept(
    "persistence",
    "Persistence",
    "Keeping conversation or execution state across process boundaries and restarts.",
    definition(
        "persistence.definition",
        "Persistence covers storing and restoring the state needed to continue work. Conversation persistence, step persistence, and durable execution solve related but distinct problems.",
        weight=10,
    ),
    aliases=["restart", "resume", "state", "durable"],
    domain="Conversation & state",
)

testing = concept(
    "testing",
    "Testing",
    "Fast deterministic checks of agent behaviour without relying on live model calls.",
    definition(
        "testing.definition",
        "Testing isolates deterministic behaviour and uses controlled models or functions so failures are reproducible and cheap.",
        weight=10,
    ),
    aliases=["unit test", "test model", "function model"],
    kind=ConceptKind.ASSURANCE,
    domain="Interfaces & assurance",
)

evaluation = concept(
    "evaluation",
    "Evaluation",
    "Evidence about how well a run, output, or trajectory satisfies explicit criteria.",
    definition(
        "evaluation.definition",
        "Evaluation measures behaviour across a dataset of cases. It belongs to the assurance model rather than the agent definition itself.",
        weight=10,
    ),
    aliases=["evals", "quality", "measure"],
    kind=ConceptKind.ASSURANCE,
    domain="Interfaces & assurance",
)

current = projection(
    "current",
    "Current docs",
    group("About", nav("How these docs are organised", "how-docs-are-organised")),
    group(
        "Core Concepts",
        nav("Agents", "agent"),
        nav("Dependencies", "dependencies"),
        nav("Output", "output"),
        nav("Output validation", "output-validation"),
        nav("Agent runs", "agent-run"),
        nav("Retries", "retries"),
        nav("Persistence", "persistence"),
    ),
    group("Models & Providers", nav("Models", "model"), nav("Providers", "provider")),
    group("Tools & Toolsets", nav("Tools", "tool")),
    group("Capabilities", nav("Capabilities", "capability")),
    group("Assurance", nav("Testing", "testing"), nav("Evaluation", "evaluation")),
)

reliable_answers = job(
    "reliable-answers",
    "Get reliable answers",
    "Make the agent return answers that are structurally correct and semantically acceptable.",
    example_phrase(
        "It keeps giving me valid JSON but the citations are made up",
        expected=["output-validation"],
        answer_must_contain=["validation", "semantic"],
    ),
    example_phrase(
        "I need a typed object back instead of free text",
        expected=["output"],
        answer_must_contain=["typed"],
    ),
    example_phrase(
        "How do I make it try again when the answer fails my checks?",
        expected=["retries", "output-validation"],
        answer_must_contain=["retry"],
    ),
    expected=["output", "output-validation", "retries"],
)

system_access = job(
    "system-access",
    "Give the agent access to my systems",
    "Connect agent behaviour to application services and actions without hiding dependencies.",
    example_phrase(
        "My agent needs to call our internal pricing API",
        expected=["tool"],
        answer_must_contain=["action"],
    ),
    example_phrase(
        "How should my tools get a database connection?",
        expected=["dependencies"],
        answer_must_contain=["dependencies"],
    ),
    expected=["tool", "dependencies", "capability"],
)

survive_failures = job(
    "survive-failures",
    "Survive failures and restarts",
    "Recover from transient model failures and continue work across process interruption.",
    example_phrase(
        "The worker can die halfway through; I need to resume safely",
        expected=["persistence"],
        answer_must_contain=["restore"],
    ),
    example_phrase(
        "A tool call sometimes fails and I want the model to recover",
        expected=["retries"],
        answer_must_contain=["recover"],
    ),
    expected=["persistence", "retries"],
)

know_it_works = job(
    "know-it-works",
    "Know whether it works",
    "Test deterministic behaviour and measure quality across representative cases.",
    example_phrase(
        "How do I test the agent without paying for model calls?",
        expected=["testing"],
        answer_must_contain=["deterministic"],
    ),
    example_phrase(
        "I want a dataset that tells me whether answer quality is improving",
        expected=["evaluation"],
        answer_must_contain=["dataset"],
    ),
    expected=["testing", "evaluation"],
)

choose_model = job(
    "choose-model",
    "Choose how inference runs",
    "Pick the model/provider combination that fits the application and runtime constraints.",
    example_phrase("Which model should this agent use?", expected=["model"]),
    example_phrase(
        "Can I run this through Ollama instead of OpenAI?", expected=["provider", "model"]
    ),
    expected=["model", "provider"],
)

first_agent = job(
    "first-agent",
    "Build my first agent",
    "Go from an installed package to an agent that returns a typed result and calls a tool.",
    example_phrase("How do I get started with an agent?", expected=["agent"]),
    example_phrase("I want the agent to return a typed object", expected=["output"]),
    expected=["agent", "model", "output", "tool"],
)

journeys = [
    journey(
        "first-agent-journey",
        "First agent",
        "first-agent",
        "Define an agent, choose its model, type its output, then give it an action.",
        step("agent", "Define behaviour once and reuse it."),
        step("model", "Choose how inference runs."),
        step("output", "Declare what a successful run returns."),
        step("tool", "Let the model take an action."),
    ),

    journey(
        "reliable-answers-journey",
        "Reliable answers",
        "reliable-answers",
        "Start with the response contract, then add semantic checks and recovery behaviour.",
        step("output", "Define the structural contract."),
        step("output-validation", "Reject semantically unacceptable results."),
        step("retries", "Recover by asking the model to try again."),
        step("evaluation", "Measure the behaviour across representative cases."),
    ),
    journey(
        "system-access-journey",
        "System access",
        "system-access",
        "Separate actions from application dependencies, then package reusable behaviour.",
        step("dependencies", "Provide typed application services."),
        step("tool", "Expose actions to the model."),
        step("capability", "Package reusable behaviour when it spans more than one tool."),
    ),
    journey(
        "survive-failures-journey",
        "Failure recovery",
        "survive-failures",
        "Handle recoverable failures first, then add persistence when work must survive process interruption.",
        step("retries", "Recover within a run."),
        step("persistence", "Restore state across interruption."),
    ),
    journey(
        "know-it-works-journey",
        "Confidence in behaviour",
        "know-it-works",
        "Use deterministic tests for known behaviour and evals for quality across cases.",
        step("testing", "Make failures cheap and reproducible."),
        step("evaluation", "Measure quality across a dataset."),
    ),
]

DOCS = docs(
    "Pydantic AI Knowledge",
    concepts=[
        about_docs,
        agent_run,
        agent,
        output,
        output_validation,
        retries,
        dependencies,
        capability,
        tool,
        model,
        provider,
        persistence,
        testing,
        evaluation,
    ],
    relationships=[
        relates(
            "agent",
            RelationKind.INSTANTIATES,
            "agent-run",
            label="instantiates",
            route_when="when the user needs to understand what happens when an agent runs",
            weight=10,
        ),
        relates(
            "agent",
            RelationKind.HAS,
            "output",
            label="declares output",
            route_when="when the user needs typed or structured results",
        ),
        relates(
            "output",
            RelationKind.RELATED_TO,
            "output-validation",
            label="validated by",
            route_when="when structurally valid output can still be semantically unacceptable",
            weight=9,
        ),
        relates(
            "output-validation",
            RelationKind.RELATED_TO,
            "retries",
            label="may request",
            route_when="when a failed semantic check should trigger another model attempt",
            weight=9,
        ),
        relates(
            "agent",
            RelationKind.DEPENDS_ON,
            "dependencies",
            label="uses dependencies",
            route_when="when tools or validators need typed application services",
        ),
        relates(
            "agent-run",
            RelationKind.USES,
            "model",
            label="uses",
            route_when="when choosing how inference should run",
            weight=10,
        ),
        relates(
            "provider",
            RelationKind.PROVIDES,
            "model",
            label="provides",
            route_when="when changing model vendors or local runtimes",
        ),
        relates(
            "capability",
            RelationKind.CONTRIBUTES,
            "tool",
            label="may contribute",
            route_when="when reusable behaviour includes actions",
        ),
        relates(
            "agent",
            RelationKind.HAS,
            "capability",
            label="has",
            route_when="when behaviour spans tools, hooks, instructions or settings",
        ),
        relates(
            "agent-run",
            RelationKind.PRODUCES,
            "output",
            label="produces",
            route_when="when investigating what a run returns",
        ),
        relates(
            "persistence",
            RelationKind.RESUMES,
            "agent-run",
            label="resumes",
            route_when="when work must survive process interruption",
            weight=10,
        ),
        relates(
            "testing",
            RelationKind.EVALUATES,
            "agent-run",
            label="tests",
            route_when="when behaviour should be checked without live model calls",
        ),
        relates(
            "evaluation",
            RelationKind.EVALUATES,
            "agent-run",
            label="evaluates",
            route_when="when quality should be measured across representative cases",
            weight=10,
        ),
    ],
    projections=[current],
    jobs=[first_agent, reliable_answers, system_access, survive_failures, know_it_works, choose_model],
    journeys=journeys,
    branding=Branding(
        name="Pydantic AI Knowledge",
        logo_svg=Path(__file__).with_name("assets").joinpath("pydantic-ai-light.svg").read_text(),
        logo_svg_dark=Path(__file__)
        .with_name("assets")
        .joinpath("pydantic-ai-dark.svg")
        .read_text(),
        links=(
            BrandLink(label="Pydantic Validation", url="https://docs.pydantic.dev/"),
            BrandLink(label="Pydantic AI", url="https://ai.pydantic.dev/", current=True),
            BrandLink(label="Pydantic Logfire", url="https://logfire.pydantic.dev/"),
        ),
    ),
    home="agent-run",
    domains=[
        "Agent definition",
        "Run & interaction",
        "Conversation & state",
        "Models & providers",
        "Capability & action",
        "Execution & environment",
        "Interfaces & assurance",
    ],
)

# Ontology domains for concepts introduced by the restored and imported pages below.
_ontology_domains = {"messages": "Conversation & state", "streaming": "Run & interaction"}


# Preserve every authored block and route from the earlier adaptive prototype.
# This is a curated example, not a mirror of the complete upstream documentation.
_original = json.loads(
    Path(__file__).with_name("assets").joinpath("adaptive-content.json").read_text()
)
_ids = {"agents": "agent", "tools": "tool", "output-validators": "output-validation"}
_kinds = {
    "lead": BlockKind.DEFINITION,
    "code": BlockKind.EXAMPLE,
    "concept": BlockKind.MENTAL_MODEL,
    "pitfall": BlockKind.FAILURE,
    "testing": BlockKind.PROCEDURE,
    "api": BlockKind.REFERENCE,
    "next": BlockKind.NOTE,
}
_concepts = {c.id: c for c in DOCS.concepts}
_relationships = list(DOCS.relationships)
for page in _original:
    concept_id = _ids.get(page["id"], page["id"])
    blocks = tuple(
        KnowledgeBlock(
            id=f"{concept_id}.restored.{block['id']}",
            kind=_kinds[block["kind"]],
            title=block["title"],
            body=block["code"] or block["body"],
            language="python" if block["code"] else None,
            intents=frozenset(Intent(i) for i in block["intents"]),
            weight=10 if block["essential"] else 0,
        )
        for block in page["blocks"]
    )
    existing = _concepts.get(concept_id)
    _concepts[concept_id] = Concept(
        id=concept_id,
        title=page["title"],
        summary=page["summary"],
        kind=existing.kind if existing else ConceptKind.CONCEPT,
        domain=existing.domain if existing else _ontology_domains.get(concept_id),
        source_url=page["source_url"],
        aliases=frozenset(page["search_terms"]) | (existing.aliases if existing else frozenset()),
        blocks=blocks + (existing.blocks if existing else ()),
    )
    for link in page["next"]:
        target = _ids.get(link["target"], link["target"])
        # A typed relationship already says more than a generic "next" route.
        if any(r.source == concept_id and r.target == target for r in _relationships):
            continue
        _relationships.append(
            Relationship(
                source=concept_id,
                target=target,
                kind=RelationKind.RELATED_TO,
                route_when=link["when"],
                label="next",
                weight=10,
            )
        )
DOCS = DOCS.model_copy(
    update={
        "concepts": tuple(_concepts.values()),
        "relationships": tuple(_relationships),
        "decision": DecisionConfig(
            entry_concepts=("agent", "output", "tool", "dependencies", "testing")
        ),
    }
)
# Validate the expanded model instead of relying on model_copy to validate updates.
DOCS = type(DOCS).model_validate(DOCS.model_dump())


# Full documentation is the default view; curated blocks remain available for tailoring.


_navigation = yaml.safe_load(
    Path(__file__).with_name("pydantic_ai_content").joinpath("navigation.yml").read_text()
)
_titles, _routes = {}, {}


def _nav_entries(entries):
    result = []
    for entry in entries:
        if "path" in entry and entry["path"].endswith(".md"):
            _titles[entry["path"]] = entry["page"]
            _routes[entry["path"]] = entry.get("slug", entry["path"].removesuffix(".md"))
        result.extend(_nav_entries(entry.get("contents", [])))
    return result


_nav_entries(_navigation["navigation"])
_full = import_markdown_directory(
    Path(__file__).with_name("pydantic_ai_content"),
    base_url="https://pydantic.dev/docs/ai/",
    ids={
        "agent.md": "agent",
        "output.md": "output",
        "tools.md": "tool",
        "dependencies.md": "dependencies",
        "testing.md": "testing",
        "retries.md": "retries",
        "message-history.md": "messages",
        "models/overview.md": "model",
        "output-validation.md": "output-validation",
        "evals.md": "evaluation",
        "persistence.md": "persistence",
        "capabilities/overview.md": "capability",
        "toolsets.md": "toolset",
        "hooks.md": "hooks",
        "mcp/overview.md": "mcp",
        "workspace.md": "workspace",
        "timeouts.md": "timeouts",
        "multi-agent-applications.md": "multi-agent",
        "realtime/overview.md": "realtime",
        "durable_execution/overview.md": "durable-execution",
        "graph.md": "graph",
        "interfaces.md": "interfaces",
        "logfire.md": "observability",
        "gateway.md": "gateway",
    },
    titles=_titles,
    routes=_routes,
)
_concepts = {c.id: c for c in DOCS.concepts}
for page in _full:
    curated = _concepts.get(page.id)
    # Imported pages bring complete source text; curated concepts keep their ontology identity.
    identity = (
        {
            # Page titles follow upstream, except generic section titles such as "Overview".
            "title": curated.title if page.title == "Overview" else page.title,
            "kind": curated.kind,
            "domain": curated.domain,
            "aliases": curated.aliases | page.aliases,
        }
        if curated
        else {}
    )
    _concepts[page.id] = page.model_copy(
        update={"blocks": (curated.blocks if curated else ()) + page.blocks, **identity}
    )

# --- Information architecture ---------------------------------------------------------
# Every upstream page is placed in the ontology once, here. The sidebar, the concept map,
# page context and pagination are all generated from these placements; the upstream
# navigation is kept only as a secondary projection for comparison.
AGENT, RUN, STATE, MODELS, ACTION, ENV, ASSURE = DOCS.domains

_PLACEMENT = {
    # Start here
    "index.md": (None, Role.START, None),
    "install.md": (None, Role.START, None),
    "coding-agent-skills.md": (None, Role.START, None),
    "help.md": (None, Role.START, None),
    "enterprise-support.md": (None, Role.START, None),
    "troubleshooting.md": (None, Role.START, None),
    # Agent definition
    "agent.md": (AGENT, Role.CONCEPT, None),
    "dependencies.md": (AGENT, Role.CONCEPT, None),
    "output.md": (AGENT, Role.CONCEPT, None),
    "input.md": (AGENT, Role.GUIDE, None),
    "agent-spec.md": (AGENT, Role.GUIDE, None),
    # Run & interaction
    "retries.md": (RUN, Role.CONCEPT, None),
    "timeouts.md": (RUN, Role.CONCEPT, None),
    "multi-agent-applications.md": (RUN, Role.CONCEPT, None),
    "realtime/overview.md": (RUN, Role.CONCEPT, None),
    # Conversation & state
    "message-history.md": (STATE, Role.CONCEPT, None),
    "persistence.md": (STATE, Role.CONCEPT, None),
    # Models & providers
    "models/overview.md": (MODELS, Role.CONCEPT, None),
    "gateway.md": (MODELS, Role.INTEGRATION, "Providers"),
    "models/decision.md": (MODELS, Role.GUIDE, None),
    "direct.md": (MODELS, Role.GUIDE, None),
    "image-generation.md": (MODELS, Role.GUIDE, None),
    "embeddings.md": (MODELS, Role.GUIDE, None),
    # Capability & action
    "tools.md": (ACTION, Role.CONCEPT, None),
    "toolsets.md": (ACTION, Role.CONCEPT, None),
    "capabilities/overview.md": (ACTION, Role.CONCEPT, None),
    "hooks.md": (ACTION, Role.CONCEPT, None),
    "mcp/overview.md": (ACTION, Role.CONCEPT, None),
    "tools-advanced.md": (ACTION, Role.GUIDE, "Tools"),
    "deferred-tools.md": (ACTION, Role.GUIDE, "Tools"),
    "native-tools.md": (ACTION, Role.GUIDE, "Tools"),
    "common-tools.md": (ACTION, Role.INTEGRATION, "Tool collections"),
    "third-party-tools.md": (ACTION, Role.INTEGRATION, "Tool collections"),
    "capabilities/on-demand.md": (ACTION, Role.GUIDE, "Building capabilities"),
    "capabilities/custom.md": (ACTION, Role.GUIDE, "Building capabilities"),
    "extensibility.md": (ACTION, Role.GUIDE, "Building capabilities"),
    "mcp/client.md": (ACTION, Role.GUIDE, "MCP"),
    "mcp/server.md": (ACTION, Role.GUIDE, "MCP"),
    "harness/index.md": (ACTION, Role.INTEGRATION, "Capability library"),
    "capabilities/third-party.md": (ACTION, Role.INTEGRATION, "Capability library"),
    "harness/examples.md": (ACTION, Role.EXAMPLE, None),
    # Execution & environment
    "workspace.md": (ENV, Role.CONCEPT, None),
    "durable_execution/overview.md": (ENV, Role.CONCEPT, None),
    "graph.md": (ENV, Role.CONCEPT, None),
    "durable_execution/backends.md": (ENV, Role.GUIDE, "Durable backends"),
    "harness/aws-lambda.md": (ENV, Role.INTEGRATION, "Durable backends"),
    "harness/absurd.md": (ENV, Role.INTEGRATION, "Durable backends"),
    "harness/durable-execution.md": (ENV, Role.INTEGRATION, "Durable backends"),
    # Interfaces & assurance
    "testing.md": (ASSURE, Role.CONCEPT, None),
    "evals.md": (ASSURE, Role.CONCEPT, None),
    "logfire.md": (ASSURE, Role.CONCEPT, None),
    "interfaces.md": (ASSURE, Role.CONCEPT, None),
    "web.md": (ASSURE, Role.INTEGRATION, "Interfaces"),
    "cli.md": (ASSURE, Role.INTEGRATION, "Interfaces"),
    "harness/gh-aw.md": (ASSURE, Role.INTEGRATION, "Interfaces"),
    "harness/acp.md": (ASSURE, Role.INTEGRATION, "Interfaces"),
    "ui/overview.md": (ASSURE, Role.GUIDE, "UI event streams"),
    "ui/ag-ui.md": (ASSURE, Role.INTEGRATION, "UI event streams"),
    "ui/vercel-ai.md": (ASSURE, Role.INTEGRATION, "UI event streams"),
    "evals/examples/simple-validation.md": (ASSURE, Role.EXAMPLE, None),
}

# Families of the upstream "Capabilities" section; environments move to their own domain.
_CAPABILITY_FAMILIES = {
    "Execution Environments": (ENV, "Execution environments"),
    "Execution Runtime": (ENV, "Execution runtime"),
}
# API modules, placed with the concepts they document.
_API_DOMAINS = {
    "agent": AGENT, "output": AGENT, "result": AGENT, "settings": AGENT, "format_prompt": AGENT,
    "template": AGENT, "function_signature": AGENT, "profiles": MODELS, "providers": MODELS,
    "direct": MODELS, "embeddings": MODELS, "images": MODELS, "run": RUN, "retries": RUN,
    "usage": RUN, "exceptions": RUN, "concurrency": RUN, "realtime": RUN, "messages": STATE,
    "tools": ACTION, "toolsets": ACTION, "capabilities": ACTION, "native_tools": ACTION,
    "common_tools": ACTION, "mcp": ACTION, "ext": ACTION, "durable_exec": ENV,
    "workspaces": ENV, "pydantic_graph": ENV, "pydantic_evals": ASSURE, "ui": ASSURE,
    "models": MODELS,
}


def _place(path: str, trail: list[str]) -> tuple[str | None, Role, str | None]:
    if path in _PLACEMENT:
        return _PLACEMENT[path]
    section = trail[0] if trail else ""
    sub = trail[1] if len(trail) > 1 else None
    if path.startswith("models/"):
        return MODELS, Role.INTEGRATION, "Providers"
    if path.startswith("realtime/"):
        providers = {"openai", "azure", "gemini", "xai"}
        if path.removeprefix("realtime/").removesuffix(".md") in providers:
            return RUN, Role.INTEGRATION, "Realtime providers"
        return RUN, Role.GUIDE, "Realtime"
    if path.startswith("durable_execution/"):
        return ENV, Role.INTEGRATION, "Durable backends"
    if path.startswith("graph/"):
        return ENV, Role.GUIDE, "Graph builder"
    if path.startswith("evals/"):
        return ASSURE, Role.GUIDE, "Pydantic Evals" + (f" / {sub}" if sub else "")
    if section == "Capabilities" and sub:
        domain, family = _CAPABILITY_FAMILIES.get(sub, (ACTION, f"Capability library / {sub}"))
        return domain, Role.INTEGRATION, family
    if section == "API Reference":
        module = path.removeprefix("api/").split("/")[0].removesuffix(".md")
        return _API_DOMAINS.get(module), Role.REFERENCE, None
    if section == "Examples":
        return None, Role.EXAMPLE, sub
    if section == "Comparisons":
        return None, Role.PROJECT, "Comparisons"
    if section == "Project":
        return None, Role.PROJECT, None
    return None, Role.REFERENCE, None


# Implementation pages are kinds of a core concept; these links feed the concept map's
# counts and every page's context.
_KIND_OF = {
    "Providers": "provider",
    "Realtime providers": "realtime",
    "Durable backends": "durable-execution",
    "Execution environments": "workspace",
    "Execution runtime": "capability",
    "Tool collections": "toolset",
    "Interfaces": "interfaces",
    "UI event streams": "interfaces",
}


def _walk(entries, trail=()):
    for entry in entries:
        if "path" in entry:
            yield entry["path"], list(trail)
        if entry.get("contents"):
            yield from _walk(entry["contents"], (*trail, entry.get("section", entry.get("page"))))


_page_by_path = {}
for _concept in _full:
    for _path, _route in _routes.items():
        if _concept.source_url == "https://pydantic.dev/docs/ai/" + _route + "/":
            _page_by_path[_path] = _concept.id
_placed = {}
for _path, _trail in _walk(_navigation["navigation"]):
    if _path in _page_by_path:
        _placed[_page_by_path[_path]] = (*_place(_path, _trail), _trail)

_relationships = list(DOCS.relationships)
for concept_id, (domain, role, family, trail) in _placed.items():
    current = _concepts[concept_id]
    curated = current.id in {c.id for c in DOCS.concepts}
    # A section overview that becomes a concept is named after its section.
    title = current.title
    if title == "Overview" and role is Role.CONCEPT and trail:
        title = trail[0].split(" (")[0].removeprefix("Pydantic ")
    _concepts[concept_id] = current.model_copy(
        update={"domain": current.domain if curated and current.domain else domain,
                "role": role, "family": family, "title": title}
    )
    parent = _KIND_OF.get((family or "").split(" / ")[0])
    if family and family.startswith("Capability library") and concept_id != "capability":
        parent = "capability"
    if parent and parent != concept_id and role is Role.INTEGRATION:
        kind = RelationKind.PROVIDES if parent == "realtime" else RelationKind.IS_A
        _relationships.append(relates(concept_id, kind, parent))
# Pages outside upstream navigation (for example new harness pages).
for _concept in _full:
    if _concept.id not in _placed:
        harness = _concept.id.startswith("reference-harness-")
        _concepts[_concept.id] = _concepts[_concept.id].model_copy(
            update={
                "role": Role.INTEGRATION if harness else Role.REFERENCE,
                "domain": ACTION if harness else None,
                "family": "Capability library" if harness else None,
            }
        )
        if harness:
            _relationships.append(relates(_concept.id, RelationKind.IS_A, "capability"))

# Reading order: upstream order, with curated concepts beside the page they belong to.
_beside = {"agent": ["agent-run"], "output": ["output-validation"],
           "messages": ["streaming"], "model": ["provider"]}
_order = []
for _path, _trail in _walk(_navigation["navigation"]):
    concept_id = _page_by_path.get(_path)
    if concept_id and concept_id not in _order:
        _order += [concept_id, *_beside.get(concept_id, [])]
_concepts = {k: _concepts[k] for k in [about_docs.id, *_order, *_concepts] if k in _concepts}

# Core relationships for the concepts the imported pages add to the ontology.
_relationships += [
    relates("agent", RelationKind.HAS, "toolset", label="registers", weight=8,
            route_when="when tools come in groups or from an external source"),
    relates("toolset", RelationKind.CONTAINS, "tool", label="contains", weight=8),
    relates("mcp", RelationKind.PROVIDES, "toolset", label="exposes tools as",
            route_when="when tools live in an MCP server"),
    relates("capability", RelationKind.CONTRIBUTES, "hooks", label="may contribute"),
    relates("hooks", RelationKind.OBSERVES, "agent-run", label="intercepts", weight=8,
            route_when="when behaviour must run before or after model and tool calls"),
    relates("agent-run", RelationKind.RECORDS, "messages", label="records", weight=8),
    relates("persistence", RelationKind.PERSISTS, "messages", label="stores"),
    relates("agent-run", RelationKind.EMITS, "streaming", label="streams"),
    relates("agent-run", RelationKind.HAS, "timeouts", label="bounded by"),
    relates("multi-agent", RelationKind.ORCHESTRATES, "agent", label="coordinates",
            route_when="when one agent should delegate to others"),
    relates("agent", RelationKind.INSTANTIATES, "realtime", label="runs as a voice session"),
    relates("durable-execution", RelationKind.PERSISTS, "agent-run", label="checkpoints",
            weight=10, route_when="when long-running work must survive restarts"),
    relates("graph", RelationKind.ORCHESTRATES, "agent-run", label="orchestrates"),
    relates("tool", RelationKind.USES, "workspace", label="acts in"),
    relates("interfaces", RelationKind.USES, "streaming", label="renders"),
    relates("observability", RelationKind.OBSERVES, "agent-run", label="traces", weight=10,
            route_when="when you need to see what a run did"),
    relates("gateway", RelationKind.IS_A, "provider"),
]

# How these docs are organised sits with the start pages.
_concepts[about_docs.id] = _concepts[about_docs.id].model_copy(update={"role": Role.START})

_upstream_used: set[str] = set()


def _upstream(entries):
    """The upstream sidebar, kept as a second projection for comparison."""
    result = []
    for entry in entries:
        if "path" in entry:
            if entry["path"] in _page_by_path:
                result.append(nav(entry["page"], _page_by_path[entry["path"]]))
                _upstream_used.add(_page_by_path[entry["path"]])
        elif entry.get("contents"):
            children = _upstream(entry["contents"])
            if children and entry.get("top-level"):
                result.extend(children)
            elif children:
                result.append(group(entry.get("section", "Documentation"), *children))
    return result


DOCS = type(DOCS).model_validate(
    DOCS.model_copy(
        update={
            "concepts": tuple(_concepts.values()),
            "relationships": tuple(_relationships),
            "home_concept": "reference-index",
            # Needs the imported gateway page, so it is added after the merge.
            "journeys": (
                *DOCS.journeys,
                journey(
                    "choose-model-journey",
                    "Choosing inference",
                    "choose-model",
                    "Understand the model abstraction, then pick a provider or use the gateway.",
                    step("model", "The abstraction every run uses."),
                    step("provider", "Where models come from."),
                    step("gateway", "One key for every provider, with cost controls."),
                ),
            ),
        }
    ).model_dump()
)
DOCS = type(DOCS).model_validate(
    DOCS.model_copy(
        update={
            "projections": (
                ontology_projection(DOCS, title="Pydantic AI documentation"),
                projection("upstream", "Upstream order", *_upstream(_navigation["navigation"])),
            )
        }
    ).model_dump()
)
