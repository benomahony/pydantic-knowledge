# `pydantic_ai.models.anthropic`

## Setup

For details on how to set up authentication with this model, see [model configuration for Anthropic](../../models/anthropic.md).









### `AnthropicStaleThinkingBlockWarning`

```python
class AnthropicStaleThinkingBlockWarning
```


Warning raised when Anthropic rejected a replayed thinking block and Pydantic AI retried without it.

Claude Fable 5.1, Claude Opus 5.5, and Claude Sonnet 5.5 bind each thinking block to the
conversation prefix that produced it and reject a replay once that prefix changes — which a dynamic
[instructions][pydantic_ai.Agent.instructions] function and a
[filtered toolset](../toolsets.md#filtering-tools) both do by design. Anthropic enforces the
check for accounts created on or after 2026-08-31; for older accounts it records the mismatch
and acts on it only if the request asks it to.

Pydantic AI therefore asks for nothing by default, so an older account keeps replaying its
reasoning untouched. Where the check is enforced, the rejected request is retried once with
`thinking.block_binding.prefix_mismatch_behavior='drop_block'`: the stale block is dropped, the
run continues, and later requests carrying that response history keep asking for the drop as
Anthropic requires. The drop is recorded on
[`ModelResponse.provider_details`][pydantic_ai.messages.ModelResponse.provider_details] and as
an `anthropic.input_transformations` span event.

### `AnthropicModelSettings`

```python
class AnthropicModelSettings
```


Settings used for an Anthropic model request.

```python
anthropic_metadata: BetaMetadataParam
```

```python
anthropic_thinking: BetaThinkingConfigParam
```

```python
anthropic_cache_tool_definitions: bool | Literal['5m', '1h']
```

```python
anthropic_service_tier: Literal['auto', 'standard_only']
```

```python
anthropic_cache_instructions: bool | Literal['5m', '1h']
```

```python
anthropic_cache_messages: bool | Literal['5m', '1h']
```

```python
anthropic_cache: bool | Literal['5m', '1h']
```

```python
anthropic_effort: AnthropicEffort | None
```

```python
anthropic_task_budget: AnthropicTaskBudget
```

```python
anthropic_container: BetaContainerParams | str | Literal[False]
```

```python
anthropic_code_execution_tool_version: AnthropicCodeExecutionToolVersion | Literal['auto']
```

```python
anthropic_eager_input_streaming: bool
```

```python
anthropic_betas: list[AnthropicBetaParam]
```

```python
anthropic_speed: Literal['standard', 'fast']
```

```python
anthropic_context_management: BetaContextManagementConfigParam
```



























### `AnthropicModel`

```python
class AnthropicModel
```


A model that uses the Anthropic API.

Internally, this uses the [Anthropic Python client](https://github.com/anthropics/anthropic-sdk-python) to interact with the API.

Apart from `__init__`, all methods are private or match those of the base class.

```python
_model_name: AnthropicModelName = field(repr=False)
```

```python
_provider: Provider[AsyncAnthropicClient] = field(repr=False)
```



#### `model_name`

```python
def model_name(self) -> AnthropicModelName
```


The model name.

#### `resolve_cache_retention`

```python
def resolve_cache_retention(self, model_settings: ModelSettings | None) -> timedelta | None
```


Resolve the longest retention requested by active Anthropic cache settings.

#### `system`

```python
def system(self) -> str
```


The model provider.

#### `profile`

```python
def profile(self) -> AnthropicModelProfile
```


The model profile.

Anthropic web-tool availability depends on both model support and the client/platform, so the
profile's `supported_native_tools` and `anthropic_supports_dynamic_filtering` are narrowed here
for clients that don't support them (e.g. Bedrock, Vertex). `supports_inline_system_prompts` is
narrowed the same way, and for the same reason: serving a `{'role': 'system'}` entry is a fact
about the transport as much as about the model. Thinking-block binding is likewise narrowed, but
by client class rather than by base URL: its beta and drop-block retry are verified against
Anthropic's Messages API, which a proxied or gateway `AsyncAnthropic` still reaches.

#### `tool_addition_mode`

```python
def tool_addition_mode(self) -> Literal['by_reference'] | None
```


The effective addition mode, narrowed for transports without inline system messages.

#### `supported_native_tools`

```python
def supported_native_tools(cls) -> frozenset[type[AbstractNativeTool]]
```


The set of builtin tool types this model can handle.

















































### `AnthropicCompaction`

```python
class AnthropicCompaction
```


Compaction capability for Anthropic models.

Configures automatic context management via Anthropic's `context_management`
API parameter. Compaction triggers server-side when input tokens exceed
the configured threshold.

Example usage:

```python {test="skip"}
from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicCompaction

agent = Agent(
    'anthropic:claude-sonnet-4-6',
    capabilities=[AnthropicCompaction(token_threshold=100_000)],
)
```





### `AnthropicStreamedResponse`

```python
class AnthropicStreamedResponse
```


Implementation of `StreamedResponse` for Anthropic models.

```python
_model_name: AnthropicModelName
```

```python
_response: _AnthropicEventStream
```

```python
_provider_name: str
```

```python
_model_id_namespace: str
```

```python
_provider_url: str
```

```python
_enabled_server_tool_names: frozenset[str]
```

```python
_timestamp: datetime = field(default_factory=_utils.now_utc)
```

#### `model_name`

```python
def model_name(self) -> AnthropicModelName
```


Get the model name of the response.

#### `provider_name`

```python
def provider_name(self) -> str
```


Get the provider name.

#### `provider_url`

```python
def provider_url(self) -> str
```


Get the provider base URL.

#### `timestamp`

```python
def timestamp(self) -> datetime
```


Get the timestamp of the response.



























