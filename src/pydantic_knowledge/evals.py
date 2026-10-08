from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict

from .models import DocsContext, KnowledgeBase
from .routing import SCORERS, authored_answer, suggest_docs


class EvalInput(BaseModel):
    model_config = ConfigDict(frozen=True)
    phrase: str
    job_id: str
    current_concept: str | None = None


class EvalExpected(BaseModel):
    model_config = ConfigDict(frozen=True)
    expected_concepts: tuple[str, ...]
    answer_must_contain: tuple[str, ...] = ()
    answer_must_not_contain: tuple[str, ...] = ()


class EvalOutput(BaseModel):
    model_config = ConfigDict(frozen=True)
    suggested_concepts: tuple[str, ...]
    answer: str


def cases_from_jobs(kb: KnowledgeBase) -> tuple[tuple[str, EvalInput, EvalExpected], ...]:
    cases: list[tuple[str, EvalInput, EvalExpected]] = []
    for job in kb.jobs:
        for i, example in enumerate(job.examples, start=1):
            expected = example.expected_concepts or job.expected_concepts
            assert expected, f"job example needs expected concepts: {job.id} #{i}"
            cases.append(
                (
                    f"{job.id}-{i:02d}",
                    EvalInput(
                        phrase=example.phrase,
                        job_id=job.id,
                        current_concept=example.current_concept,
                    ),
                    EvalExpected(
                        expected_concepts=expected,
                        answer_must_contain=example.answer_must_contain,
                        answer_must_not_contain=example.answer_must_not_contain,
                    ),
                )
            )
    return tuple(cases)


def baseline_task(
    kb: KnowledgeBase, *, scorer: str = "hybrid", limit: int = 3
) -> Callable[[EvalInput], EvalOutput]:
    def task(inputs: EvalInput) -> EvalOutput:
        suggestions = suggest_docs(
            kb,
            inputs.phrase,
            current_concept=inputs.current_concept,
            scorer=scorer,
            limit=limit,
        )
        concept_ids = tuple(s.concept_id for s in suggestions)
        return EvalOutput(
            suggested_concepts=concept_ids,
            answer=authored_answer(kb, concept_ids[:1], context=DocsContext()),
        )

    task.__name__ = f"{scorer}_docs_router"
    return task


def build_pydantic_evals_dataset(kb: KnowledgeBase) -> Any:
    """Build a native pydantic_evals Dataset from JTBD examples.

    `pydantic-evals` is an optional dependency so importing pydantic_knowledge stays lightweight.
    Install with `uv add 'pydantic-knowledge[evals]'` or `uv add pydantic-evals`.
    """
    try:
        from pydantic_evals import Case, Dataset
        from pydantic_evals.evaluators import Evaluator, EvaluatorContext
    except ImportError as exc:  # pragma: no cover - dependency not installed in minimal env
        raise RuntimeError(
            "Pydantic Evals is required for native experiments. Install pydantic-evals."
        ) from exc

    class RouteAt1(Evaluator[EvalInput, EvalOutput, dict[str, str]]):
        def evaluate(self, ctx: EvaluatorContext[EvalInput, EvalOutput, dict[str, str]]) -> bool:
            expected = ctx.expected_output
            assert isinstance(expected, EvalExpected)
            return (
                bool(ctx.output.suggested_concepts)
                and ctx.output.suggested_concepts[0] in expected.expected_concepts
            )

    class RouteHitAt3(Evaluator[EvalInput, EvalOutput, dict[str, str]]):
        def evaluate(self, ctx: EvaluatorContext[EvalInput, EvalOutput, dict[str, str]]) -> bool:
            expected = ctx.expected_output
            assert isinstance(expected, EvalExpected)
            return bool(set(ctx.output.suggested_concepts[:3]) & set(expected.expected_concepts))

    class AnswerAssertions(Evaluator[EvalInput, EvalOutput, dict[str, str]]):
        def evaluate(
            self, ctx: EvaluatorContext[EvalInput, EvalOutput, dict[str, str]]
        ) -> dict[str, bool]:
            expected = ctx.expected_output
            assert isinstance(expected, EvalExpected)
            answer = ctx.output.answer.lower()
            return {
                "answer_contains": all(x.lower() in answer for x in expected.answer_must_contain),
                "answer_excludes": all(
                    x.lower() not in answer for x in expected.answer_must_not_contain
                ),
            }

    cases = [
        Case(
            name=name,
            inputs=inputs,
            expected_output=expected,
            metadata={"job_id": inputs.job_id},
        )
        for name, inputs, expected in cases_from_jobs(kb)
    ]
    return Dataset(
        name=f"{kb.title.lower().replace(' ', '-')}-docs-routing",
        cases=cases,
        evaluators=[RouteAt1(), RouteHitAt3(), AnswerAssertions()],
    )


