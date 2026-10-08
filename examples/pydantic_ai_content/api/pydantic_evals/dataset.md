# `pydantic_evals.dataset`

Dataset management for pydantic evals.

This module provides functionality for creating, loading, saving, and evaluating datasets of test cases.
Each case must have inputs, and can optionally have a name, expected output, metadata, and case-specific evaluators.

Datasets can be loaded from and saved to YAML or JSON files, and can be evaluated against
a task function to produce an evaluation report.





### `Case`

```python
class Case
```


A single row of a [`Dataset`][pydantic_evals.Dataset].

Each case represents a single test scenario with inputs to test. A case may optionally specify a name, expected
outputs to compare against, and arbitrary metadata.

Cases can also have their own specific evaluators which are run in addition to dataset-level evaluators.

Example:
```python
from pydantic_evals import Case

case = Case(
    name='Simple addition',
    inputs={'a': 1, 'b': 2},
    expected_output=3,
    metadata={'description': 'Tests basic addition'},
)
```

```python
name: str | None
```

```python
inputs: InputsT
```

```python
metadata: MetadataT | None = None
```

```python
expected_output: OutputT | None = None
```

```python
evaluators: list[Evaluator[InputsT, OutputT, MetadataT]] = field(default_factory=list[Evaluator[InputsT, OutputT, MetadataT]])
```



### `Dataset`

```python
class Dataset
```


A dataset of test [cases][pydantic_evals.Case].

Datasets allow you to organize a collection of test cases and evaluate them against a task function.
They can be loaded from and saved to YAML or JSON files, and can have dataset-level evaluators that
apply to all cases.

Example:
```python
# Create a dataset with two test cases
from dataclasses import dataclass

from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import Evaluator, EvaluatorContext


@dataclass
class ExactMatch(Evaluator):
    def evaluate(self, ctx: EvaluatorContext) -> bool:
        return ctx.output == ctx.expected_output

dataset = Dataset(
    name='uppercase_tests',
    cases=[
        Case(name='test1', inputs={'text': 'Hello'}, expected_output='HELLO'),
        Case(name='test2', inputs={'text': 'World'}, expected_output='WORLD'),
    ],
    evaluators=[ExactMatch()],
)

# Evaluate the dataset against a task function
async def uppercase(inputs: dict) -> str:
    return inputs['text'].upper()

async def main():
    report = await dataset.evaluate(uppercase)
    report.print()
'''
   Evaluation Summary: uppercase
┏━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Case ID  ┃ Assertions ┃ Duration ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩
│ test1    │ ✔          │     10ms │
├──────────┼────────────┼──────────┤
│ test2    │ ✔          │     10ms │
├──────────┼────────────┼──────────┤
│ Averages │ 100.0% ✔   │     10ms │
└──────────┴────────────┴──────────┘
'''
```

```python
name: str
```

```python
cases: list[Case[InputsT, OutputT, MetadataT]]
```

```python
evaluators: list[Evaluator[InputsT, OutputT, MetadataT]] = []
```

```python
report_evaluators: list[ReportEvaluator[InputsT, OutputT, MetadataT]] = []
```





#### `evaluate`

```python
async def evaluate(self, task: Callable[[InputsT], Awaitable[OutputT]] | Callable[[InputsT], OutputT], *, name: str | None=None, max_concurrency: int | None=None, progress: bool=True, retry_task: RetryConfig | None=None, retry_evaluators: RetryConfig | None=None, task_name: str | None=None, metadata: dict[str, Any] | None=None, repeat: int=1, lifecycle: type[CaseLifecycle[InputsT, OutputT, MetadataT]] | Callable[[Case[InputsT, OutputT, MetadataT]], CaseLifecycle[InputsT, OutputT, MetadataT]] | None=None) -> EvaluationReport[InputsT, OutputT, MetadataT]
```


Evaluates the test cases in the dataset using the given task.

This method runs the task on each case in the dataset, applies evaluators,
and collects results into a report. Cases are run concurrently, limited by `max_concurrency` if specified.

