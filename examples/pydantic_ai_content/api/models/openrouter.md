# `pydantic_ai.models.openrouter`

## Setup

For details on how to set up authentication with this model, see [model configuration for OpenRouter](../../models/openrouter.md).







### `OpenRouterProviderConfig`

```python
class OpenRouterProviderConfig
```


Represents the 'Provider' object from the OpenRouter API.

```python
order: list[OpenRouterProviderName]
```

```python
allow_fallbacks: bool
```

```python
require_parameters: bool
```

```python
data_collection: Literal['allow', 'deny']
```

```python
zdr: bool
```

```python
only: list[OpenRouterProviderName]
```

```python
ignore: list[str]
```

```python
quantizations: list[Literal['int4', 'int8', 'fp4', 'mxfp4', 'nvfp4', 'fp6', 'fp8', 'mxfp8', 'fp16', 'bf16', 'fp32', 'unknown']]
```

```python
sort: Literal['price', 'throughput', 'latency', 'exacto']
```

```python
max_price: _OpenRouterMaxPrice
```

### `OpenRouterReasoning`

```python
class OpenRouterReasoning
```


Configuration for reasoning tokens in OpenRouter requests.

Reasoning tokens allow models to show their step-by-step thinking process.
You can configure this using either OpenAI-style effort levels or Anthropic-style
token limits, but not both simultaneously.

```python
effort: Literal['xhigh', 'high', 'medium', 'low', 'minimal', 'none']
```

```python
max_tokens: int
```

```python
exclude: bool
```

```python
enabled: bool
```

### `OpenRouterUsageConfig`

```python
class OpenRouterUsageConfig
```


Configuration for OpenRouter usage.

```python
include: bool
```

### `OpenRouterModelSettings`

```python
class OpenRouterModelSettings
```


Settings used for an OpenRouter model request.

```python
openrouter_models: list[str]
```

```python
openrouter_provider: OpenRouterProviderConfig
```

```python
openrouter_preset: str
```

```python
openrouter_transforms: list[OpenRouterTransforms]
```

```python
openrouter_reasoning: OpenRouterReasoning
```

```python
openrouter_usage: OpenRouterUsageConfig
```

```python
openrouter_cache_instructions: OpenRouterCacheTTL
```

```python
openrouter_cache_messages: OpenRouterCacheTTL
```

```python
openrouter_cache_tool_definitions: OpenRouterCacheTTL
```



































### `OpenRouterModel`

```python
class OpenRouterModel
```


Extends OpenAIChatModel to capture extra metadata for Openrouter.



#### `resolve_cache_retention`

```python
def resolve_cache_retention(self, model_settings: ModelSettings | None) -> timedelta | None
```


Resolve the longest explicit retention accepted by OpenRouter's downstream model.









#### `supported_native_tools`

```python
def supported_native_tools(cls) -> frozenset[type[AbstractNativeTool]]
```


Return the set of builtin tool types this model can handle.

OpenRouter supports web search through its server-tool API.

















### `OpenRouterStreamedResponse`

```python
class OpenRouterStreamedResponse
```


Implementation of `StreamedResponse` for OpenRouter models.

```python
_annotations: list[dict[str, Any]] = field(default_factory=list[dict[str, Any]], init=False)
```