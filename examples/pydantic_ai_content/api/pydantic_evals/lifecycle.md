# `pydantic_evals.lifecycle`

Case lifecycle hooks for pydantic evals.

This module provides the [`CaseLifecycle`][pydantic_evals.lifecycle.CaseLifecycle] class,
which allows defining setup, context preparation, and teardown hooks that run at different
stages of case evaluation.

### `CaseLifecycle`

```python
class CaseLifecycle
```


Per-case lifecycle hooks for evaluation.

A new instance is created for each case during evaluation. Subclass and override
any methods you need — all methods are no-ops by default.

The evaluation flow for each case is:

1. `setup()` — called before task execution
2. Task runs
3. `prepare_context()` — called after task, before evaluators; can enrich metrics/attributes
4. Evaluators run
5. `teardown()` — called after evaluators complete; receives the full result (or `None` when interrupted)

Exceptions raised by `setup()` or `prepare_context()` are caught and recorded as
a `ReportCaseFailure`; `teardown()` is still called afterward so you can clean up.
Exceptions raised by `teardown()` propagate to the caller and may abort the evaluation.
If your teardown may raise and you don't want it to crash the evaluation run,
handle exceptions within your `teardown()` implementation itself.

Args:
    case: The case being evaluated. Available as `self.case` in all hooks.

Example:
    ```python {lint="skip"}
    from pydantic_evals import Case, Dataset
    from pydantic_evals.evaluators.context import EvaluatorContext
    from pydantic_evals.lifecycle import CaseLifecycle

    class EnrichMetrics(CaseLifecycle):
        async def prepare_context(self, ctx: EvaluatorContext) -> EvaluatorContext:
            ctx.metrics['custom_metric'] = 42
            return ctx

    dataset = Dataset(name='lifecycle_demo', cases=[Case(name='test', inputs='hello')])
    report = dataset.evaluate_sync(lambda inputs: inputs.upper(), lifecycle=EnrichMetrics)
    print(report.cases[0].metrics['custom_metric'])
    #> 42
    ```

#### `case`

```python
def case(self) -> Case[InputsT, OutputT, MetadataT]
```


The case being evaluated.

#### `setup`

```python
async def setup(self) -> None
```


Called before task execution.

Override to perform per-case resource setup (e.g., create a test database,
start a service). The case metadata is available via `self.case.metadata`.

#### `prepare_context`

```python
async def prepare_context(self, ctx: EvaluatorContext[InputsT, OutputT, MetadataT]) -> EvaluatorContext[InputsT, OutputT, MetadataT]
```


Called after the task completes, before evaluators run.

Override to enrich the evaluator context with additional metrics or attributes
derived from the task output, span tree, or external state.

Args:
    ctx: The evaluator context produced by the task run.

Returns:
    The (possibly modified) evaluator context to pass to evaluators.

#### `teardown`

```python
async def teardown(self, result: ReportCase[InputsT, OutputT, MetadataT] | ReportCaseFailure[InputsT, OutputT, MetadataT] | None) -> None
```


Called after evaluators complete.

Override to perform per-case resource cleanup. The result is provided so that
teardown logic can vary based on success/failure (e.g., keep resources up for
inspection on failure).

Args:
    result: The evaluation result — a `ReportCase` (success), `ReportCaseFailure`,
        or `None` if the run ended without a report object (e.g. cancellation).