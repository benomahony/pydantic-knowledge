# `pydantic_evals.online`

Online evaluation — attach evaluators to live functions for automatic background evaluation.

This module provides the infrastructure for running evaluators on production (or staging) traffic.
The same `Evaluator` instances used with `Dataset.evaluate()` work here, the difference is in how
they are wired up (decorator vs dataset) rather than what they are.

Example:
```python
from dataclasses import dataclass

from pydantic_evals.evaluators import Evaluator, EvaluatorContext
from pydantic_evals.online import evaluate


@dataclass
class IsNonEmpty(Evaluator):
    def evaluate(self, ctx: EvaluatorContext) -> bool:
        return bool(ctx.output)


@evaluate(IsNonEmpty())
async def my_function(x: int) -> int:
    return x
```

### `SamplingContext`

```python
class SamplingContext
```


Context available when deciding whether to sample an evaluator.

Contains the information available *before* the decorated function runs — the evaluator
instance, function inputs, config metadata, and a per-call random seed. The function's
output and duration are not yet available at sampling time.

```python
evaluator: Evaluator
```

```python
inputs: Any
```

```python
metadata: dict[str, Any] | None
```

```python
call_seed: float
```

### `disable_evaluation`

```python
def disable_evaluation() -> Generator[None]
```


Context manager to disable all online evaluation in the current context.

When active, decorated functions still execute normally but no evaluators are dispatched.

### `SpanReference`

```python
class SpanReference
```


Identifies a span that evaluation results should be associated with.

Used by sinks to associate evaluation results with the original function execution span.

```python
trace_id: str
```

```python
span_id: str
```

### `OnlineEvaluator`

```python
class OnlineEvaluator
```


Wraps an `Evaluator` with per-evaluator online configuration.

Different evaluators often need different settings — a cheap heuristic should
run on 100% of traffic while an expensive LLM judge might run on only 1%.

```python
evaluator: Evaluator
```

```python
sample_rate: float | Callable[[SamplingContext], float | bool] | None = None
```

```python
max_concurrency: int = 10
```

```python
sink: EvaluationSink | Sequence[EvaluationSink | SinkCallback] | SinkCallback | None = None
```

```python
on_max_concurrency: OnMaxConcurrencyCallback | None = None
```

```python
on_sampling_error: OnSamplingErrorCallback | None = None
```

```python
on_error: OnErrorCallback | None = None
```

```python
run_on_errors: bool = False
```

### `EvaluatorContextSource`

```python
class EvaluatorContextSource
```


Protocol for retrieving stored evaluator contexts.

Implementations reconstruct [`EvaluatorContext`][pydantic_evals.evaluators.EvaluatorContext]
objects from stored traces (e.g., Logfire). The batch method allows fetching contexts
for multiple spans in a single call.

#### `fetch`

```python
async def fetch(self, span: SpanReference) -> EvaluatorContext
```


Fetch an evaluator context for a single span.

Args:
    span: Reference to the span to fetch context for.

Returns:
    The evaluator context for the span.

#### `fetch_many`

```python
async def fetch_many(self, spans: Sequence[SpanReference]) -> list[EvaluatorContext]
```


Fetch evaluator contexts for multiple spans in a single batch.

Args:
    spans: References to the spans to fetch context for.

Returns:
    Evaluator contexts in the same order as the input spans.

### `run_evaluators`

```python
async def run_evaluators(evaluators: Sequence[Evaluator], context: EvaluatorContext) -> tuple[list[EvaluationResult], list[EvaluatorFailure]]
```


Run evaluators on a context and return results.

Useful for re-running evaluators from stored data.

Args:
    evaluators: The evaluators to run.
    context: The evaluator context to evaluate against.

Returns:
    A tuple of (results, failures).











### `OnlineEvalConfig`

```python
class OnlineEvalConfig
```


Holds cross-evaluator defaults for online evaluation.

Create instances for different evaluation configurations, or use the global
`DEFAULT_CONFIG` via the module-level `evaluate()` and `configure()` functions.

```python
default_sink: EvaluationSink | Sequence[EvaluationSink | SinkCallback] | SinkCallback | None = None
```

```python
default_sample_rate: float | Callable[[SamplingContext], float | bool] = 1.0
```

```python
emit_otel_events: bool = True
```

```python
include_baggage: bool = True
```

```python
sampling_mode: SamplingMode = 'independent'
```

```python
enabled: bool = True
```

```python
metadata: dict[str, Any] | None = None
```

```python
on_max_concurrency: OnMaxConcurrencyCallback | None = None
```

```python
on_sampling_error: OnSamplingErrorCallback | None = None
```

```python
on_error: OnErrorCallback | None = None
```

#### `evaluate`

```python
def evaluate(self, *evaluators: Evaluator | OnlineEvaluator, target: str | None=None, msg_template: LiteralString | None=None, span_name: str | None=None, extract_args: bool | Iterable[str]=False, record_return: bool=False) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]
```


Decorator to attach online evaluators to a function.

Each decorated call opens a dedicated span representing the function
invocation — evaluator events are parented to this span, and the span
itself appears in the user's configured OTel/logfire traces.

Bare `Evaluator` instances are auto-wrapped in `OnlineEvaluator` at decoration time
(so concurrency semaphores are shared across calls). Their `sample_rate` defaults to
`None`, which resolves to the config's `default_sample_rate` at each call — so
changes to the config after decoration take effect.

To version an evaluator, override
[`get_evaluator_version`][pydantic_evals.evaluators.Evaluator.get_evaluator_version] on the
`Evaluator` subclass — the framework calls it at dispatch time and records the value on every
[`EvaluationResult`][pydantic_evals.evaluators.EvaluationResult] and
[`EvaluatorFailure`][pydantic_evals.evaluators.EvaluatorFailure] the evaluator emits:

