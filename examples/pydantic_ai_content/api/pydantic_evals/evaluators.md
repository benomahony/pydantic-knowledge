# `pydantic_evals.evaluators`

### `GradingOutput`

```python
class GradingOutput
```


The output of a grading operation.

```python
reason: str = Field(description=_JUDGE_REASON_DESCRIPTION)
```

```python
pass_: bool = Field(validation_alias='pass', serialization_alias='pass')
```

```python
score: float
```





### `judge_output`

```python
async def judge_output(output: Any, rubric: str, model: models.Model | models.KnownModelName | str | None=None, model_settings: ModelSettings | None=None) -> GradingOutput
```


Judge the output of a model based on a rubric.

If the model is not specified, a default model is used. The default model starts as 'openai:gpt-5.2',
but this can be changed using the `set_default_judge_model` function.

### `judge_input_output`

```python
async def judge_input_output(inputs: Any, output: Any, rubric: str, model: models.Model | models.KnownModelName | str | None=None, model_settings: ModelSettings | None=None) -> GradingOutput
```


Judge the output of a model based on the inputs and a rubric.

If the model is not specified, a default model is used. The default model starts as 'openai:gpt-5.2',
but this can be changed using the `set_default_judge_model` function.

### `judge_input_output_expected`

```python
async def judge_input_output_expected(inputs: Any, output: Any, expected_output: Any, rubric: str, model: models.Model | models.KnownModelName | str | None=None, model_settings: ModelSettings | None=None) -> GradingOutput
```


Judge the output of a model based on the inputs and a rubric.

If the model is not specified, a default model is used. The default model starts as 'openai:gpt-5.2',
but this can be changed using the `set_default_judge_model` function.

### `judge_output_expected`

```python
async def judge_output_expected(output: Any, expected_output: Any, rubric: str, model: models.Model | models.KnownModelName | str | None=None, model_settings: ModelSettings | None=None) -> GradingOutput
```


Judge the output of a model based on the expected output, output, and a rubric.

If the model is not specified, a default model is used. The default model starts as 'openai:gpt-5.2',
but this can be changed using the `set_default_judge_model` function.

### `set_default_judge_model`

```python
def set_default_judge_model(model: models.Model | models.KnownModelName) -> None
```


Set the default model used for judging.

This model is used if `None` is passed to the `model` argument of `judge_output` and `judge_input_output`.





### `GEvalOutput`

```python
class GEvalOutput
```


The output of a G-Eval grading operation.

G-Eval asks the judge to emit a short chain-of-thought `reason` followed by an
integer `score` in a user-specified range (see [`judge_g_eval`][pydantic_evals.evaluators.llm_as_a_judge.judge_g_eval]).

```python
reason: str
```

```python
score: int
```



### `judge_g_eval`

```python
async def judge_g_eval(output: Any, criteria: str, evaluation_steps: Sequence[str], score_range: tuple[int, int]=(1, 5), inputs: Any | None=None, model: models.Model | models.KnownModelName | str | None=None, model_settings: ModelSettings | None=None) -> GEvalOutput
```


Judge an output using a G-Eval style chain-of-thought prompt.

This is a simplified implementation of G-Eval (Liu et al., 2023, "G-Eval: NLG Evaluation using
GPT-4 with Better Human Alignment"). The original paper computes an expectation over the
distribution of score tokens using log-probs. We skip that step and simply ask the model for
a direct integer score. This keeps the evaluator provider-agnostic at the cost of some
correlation with human judgments.

Args:
    output: The output being evaluated.
    criteria: The aspect being evaluated (e.g. "coherence", "fluency").
    evaluation_steps: Explicit chain-of-thought steps the judge should follow.
    score_range: Inclusive `(min, max)` integer score range.
    inputs: Optional inputs/context to show alongside the output.
    model: The model to use. If not specified, the default judge model is used.
    model_settings: Optional model settings.

Returns:
    A [`GEvalOutput`][pydantic_evals.evaluators.llm_as_a_judge.GEvalOutput] containing
    the judge's reasoning and integer score.

Raises:
    UserError: If the judge cannot generate the required reason.
    ValueError: If `score_range` is invalid, `evaluation_steps` is empty, or the judge
        returns a score outside the range.