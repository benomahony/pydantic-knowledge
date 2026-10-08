from __future__ import annotations

from pathlib import Path

from pydantic_knowledge import (
    RelationKind,
    cases_from_jobs,
    concept,
    definition,
    docs,
    example_phrase,
    job,
    journey,
    relates,
    run_baselines,
    ship_gate,
    step,
    suggest_docs,
    write_eval_artifacts,
)


def knowledge():
    output = concept(
        "output",
        "Output",
        "Typed structured results.",
        definition("output.def", "Output is a typed contract."),
        aliases=["typed response", "json"],
    )
    validation = concept(
        "validation",
        "Output Validation",
        "Reject semantically unacceptable output.",
        definition("validation.def", "Semantic validation can reject unacceptable answers."),
        aliases=["citations", "semantic validation"],
    )
    reliable = job(
        "reliable",
        "Get reliable answers",
        "Return structurally and semantically acceptable answers.",
        example_phrase(
            "The JSON is valid but the citations are made up",
            expected=["validation"],
            answer_must_contain=["semantic"],
        ),
    )
    return docs(
        "Example",
        concepts=[output, validation],
        relationships=[
            relates(
                "output",
                RelationKind.RELATED_TO,
                "validation",
                route_when="when valid output is semantically unacceptable or citations are wrong",
            )
        ],
        jobs=[reliable],
        journeys=[
            journey(
                "reliable-path",
                "Reliable answers",
                "reliable",
                "Move from structure to semantic acceptance.",
                step("output", "Start with structure."),
                step("validation", "Then validate meaning."),
            )
        ],
        home="output",
    )


def test_jtbd_examples_become_eval_cases() -> None:
    cases = cases_from_jobs(knowledge())
    assert len(cases) == 1
    assert cases[0][1].phrase.startswith("The JSON")
    assert cases[0][2].expected_concepts == ("validation",)


def test_route_when_is_used_by_baseline_router() -> None:
    suggestions = suggest_docs(knowledge(), "citations are wrong", scorer="hybrid")
    assert suggestions[0].concept_id == "validation"


def test_baselines_and_ship_gate_are_automatic() -> None:
    report = run_baselines(knowledge())
    assert set(report["experiments"]) == {"token", "char_ngram", "hybrid"}
    assert ship_gate(report)["decision"] == "AI_NOT_YET_JUSTIFIED"


def test_eval_outputs_are_written(tmp_path: Path) -> None:
    root = write_eval_artifacts(knowledge(), tmp_path / "evals")
    assert (root / "routing-cases.json").exists()
    assert (root / "baseline-results.json").exists()
    assert (root / "report.md").exists()
    assert (root / "dashboard.html").exists()