Args:
    task: The task to evaluate. This should be a callable that takes the inputs of the case
        and returns the output.
    name: The name of the experiment being run, this is used to identify the experiment in the report.
        If omitted, the task_name will be used; if that is not specified, the name of the task function is used.
    max_concurrency: The maximum number of concurrent evaluations of the task to allow.
        If None, all cases will be evaluated concurrently.
    progress: Whether to show a progress bar for the evaluation. Defaults to `True`.
    retry_task: Optional retry configuration for the task execution.
    retry_evaluators: Optional retry configuration for evaluator execution.
    task_name: Optional override to the name of the task being executed, otherwise the name of the task
        function will be used.
    metadata: Optional dict of experiment metadata.
    repeat: Number of times to run each case. When > 1, each case is run multiple times and
        results are grouped by the original case name for aggregation. Defaults to 1.
    lifecycle: Optional lifecycle class for per-case setup, context preparation, and teardown hooks.
        A new instance is created for each case. See [`CaseLifecycle`][pydantic_evals.lifecycle.CaseLifecycle].

Returns:
    A report containing the results of the evaluation.

#### `evaluate_sync`

```python
def evaluate_sync(self, task: Callable[[InputsT], Awaitable[OutputT]] | Callable[[InputsT], OutputT], *, name: str | None=None, max_concurrency: int | None=None, progress: bool=True, retry_task: RetryConfig | None=None, retry_evaluators: RetryConfig | None=None, task_name: str | None=None, metadata: dict[str, Any] | None=None, repeat: int=1, lifecycle: type[CaseLifecycle[InputsT, OutputT, MetadataT]] | Callable[[Case[InputsT, OutputT, MetadataT]], CaseLifecycle[InputsT, OutputT, MetadataT]] | None=None) -> EvaluationReport[InputsT, OutputT, MetadataT]
```


Evaluates the test cases in the dataset using the given task.

This is a synchronous wrapper around [`evaluate`][pydantic_evals.dataset.Dataset.evaluate] provided for convenience.

Args:
    task: The task to evaluate. This should be a callable that takes the inputs of the case
        and returns the output.
    name: The name of the experiment being run, this is used to identify the experiment in the report.
        If omitted, the task_name will be used; if that is not specified, the name of the task function is used.
    max_concurrency: The maximum number of concurrent evaluations of the task to allow.
        If None, all cases will be evaluated concurrently.
    progress: Whether to show a progress bar for the evaluation. Defaults to `True`.
    retry_task: Optional retry configuration for the task execution.
    retry_evaluators: Optional retry configuration for evaluator execution.
    task_name: Optional override to the name of the task being executed, otherwise the name of the task
        function will be used.
    metadata: Optional dict of experiment metadata.
    repeat: Number of times to run each case. When > 1, each case is run multiple times and
        results are grouped by the original case name for aggregation. Defaults to 1.
    lifecycle: Optional lifecycle class for per-case setup, context preparation, and teardown hooks.
        A new instance is created for each case. See [`CaseLifecycle`][pydantic_evals.lifecycle.CaseLifecycle].

Returns:
    A report containing the results of the evaluation.

#### `add_case`

```python
def add_case(self, *, name: str | None=None, inputs: InputsT, metadata: MetadataT | None=None, expected_output: OutputT | None=None, evaluators: Sequence[Evaluator[InputsT, OutputT, MetadataT]]=()) -> None
```


Adds a case to the dataset.

This is a convenience method for creating a [`Case`][pydantic_evals.Case] and adding it to the dataset.

Args:
    name: Optional name for the case. If not provided, a generic name will be assigned.
    inputs: The inputs to the task being evaluated.
    metadata: Optional metadata for the case, which can be used by evaluators.
    expected_output: The expected output of the task, used for comparison in evaluators.
    evaluators: Evaluators specific to this case, in addition to dataset-level evaluators.

#### `add_evaluator`

```python
def add_evaluator(self, evaluator: Evaluator[InputsT, OutputT, MetadataT], specific_case: str | None=None) -> None
```


Adds an evaluator to the dataset or a specific case.

Args:
    evaluator: The evaluator to add.
    specific_case: If provided, the evaluator will only be added to the case with this name.
        If None, the evaluator will be added to all cases in the dataset.

Raises:
    ValueError: If `specific_case` is provided but no case with that name exists in the dataset.



#### `from_file`

```python
def from_file(cls, path: Path | str, fmt: Literal['yaml', 'json'] | None=None, custom_evaluator_types: Sequence[type[Evaluator[InputsT, OutputT, MetadataT]]]=(), custom_report_evaluator_types: Sequence[type[ReportEvaluator[InputsT, OutputT, MetadataT]]]=()) -> Self
```


Load a dataset from a file.

