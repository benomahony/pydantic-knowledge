# `pydantic_ai.models.openai`

## Setup

For details on how to set up authentication with this model, see [model configuration for OpenAI](../../models/openai.md).





























### `OpenAIPromptCacheOptions`

```python
class OpenAIPromptCacheOptions
```


Options for OpenAI prompt caching on GPT-5.6 models.

```python
mode: Literal['implicit', 'explicit']
```

```python
ttl: Literal['30m']
```

### `OpenAIChatModelSettings`

```python
class OpenAIChatModelSettings
```


Settings used for an OpenAI model request.

```python
openai_reasoning_effort: ReasoningEffort
```

```python
openai_logprobs: bool
```

```python
openai_top_logprobs: int
```

```python
openai_store: bool | None
```

```python
openai_user: str
```

```python
openai_moderation: Moderation
```

```python
openai_service_tier: Literal['auto', 'default', 'flex', 'priority']
```

```python
openai_prediction: ChatCompletionPredictionContentParam
```

```python
openai_prompt_cache_key: str
```

```python
openai_prompt_cache_retention: Literal['in_memory', '24h']
```

```python
openai_prompt_cache_options: OpenAIPromptCacheOptions
```

```python
openai_continuous_usage_stats: bool
```

### `OpenAIResponsesModelSettings`

```python
class OpenAIResponsesModelSettings
```


Settings used for an OpenAI Responses model request.

ALL FIELDS MUST BE `openai_` PREFIXED SO YOU CAN MERGE THEM WITH OTHER MODELS.

```python
openai_native_tools: Sequence[FileSearchToolParam | WebSearchToolParam | ComputerToolParam]
```

```python
openai_reasoning_mode: Literal['standard', 'pro']
```

```python
openai_reasoning_context: Literal['auto', 'current_turn', 'all_turns']
```

```python
openai_reasoning_summary: Literal['detailed', 'concise', 'auto']
```

```python
openai_send_reasoning_ids: bool
```

```python
openai_truncation: Literal['disabled', 'auto']
```

```python
openai_text_verbosity: Literal['low', 'medium', 'high']
```

```python
openai_previous_response_id: Literal['auto'] | str
```

```python
openai_conversation_id: Literal['auto'] | str
```

```python
openai_include_code_execution_outputs: bool
```

```python
openai_include_web_search_sources: bool
```

```python
openai_include_file_search_results: bool
```

```python
openai_include_raw_annotations: bool
```

```python
openai_context_management: list[ContextManagement]
```

```python
openai_background: bool
```



### `OpenAIChatModel`

```python
class OpenAIChatModel
```


A model that uses the OpenAI API.

