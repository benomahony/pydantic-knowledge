# `pydantic_ai.settings`

### `ToolOrOutput`

```python
class ToolOrOutput
```


Restricts function tools while keeping output tools and direct text/image output available.

Use this when you want to control which function tools the model can use
in an agent run while still allowing the agent to complete with structured output,
text, or images.

See the [Tool Choice guide](../tools-advanced.md#tool-choice) for examples.

```python
function_tools: list[str]
```

### `ModelSettings`

```python
class ModelSettings
```


Settings to configure an LLM.

Includes only settings which apply to multiple models / model providers,
though not all of these settings are supported by all models.

Each field's `Supported by:` list names the model classes that put the setting on the wire. A bare
name covers every interface that model serves, so `OpenAI` means both
[`OpenAIChatModel`][pydantic_ai.models.openai.OpenAIChatModel] and
[`OpenAIResponsesModel`][pydantic_ai.models.openai.OpenAIResponsesModel]; a name qualified with an
interface, like `OpenAI Chat Completions`, covers only that one, because the Responses API does
not accept the setting at all.

These lists are parsed and checked against the wire by
`tests/models/test_model_settings_support.py`, so keep the `* Name` bullet shape and put any nuance in
parentheses after the name.

Being listed means Pydantic AI sends the setting, not that the service honors it: the
OpenAI-compatible model classes forward whatever the OpenAI schema accepts, and an individual
provider behind one of them may ignore a field its own API doesn't define, or reject it. Where we
know of such a case it is noted on the entry, but the provider's own API reference is the
authority.

All types must be serializable using Pydantic.

```python
max_tokens: int
```

```python
temperature: float
```

```python
top_p: float
```

```python
top_k: int
```

```python
timeout: int | float | Timeout
```

```python
parallel_tool_calls: bool
```

```python
tool_choice: ToolChoice
```

```python
seed: int
```

```python
presence_penalty: float
```

```python
frequency_penalty: float
```

```python
logit_bias: dict[str, int]
```

```python
stop_sequences: list[str]
```

```python
extra_headers: dict[str, str]
```

```python
thinking: ThinkingLevel
```

```python
service_tier: ServiceTier
```

```python
extra_body: object
```

### `merge_model_settings`

```python
def merge_model_settings(base: ModelSettings | None, overrides: ModelSettings | None) -> ModelSettings | None
```


Merge two sets of model settings, preferring the overrides.

A common use case is: merge_model_settings(<agent settings>, <run settings>)