```python
from dataclasses import dataclass

from pydantic_evals.evaluators import Evaluator, EvaluatorContext
from pydantic_evals.online import evaluate


@dataclass
class Tone(Evaluator):
    def evaluate(self, ctx: EvaluatorContext) -> str:
        return 'neutral'

    def get_evaluator_version(self) -> str | None:
        return 'v2'


@evaluate(Tone())
async def summarize(text: str) -> str:
    return text
```

Args:
    *evaluators: Evaluators to attach. Can be `Evaluator` or `OnlineEvaluator` instances.
    target: Name of the thing being evaluated. Written to sinks and emitted
        OTel events as `gen_ai.evaluation.target`. Defaults to the decorated
        function's `__name__` when omitted.
    msg_template: Template for the call span's message. Defaults to
        `"Calling {module}.{qualname}"` like `@logfire.instrument`.
        When logfire is installed, `{arg=}`-style placeholders in the
        template are formatted against the function's arguments.
    span_name: Override for the call span's name. Defaults to `msg_template`.
    extract_args: Whether to record function arguments as span attributes.
        `False` (default) records nothing; `True` records all bound arguments;
        an iterable of names records only those arguments. Requires logfire
        to be installed so arguments are serialised with their JSON schema —
        raises `RuntimeError` at decoration time otherwise.
    record_return: Whether to record the function's return value as a `return`
        span attribute. Requires logfire for the same reason as `extract_args`.

Returns:
    A decorator that wraps the function with online evaluation.

#### `should_evaluate`

```python
def should_evaluate(self) -> bool
```


Whether evaluators with this config should run, based on the current settings and context.











### `evaluate`

```python
def evaluate(*evaluators: Evaluator | OnlineEvaluator, target: str | None=None, msg_template: LiteralString | None=None, span_name: str | None=None, extract_args: bool | Iterable[str]=False, record_return: bool=False) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]
```


Decorator to attach online evaluators to a function using the global default config.

Equivalent to `DEFAULT_CONFIG.evaluate(...)`.

Args:
    *evaluators: Evaluators to attach. Can be `Evaluator` or `OnlineEvaluator` instances.
    target: Name of the thing being evaluated. Written to sinks and emitted
        OTel events as `gen_ai.evaluation.target`. Defaults to the decorated
        function's `__name__` when omitted.
    msg_template: Template for the call span's message. Defaults to
        `"Calling {module}.{qualname}"` like `@logfire.instrument`.
    span_name: Override for the call span's name. Defaults to `msg_template`.
    extract_args: Whether to record function arguments as span attributes.
        `False` (default) records nothing; `True` records all bound arguments;
        an iterable of names records only those arguments. Requires logfire
        to be installed — raises `RuntimeError` at decoration time otherwise.
    record_return: Whether to record the function's return value as a `return`
        span attribute. Requires logfire for the same reason as `extract_args`.

Returns:
    A decorator that wraps the function with online evaluation.

Example:
```python
from dataclasses import dataclass

from pydantic_evals.evaluators import Evaluator, EvaluatorContext
from pydantic_evals.online import evaluate


@dataclass
class IsNonEmpty(Evaluator):
    def evaluate(self, ctx: EvaluatorContext) -> bool:
        return bool(ctx.output)


@evaluate(IsNonEmpty())
async def my_function(x: int) -> int:
    return x
```

### `configure`

```python
def configure(*, default_sink: EvaluationSink | Sequence[EvaluationSink | SinkCallback] | SinkCallback | None | Unset=UNSET, default_sample_rate: float | Callable[[SamplingContext], float | bool] | Unset=UNSET, sampling_mode: SamplingMode | Unset=UNSET, enabled: bool | Unset=UNSET, metadata: dict[str, Any] | None | Unset=UNSET, on_max_concurrency: OnMaxConcurrencyCallback | None | Unset=UNSET, on_sampling_error: OnSamplingErrorCallback | None | Unset=UNSET, on_error: OnErrorCallback | None | Unset=UNSET, emit_otel_events: bool | Unset=UNSET, include_baggage: bool | Unset=UNSET) -> None
```


Configure the global default `OnlineEvalConfig`.

Only provided values are updated; unset arguments are ignored.
Pass `None` explicitly to clear `default_sink`, `metadata`, `on_max_concurrency`,
`on_sampling_error`, or `on_error`.

Args:
    default_sink: Default sink(s) for evaluators. Pass `None` to clear.
    default_sample_rate: Default sample rate for evaluators.
    sampling_mode: Sampling mode (`'independent'` or `'correlated'`).
    enabled: Whether online evaluation is enabled.
    metadata: Metadata to include in evaluator contexts. Pass `None` to clear.
    on_max_concurrency: Default handler for dropped evaluations. Pass `None` to clear.
    on_sampling_error: Default handler for sample_rate exceptions. Pass `None` to clear.
    on_error: Default handler for pipeline exceptions. Pass `None` to clear.
    emit_otel_events: Whether to emit `gen_ai.evaluation.result` OTel events.
    include_baggage: Whether to copy current OTel baggage onto every emitted event.

### `wait_for_evaluations`

```python
async def wait_for_evaluations(*, timeout: float=30.0) -> None
```


Wait for all pending background evaluation tasks and threads to complete.

This is useful in tests to deterministically wait for background evaluators
to finish instead of relying on timing-based sleeps.

For async decorated functions, evaluators run as tasks on the caller's event loop
and are awaited directly. For sync decorated functions, evaluators run in background
threads which are joined with the given timeout.

Args:
    timeout: Maximum seconds to wait for each background thread. Defaults to 30.