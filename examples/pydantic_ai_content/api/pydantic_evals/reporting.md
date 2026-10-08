# `pydantic_evals.reporting`

### `ReportCase`

```python
class ReportCase
```


A single case in an evaluation report.

```python
name: str
```

```python
inputs: InputsT
```

```python
metadata: MetadataT | None
```

```python
expected_output: OutputT | None
```

```python
output: OutputT
```

```python
metrics: dict[str, float | int]
```

```python
attributes: dict[str, Any]
```

```python
scores: dict[str, EvaluationResult[int | float]]
```

```python
labels: dict[str, EvaluationResult[str]]
```

```python
assertions: dict[str, EvaluationResult[bool]]
```

```python
task_duration: float
```

```python
total_duration: float
```

```python
source_case_name: str | None = None
```

```python
trace_id: str | None = None
```

```python
span_id: str | None = None
```

```python
evaluator_failures: list[EvaluatorFailure] = field(default_factory=list[EvaluatorFailure])
```

### `ReportCaseFailure`

```python
class ReportCaseFailure
```


A single case in an evaluation report that failed due to an error during task execution.

```python
name: str
```

```python
inputs: InputsT
```

```python
metadata: MetadataT | None
```

```python
expected_output: OutputT | None
```

```python
error_message: str
```

```python
error_stacktrace: str
```

```python
source_case_name: str | None = None
```

```python
trace_id: str | None = None
```

```python
span_id: str | None = None
```

### `ReportCaseGroup`

```python
class ReportCaseGroup
```


Grouped results from running the same case multiple times.

This is a computed view, not stored data. Obtain via
`EvaluationReport.case_groups()`.

```python
name: str
```

```python
inputs: InputsT
```

```python
metadata: MetadataT | None
```

```python
expected_output: OutputT | None
```

```python
runs: Sequence[ReportCase[InputsT, OutputT, MetadataT]]
```

```python
failures: Sequence[ReportCaseFailure[InputsT, OutputT, MetadataT]]
```

```python
summary: ReportCaseAggregate
```

### `ReportCaseAggregate`

```python
class ReportCaseAggregate
```


A synthetic case that summarizes a set of cases.

```python
name: str
```

```python
scores: dict[str, float | int]
```

```python
labels: dict[str, dict[str, float]]
```

```python
metrics: dict[str, float | int]
```

```python
assertions: float | None
```

```python
task_duration: float
```

```python
total_duration: float
```

#### `average`

```python
def average(cases: list[ReportCase]) -> ReportCaseAggregate
```


Produce a synthetic "summary" case by averaging quantitative attributes.

#### `average_from_aggregates`

```python
def average_from_aggregates(aggregates: list[ReportCaseAggregate]) -> ReportCaseAggregate
```


Average across multiple aggregates (used for multi-run experiment summaries).

### `EvaluationReport`

```python
class EvaluationReport
```


A report of the results of evaluating a model on a set of cases.

```python
name: str
```

```python
cases: list[ReportCase[InputsT, OutputT, MetadataT]]
```

```python
failures: list[ReportCaseFailure[InputsT, OutputT, MetadataT]] = field(default_factory=list[ReportCaseFailure[InputsT, OutputT, MetadataT]])
```

```python
analyses: list[ReportAnalysis] = field(default_factory=list[ReportAnalysis])
```

```python
report_evaluator_failures: list[EvaluatorFailure] = field(default_factory=list[EvaluatorFailure])
```

```python
experiment_metadata: dict[str, Any] | None = None
```

```python
trace_id: str | None = None
```

```python
span_id: str | None = None
```

#### `case_groups`

```python
def case_groups(self) -> list[ReportCaseGroup[InputsT, OutputT, MetadataT]] | None
```


Group cases by source_case_name and compute per-group aggregates.

Returns None if no cases have source_case_name set (i.e., single-run experiment).

#### `averages`

```python
def averages(self) -> ReportCaseAggregate | None
```


Aggregate scores, labels, and metrics averaged across the report's cases.

For multi-run reports, per-group summaries are averaged instead; returns `None` when there
is nothing to aggregate.

#### `render`

```python
def render(self, width: int | None=None, baseline: EvaluationReport[InputsT, OutputT, MetadataT] | None=None, *, include_input: bool=False, include_metadata: bool=False, include_expected_output: bool=False, include_output: bool=False, include_durations: bool=True, include_total_duration: bool=False, include_removed_cases: bool=False, include_averages: bool=True, include_errors: bool=True, include_error_stacktrace: bool=False, include_evaluator_failures: bool=True, include_analyses: bool=True, input_config: RenderValueConfig | None=None, metadata_config: RenderValueConfig | None=None, output_config: RenderValueConfig | None=None, score_configs: dict[str, RenderNumberConfig] | None=None, label_configs: dict[str, RenderValueConfig] | None=None, metric_configs: dict[str, RenderNumberConfig] | None=None, duration_config: RenderNumberConfig | None=None, include_reasons: bool=False) -> str
```


Render this report to a nicely-formatted string, optionally comparing it to a baseline report.

If you want more control over the output, use `console_table` instead and pass it to `rich.Console.print`.

#### `print`

