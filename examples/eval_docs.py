"""Run the documentation routing benchmark with native Pydantic Evals.

Install the optional dependency first:
    uv sync --extra evals

The same Dataset can be evaluated with a deterministic baseline, TAMEV/Jev,
or a frontier-model task as long as the task returns EvalOutput.
"""

from pathlib import Path

from pydantic_knowledge import baseline_task, build_pydantic_evals_dataset
from pydantic_knowledge.cli import load_knowledge_base


def main() -> None:
    knowledge = load_knowledge_base(Path(__file__).with_name("pydantic_ai_docs.py"))
    dataset = build_pydantic_evals_dataset(knowledge)
    report = dataset.evaluate_sync(baseline_task(knowledge, scorer="hybrid"))
    report.print(include_input=True, include_output=True, include_durations=False)


if __name__ == "__main__":
    main()