Args:
    path: Path to the file to load.
    fmt: Format of the file. If None, the format will be inferred from the file extension.
        Must be either 'yaml' or 'json'.
    custom_evaluator_types: Custom evaluator classes to use when deserializing the dataset.
        These are additional evaluators beyond the default ones.
    custom_report_evaluator_types: Custom report evaluator classes to use when deserializing the dataset.
        These are additional report evaluators beyond the default ones.

Returns:
    A new Dataset instance loaded from the file.

Raises:
    ValidationError: If the file cannot be parsed as a valid dataset.
    ValueError: If the format cannot be inferred from the file extension.

#### `from_text`

```python
def from_text(cls, contents: str, fmt: Literal['yaml', 'json']='yaml', custom_evaluator_types: Sequence[type[Evaluator[InputsT, OutputT, MetadataT]]]=(), custom_report_evaluator_types: Sequence[type[ReportEvaluator[InputsT, OutputT, MetadataT]]]=(), *, default_name: str | None=None) -> Self
```


Load a dataset from a string.

Args:
    contents: The string content to parse.
    fmt: Format of the content. Must be either 'yaml' or 'json'.
    custom_evaluator_types: Custom evaluator classes to use when deserializing the dataset.
        These are additional evaluators beyond the default ones.
    custom_report_evaluator_types: Custom report evaluator classes to use when deserializing the dataset.
        These are additional report evaluators beyond the default ones.
    default_name: Default name of the dataset, to be used if not specified in the serialized contents.

Returns:
    A new Dataset instance parsed from the string.

Raises:
    ValidationError: If the content cannot be parsed as a valid dataset.

#### `from_dict`

```python
def from_dict(cls, data: dict[str, Any], custom_evaluator_types: Sequence[type[Evaluator[InputsT, OutputT, MetadataT]]]=(), custom_report_evaluator_types: Sequence[type[ReportEvaluator[InputsT, OutputT, MetadataT]]]=(), *, default_name: str | None=None) -> Self
```


Load a dataset from a dictionary.

Args:
    data: Dictionary representation of the dataset.
    custom_evaluator_types: Custom evaluator classes to use when deserializing the dataset.
        These are additional evaluators beyond the default ones.
    custom_report_evaluator_types: Custom report evaluator classes to use when deserializing the dataset.
        These are additional report evaluators beyond the default ones.
    default_name: Default name of the dataset, to be used if not specified in the data.

Returns:
    A new Dataset instance created from the dictionary.

Raises:
    ValidationError: If the dictionary cannot be converted to a valid dataset.



#### `to_file`

```python
def to_file(self, path: Path | str, fmt: Literal['yaml', 'json'] | None=None, schema_path: Path | str | None=DEFAULT_SCHEMA_PATH_TEMPLATE, custom_evaluator_types: Sequence[type[Evaluator[InputsT, OutputT, MetadataT]]]=(), custom_report_evaluator_types: Sequence[type[ReportEvaluator[InputsT, OutputT, MetadataT]]]=())
```


Save the dataset to a file.

Args:
    path: Path to save the dataset to.
    fmt: Format to use. If None, the format will be inferred from the file extension.
        Must be either 'yaml' or 'json'.
    schema_path: Path to save the JSON schema to. If None, no schema will be saved.
        Can be a string template with {stem} which will be replaced with the dataset filename stem.
    custom_evaluator_types: Custom evaluator classes to include in the schema.
    custom_report_evaluator_types: Custom report evaluator classes to include in the schema.

#### `model_json_schema_with_evaluators`

```python
def model_json_schema_with_evaluators(cls, custom_evaluator_types: Sequence[type[Evaluator[InputsT, OutputT, MetadataT]]]=(), custom_report_evaluator_types: Sequence[type[ReportEvaluator[InputsT, OutputT, MetadataT]]]=()) -> dict[str, Any]
```


Generate a JSON schema for this dataset type, including evaluator details.

This is useful for generating a schema that can be used to validate YAML-format dataset files.

Args:
    custom_evaluator_types: Custom evaluator classes to include in the schema.
    custom_report_evaluator_types: Custom report evaluator classes to include in the schema.

Returns:
    A dictionary representing the JSON schema.



















### `set_eval_attribute`

```python
def set_eval_attribute(name: str, value: Any) -> None
```


Set an attribute on the current task run.

Args:
    name: The name of the attribute.
    value: The value of the attribute.

### `increment_eval_metric`

```python
def increment_eval_metric(name: str, amount: int | float) -> None
```


Increment a metric on the current task run.

Args:
    name: The name of the metric.
    amount: The amount to increment by.