```python
def print(self, width: int | None=None, baseline: EvaluationReport[InputsT, OutputT, MetadataT] | None=None, *, console: Console | None=None, include_input: bool=False, include_metadata: bool=False, include_expected_output: bool=False, include_output: bool=False, include_durations: bool=True, include_total_duration: bool=False, include_removed_cases: bool=False, include_averages: bool=True, include_errors: bool=True, include_error_stacktrace: bool=False, include_evaluator_failures: bool=True, include_analyses: bool=True, input_config: RenderValueConfig | None=None, metadata_config: RenderValueConfig | None=None, output_config: RenderValueConfig | None=None, score_configs: dict[str, RenderNumberConfig] | None=None, label_configs: dict[str, RenderValueConfig] | None=None, metric_configs: dict[str, RenderNumberConfig] | None=None, duration_config: RenderNumberConfig | None=None, include_reasons: bool=False) -> None
```


Print this report to the console, optionally comparing it to a baseline report.

On a console `rich` reports as ASCII-only — a non-UTF-8 stream, as Windows produces when stdout is
redirected to a file or a pipe — `v`, `x` and `->` stand in for the `✔`, `✗` and `→` glyphs, and default
sub-millisecond duration formatters use `us` instead of `µs`.

If you want more control over the output, use `console_table` instead and pass it to `rich.Console.print`,
forwarding `ascii_only=console.options.ascii_only` from the console you print to.

#### `console_table`

```python
def console_table(self, baseline: EvaluationReport[InputsT, OutputT, MetadataT] | None=None, *, include_input: bool=False, include_metadata: bool=False, include_expected_output: bool=False, include_output: bool=False, include_durations: bool=True, include_total_duration: bool=False, include_removed_cases: bool=False, include_averages: bool=True, include_evaluator_failures: bool=True, input_config: RenderValueConfig | None=None, metadata_config: RenderValueConfig | None=None, output_config: RenderValueConfig | None=None, score_configs: dict[str, RenderNumberConfig] | None=None, label_configs: dict[str, RenderValueConfig] | None=None, metric_configs: dict[str, RenderNumberConfig] | None=None, duration_config: RenderNumberConfig | None=None, include_reasons: bool=False, with_title: bool=True, ascii_only: bool=False) -> RenderableType
```


Return a table containing the data from this report.

If a baseline is provided, returns a diff between this report and the baseline report.
Optionally include input and output details.

`ascii_only` renders `v`, `x` and `->` in place of the `✔`, `✗` and `→` glyphs, and uses `us` instead of
`µs` from the default sub-millisecond duration formatters. Only the caller holding that console can answer
this, so it defaults to `False`; pass `ascii_only=console.options.ascii_only` from the console you print the
table to.



#### `failures_table`

```python
def failures_table(self, *, include_input: bool=False, include_metadata: bool=False, include_expected_output: bool=False, include_error_message: bool=True, include_error_stacktrace: bool=True, input_config: RenderValueConfig | None=None, metadata_config: RenderValueConfig | None=None) -> RenderableType
```


Return a table containing the failures in this report.



### `RenderValueConfig`

```python
class RenderValueConfig
```


A configuration for rendering a values in an Evaluation report.

```python
value_formatter: str | Callable[[Any], str]
```

```python
diff_checker: Callable[[Any, Any], bool] | None
```

```python
diff_formatter: Callable[[Any, Any], str | None] | None
```

```python
diff_style: str
```

### `RenderNumberConfig`

```python
class RenderNumberConfig
```


A configuration for rendering a particular score or metric in an Evaluation report.

See the implementation of `_RenderNumber` for more clarity on how these parameters affect the rendering.

```python
value_formatter: str | Callable[[float | int], str]
```

```python
diff_formatter: str | Callable[[float | int, float | int], str | None] | None
```

```python
diff_atol: float
```

```python
diff_rtol: float
```

```python
diff_increase_style: str
```

```python
diff_decrease_style: str
```



### `EvaluationRenderer`

```python
class EvaluationRenderer
```


A class for rendering an EvalReport or the diff between two EvalReports.

```python
include_input: bool
```

```python
include_metadata: bool
```

```python
include_expected_output: bool
```

```python
include_output: bool
```

```python
include_durations: bool
```

```python
include_total_duration: bool
```

```python
include_removed_cases: bool
```

```python
include_averages: bool
```

```python
input_config: RenderValueConfig
```

```python
metadata_config: RenderValueConfig
```

```python
output_config: RenderValueConfig
```

```python
score_configs: dict[str, RenderNumberConfig]
```

```python
label_configs: dict[str, RenderValueConfig]
```

```python
metric_configs: dict[str, RenderNumberConfig]
```

```python
duration_config: RenderNumberConfig
```

```python
include_reasons: bool
```

```python
include_error_message: bool
```

```python
include_error_stacktrace: bool
```

```python
include_evaluator_failures: bool
```

```python
ascii_only: bool = False
```

#### `build_table`

```python
def build_table(self, report: EvaluationReport, *, with_title: bool=True) -> Table
```


Build a table for the report.

Args:
    report: The evaluation report to render
    with_title: Whether to include the title in the table (default True)

Returns:
    A Rich Table object

#### `build_diff_table`

```python
def build_diff_table(self, report: EvaluationReport, baseline: EvaluationReport, *, with_title: bool=True) -> Table
```


Build a diff table comparing report to baseline.

Args:
    report: The evaluation report to compare
    baseline: The baseline report to compare against
    with_title: Whether to include the title in the table (default True)

Returns:
    A Rich Table object