Internally, this uses the [OpenAI Python client](https://github.com/openai/openai-python) to interact with the API.

Apart from `__init__`, all methods are private or match those of the base class.

```python
_model_name: OpenAIModelName = field(repr=False)
```

```python
_provider: Provider[AsyncOpenAI] = field(repr=False)
```



#### `model_name`

```python
def model_name(self) -> OpenAIModelName
```


The model name.

#### `resolve_cache_retention`

```python
def resolve_cache_retention(self, model_settings: ModelSettings | None) -> timedelta | None
```


Resolve the extended prompt cache retention requested by OpenAI settings.

#### `system`

```python
def system(self) -> str
```


The model provider.

#### `supported_native_tools`

```python
def supported_native_tools(cls) -> frozenset[type[AbstractNativeTool]]
```


Return the set of builtin tool types this model can handle.

#### `profile`

```python
def profile(self) -> OpenAIModelProfile
```


The model profile.

WebSearchTool is only supported if openai_chat_supports_web_search is True.















































### `OpenAIResponsesModel`

```python
class OpenAIResponsesModel
```


A model that uses the OpenAI Responses API.

The [OpenAI Responses API](https://platform.openai.com/docs/api-reference/responses) is the
new API for OpenAI models.

If you are interested in the differences between the Responses API and the Chat Completions API,
see the [OpenAI API docs](https://platform.openai.com/docs/guides/responses-vs-chat-completions).

```python
_model_name: OpenAIModelName = field(repr=False)
```

```python
_provider: Provider[AsyncOpenAI] = field(repr=False)
```



#### `model_name`

```python
def model_name(self) -> OpenAIModelName
```


The model name.

#### `resolve_cache_retention`

```python
def resolve_cache_retention(self, model_settings: ModelSettings | None) -> timedelta | None
```


Resolve the extended prompt cache retention requested by OpenAI settings.

#### `system`

```python
def system(self) -> str
```


The model provider.

#### `cancel_suspended_response`

```python
async def cancel_suspended_response(self, response: ModelResponse) -> None
```


Cancel a suspended background response by cancelling its server-side job.

`responses.cancel` only applies to background responses; calling it on an ordinary
(foreground) response returns a 400. The `provider_details['background']` marker is
stamped from the API's own `response.background` field (see `_process_response` and
`OpenAIResponsesStreamedResponse._track_background`), so it explicitly and reliably
distinguishes a cancellable background job from a normal streamed response that happens
to be interrupted by `cancel()` — no need to infer background mode from the
`continuation_delay` poll interval.

#### `supported_native_tools`

```python
def supported_native_tools(cls) -> frozenset[type[AbstractNativeTool]]
```


Return the set of builtin tool types this model can handle.

#### `compact_messages`

```python
async def compact_messages(self, request_context: ModelRequestContext, *, instructions: str | None=None) -> ModelResponse
```


Compact messages using the OpenAI Responses compaction endpoint.

This calls OpenAI's `responses.compact` API to produce an encrypted compaction
that summarizes the conversation history. The returned `ModelResponse` contains
a single `CompactionPart` that must be round-tripped in subsequent requests.

Args:
    request_context: The model request context containing messages, settings, and parameters.
    instructions: Optional custom instructions for the compaction summarization.
        If provided, these override the agent-level instructions.

Returns:
    A `ModelResponse` with a single `CompactionPart` containing the encrypted compaction data.































### `OpenAIStreamedResponse`

```python
class OpenAIStreamedResponse
```


Implementation of `StreamedResponse` for OpenAI models.

```python
_model_name: OpenAIModelName
```

```python
_model_profile: OpenAIModelProfile
```

```python
_response: _utils.PeekableAsyncStream[ChatCompletionChunk, AsyncStream[ChatCompletionChunk]]
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
_provider_timestamp: datetime | None = None
```

```python
_timestamp: datetime = field(default_factory=_now_utc)
```

```python
_model_settings: OpenAIChatModelSettings | None = None
```

```python
_content_generation: int = field(default=0, init=False)
```

```python
_reasoning_generation: int = field(default=0, init=False)
```

```python
_held_text_whitespace: str = field(default='', init=False)
```

```python
_awaiting_text_after_reasoning: bool = field(default=False, init=False)
```

```python
_has_refusal: bool = field(default=False, init=False)
```

```python
_refusal_text: str = field(default='', init=False)
```

```python
_has_finish_reason: bool = field(default=False, init=False)
```

```python
_logprobs: list[dict[str, Any]] = field(default_factory=list[dict[str, Any]], init=False)
```



















#### `model_name`

```python
def model_name(self) -> OpenAIModelName
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



### `OpenAIResponsesStreamedResponse`

```python
class OpenAIResponsesStreamedResponse
```


Implementation of `StreamedResponse` for OpenAI Responses API.

```python
_model_name: OpenAIModelName
```

```python
_model_settings: OpenAIResponsesModelSettings
```

```python
_response: _utils.PeekableAsyncStream[responses.ResponseStreamEvent, AsyncStream[responses.ResponseStreamEvent]]
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
_tool_call_ids_are_response_scoped: bool
```

```python
_provider_timestamp: datetime | None = None
```

```python
_timestamp: datetime = field(default_factory=_now_utc)
```

```python
_has_refusal: bool = field(default=False, init=False)
```

```python
_refusal_text: str = field(default='', init=False)
```

```python
_last_sequence_number: int | None = field(default=None, init=False)
```





#### `model_name`

```python
def model_name(self) -> OpenAIModelName
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

### `OpenAICompaction`

```python
class OpenAICompaction
```


Compaction capability for OpenAI Responses API.

Automatically compacts conversation history to keep long-running agent
runs within manageable context limits. Two modes are supported, selected
by the `stateless` flag:

- **Stateful mode** (default, `stateless=False`): configures
  [OpenAI's server-side auto-compaction](https://developers.openai.com/api/docs/guides/compaction)
  via the `context_management` field on the regular `/responses` request.
  The server triggers compaction when input tokens cross a threshold,
  and the compacted item is returned alongside the normal response. On
  subsequent requests, only that item and the content after it are sent.
  Compatible with [`openai_previous_response_id='auto'`][pydantic_ai.models.openai.OpenAIResponsesModelSettings.openai_previous_response_id]
  and server-side conversation state.

  Configurable with `token_threshold` (`compact_threshold` on the API).
  If omitted, OpenAI picks a server-side default.

- **Stateless mode** (`stateless=True`): calls the stateless
  `/responses/compact` endpoint from a `before_model_request` hook when
  your trigger condition is met. Use this in
  [ZDR](https://openai.com/enterprise-privacy/) environments where
  OpenAI must not retain conversation data, when you set
  [`openai_store=False`][pydantic_ai.models.openai.OpenAIResponsesModelSettings.openai_store],
  or when you need explicit out-of-band control over when compaction runs.

  Requires either `message_count_threshold` or a custom `trigger` callable.

If `stateless` is not set, it is inferred from which parameters you
provide: passing any stateless-only parameter (`message_count_threshold`
or `trigger`) implies `stateless=True`; otherwise stateful mode is used.

Example usage:

```python {test="skip"}
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAICompaction

# Stateful mode with OpenAI's server-side default threshold:
agent = Agent(
    'openai-responses:gpt-5.2',
    capabilities=[OpenAICompaction()],
)

# Stateful mode with a custom token threshold:
agent = Agent(
    'openai-responses:gpt-5.2',
    capabilities=[OpenAICompaction(token_threshold=100_000)],
)

# Stateless mode for ZDR environments or explicit control:
agent = Agent(
    'openai-responses:gpt-5.2',
    capabilities=[OpenAICompaction(message_count_threshold=20)],
)
```













