def run_pydantic_evals(kb: KnowledgeBase, task: Callable[[EvalInput], EvalOutput]) -> Any:
    dataset = build_pydantic_evals_dataset(kb)
    return dataset.evaluate_sync(task)


@dataclass(frozen=True)
class BaselineCaseResult:
    name: str
    phrase: str
    job_id: str
    expected: tuple[str, ...]
    suggested: tuple[str, ...]
    route_at_1: bool
    hit_at_3: bool
    answer_contains: bool
    answer_excludes: bool


def run_baselines(kb: KnowledgeBase) -> dict[str, object]:
    """Run cheap local baselines without requiring pydantic-evals.

    This is intentionally only a convenience report. Pydantic Evals remains the experiment harness.
    """
    payload: dict[str, object] = {"dataset_cases": len(cases_from_jobs(kb)), "experiments": {}}
    experiments: dict[str, object] = payload["experiments"]  # type: ignore[assignment]
    for scorer in SCORERS:
        task = baseline_task(kb, scorer=scorer)
        rows: list[BaselineCaseResult] = []
        for name, inputs, expected in cases_from_jobs(kb):
            output = task(inputs)
            lower = output.answer.lower()
            rows.append(
                BaselineCaseResult(
                    name=name,
                    phrase=inputs.phrase,
                    job_id=inputs.job_id,
                    expected=expected.expected_concepts,
                    suggested=output.suggested_concepts,
                    route_at_1=bool(output.suggested_concepts)
                    and output.suggested_concepts[0] in expected.expected_concepts,
                    hit_at_3=bool(
                        set(output.suggested_concepts[:3]) & set(expected.expected_concepts)
                    ),
                    answer_contains=all(x.lower() in lower for x in expected.answer_must_contain),
                    answer_excludes=all(
                        x.lower() not in lower for x in expected.answer_must_not_contain
                    ),
                )
            )
        n = len(rows) or 1
        experiments[scorer] = {
            "route_at_1": sum(r.route_at_1 for r in rows) / n,
            "hit_at_3": sum(r.hit_at_3 for r in rows) / n,
            "answer_assertions": sum(r.answer_contains and r.answer_excludes for r in rows) / n,
            "cases": [r.__dict__ for r in rows],
        }
    return payload


def ship_gate(
    report: dict[str, object],
    *,
    ai_result: dict[str, float] | None = None,
    min_accuracy_gain: float = 0.05,
) -> dict[str, object]:
    experiments = report["experiments"]
    assert isinstance(experiments, dict)
    best_name, best = max(experiments.items(), key=lambda item: item[1]["route_at_1"])  # type: ignore[index]
    best_accuracy = float(best["route_at_1"])  # type: ignore[index]
    best_hit = float(best["hit_at_3"])  # type: ignore[index]
    if ai_result is None:
        return {
            "decision": "AI_NOT_YET_JUSTIFIED",
            "reason": "No decision-model experiment has been supplied.",
            "best_baseline": best_name,
            "best_baseline_route_at_1": best_accuracy,
            "best_baseline_hit_at_3": best_hit,
            "required_accuracy_gain": min_accuracy_gain,
        }
    ai_accuracy = ai_result["route_at_1"]
    ai_hit = ai_result["hit_at_3"]
    passed = ai_accuracy >= best_accuracy + min_accuracy_gain and ai_hit >= best_hit
    return {
        "decision": "SHIP_AI_ROUTER" if passed else "KEEP_DETERMINISTIC_ROUTER",
        "best_baseline": best_name,
        "best_baseline_route_at_1": best_accuracy,
        "best_baseline_hit_at_3": best_hit,
        "ai_route_at_1": ai_accuracy,
        "ai_hit_at_3": ai_hit,
        "required_accuracy_gain": min_accuracy_gain,
    }


def write_baseline_report(kb: KnowledgeBase, output: str | Path) -> Path:
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    report = run_baselines(kb)
    report["ship_gate"] = ship_gate(report)
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return path
