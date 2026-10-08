# `pydantic_ai.models`

Logic related to making requests to an LLM.

The aim here is to make a common interface for different LLMs, so that the rest of the code can be agnostic to the
specific LLM being used.

### `known_model_names`

```python
def known_model_names() -> tuple[str, ...]
```


Return every model name known to [`KnownModelName`][pydantic_ai.models.KnownModelName].

This is the public, stable way to enumerate the known model ids. Prefer it over introspecting
the `KnownModelName` type alias directly (e.g. `get_args(KnownModelName.__value__)`), which is
not part of the public API and would break if the alias were ever recomposed.

### `ModelRequestParameters`

```python
class ModelRequestParameters
```


Configuration for an agent's request to a model, specifically related to tools and output handling.

```python
function_tools: list[ToolDefinition] = field(default_factory=list[ToolDefinition])
```

```python
native_tools: list[AbstractNativeTool] = field(default_factory=list[AbstractNativeTool])
```

```python
tool_visibility: dict[str, ToolVisibility] | None = None
```

```python
revealed_tool_names: set[str] = field(default_factory=set[str], repr=False)
```

```python
deferred_capability_ids: set[str] = field(default_factory=set[str], repr=False)
```

```python
output_mode: OutputMode = 'text'
```

```python
output_object: OutputObjectDefinition | None = None
```

```python
output_tools: list[ToolDefinition] = field(default_factory=list[ToolDefinition])
```

```python
prompted_output_template: str | Literal[False] | None = None
```

```python
allow_text_output: bool = True
```

```python
allow_image_output: bool = False
```

```python
instruction_parts: list[InstructionPart] | None = None
```

```python
thinking: ThinkingLevel | None = None
```

#### `visibility_of`

```python
def visibility_of(self, tool_name: str) -> ToolVisibility
```


The resolved [`ToolVisibility`][pydantic_ai.models.ToolVisibility] for `tool_name`.

For parameters constructed directly rather than resolved by [`Model.prepare_request`][pydantic_ai.models.Model.prepare_request],
deferred function tools default to `'withheld'` and every other name defaults to `'visible'`.

#### `declared_tool_defs`

```python
def declared_tool_defs(self) -> dict[str, ToolDefinition]
```


Definitions represented in the provider's ordinary `tools` collection.

The visibility filter applies to function tools only: output tools are always plain
`tools` entries, so they are included unconditionally rather than keyed through a
name-indexed filter a hidden function tool could shadow.

#### `declared_function_tools`

```python
def declared_function_tools(self) -> list[ToolDefinition]
```


Function tools represented in the provider's ordinary `tools` collection.

#### `with_default_output_mode`

```python
def with_default_output_mode(self, output_mode: StructuredOutputMode) -> ModelRequestParameters
```


Set the default output mode if the current mode is 'auto', atomically updating allow_text_output.

No-op if the current output_mode is not 'auto'. This ensures the two fields stay in sync —
output_mode='tool' implies allow_text_output=False, while 'native' and 'prompted' imply
allow_text_output=True.

### `ModelRequestContext`

```python
class ModelRequestContext
```


Context for model request hooks.

Wrapping these parameters in a dataclass instead of a tuple makes the signature
future-proof: new fields can be added without breaking existing implementations.

A [`before_model_request`][pydantic_ai.capabilities.AbstractCapability.before_model_request] hook
returns a context, so modifying one is normally `dataclasses.replace(request_context, ...)`. Every
field is therefore settable through `replace()`, including `model_id` and `streaming`: the agent
graph sets those two immediately before calling the hook, and `replace()` re-initializes any
`init=False` field to its default, so declaring them that way silently zeroed both for any hook
that copied its context — costing a streamed run its `streaming` flag and a durable-execution
worker the selection token it re-resolves an aliased model from. They are still set by the graph
rather than by a caller; passing either to a fresh `ModelRequestContext` is not meaningful.

```python
model: Model
```

```python
messages: list[ModelMessage]
```

```python
model_settings: ModelSettings | None
```

```python
model_request_parameters: ModelRequestParameters
```

```python
model_id: str | None = None
```

```python
streaming: bool = False
```

```python
_usage_response_ledger: _ModelRequestUsageLedger = field(default_factory=_ModelRequestUsageLedger, repr=False, compare=False)
```



### `ModelResolutionContext`

```python
class ModelResolutionContext
```


Context used to resolve a model ID before a model is available.

This is narrower than [`RunContext`][pydantic_ai.tools.RunContext] because model
resolution happens before a run context can contain its resolved model.

```python
agent: AbstractAgent[ModelContextDepsT, Any]
```

```python
deps: ModelContextDepsT
```

### `ModelSelectionContext`

```python
class ModelSelectionContext
```


Context used by a capability to select the model for a request step.

```python
model: Model | None
```

```python
run_step: int
```

```python
prompt: str | Sequence[UserContent] | None = None
```

```python
messages: list[ModelMessage]
```

```python
usage: RunUsage
```

### `Model`

```python
class Model
```


Abstract class for a model.

```python
supported_tool_deferral_modes: ClassVar[frozenset[ToolDeferralMode]] = frozenset()
```

```python
supported_tool_addition_modes: ClassVar[frozenset[ToolAdditionMode]] = frozenset()
```

```python
compaction_requires_encrypted_content: ClassVar[bool] = False
```

```python
compaction_retains_standing_prompt: ClassVar[bool] = False
```

```python
_provider: Provider[InterfaceClient]
```

```python
_profile: ModelProfileSpec | None = None
```

```python
_settings: ModelSettings | None = None
```



#### `provider`

```python
def provider(self) -> Provider[InterfaceClient] | None
```


The provider for this model, if any.





#### `settings`

```python
def settings(self) -> ModelSettings | None
```


Get the model settings.

#### `resolve_cache_retention`

```python
def resolve_cache_retention(self, model_settings: ModelSettings | None) -> timedelta | None
```


Resolve prompt cache retention requested by provider-specific model settings.

The model's default settings are merged with the per-request `model_settings`. Only provider-specific settings
are currently considered; a future unified cache setting is not yet an input. If multiple active settings
request different retention periods, the longest period wins because any longer-lived cache breakpoint can
keep the corresponding prompt prefix available. Models without a provider-specific retention setting return
`None`, in which case the provider's
[`default_cache_retention`][pydantic_ai.profiles.ModelProfile.default_cache_retention] applies.

#### `resolve_prompt_cache_retention`

```python
def resolve_prompt_cache_retention(self, model_settings: ModelSettings | None) -> timedelta | None
```


Deprecated alias of [`resolve_cache_retention`][pydantic_ai.models.Model.resolve_cache_retention].

#### `tool_deferral_mode`

```python
def tool_deferral_mode(self) -> ToolDeferralMode | None
```


The effective schema-deferral mode: the profile's claim, if this adapter renders it.

#### `tool_addition_mode`

```python
def tool_addition_mode(self) -> ToolAdditionMode | None
```


The effective tool-addition mode: the profile's claim, if this adapter renders it.



#### `request`

```python
async def request(self, messages: list[ModelMessage], model_settings: ModelSettings | None, model_request_parameters: ModelRequestParameters) -> ModelResponse
```


Make a request to the model.

This is ultimately called by `pydantic_ai._agent_graph.ModelRequestNode._make_request(...)`.

#### `count_tokens`

```python
async def count_tokens(self, messages: list[ModelMessage], model_settings: ModelSettings | None, model_request_parameters: ModelRequestParameters) -> RequestUsage
```


Make a request to the model for counting tokens.

#### `compact_messages`

```python
async def compact_messages(self, request_context: ModelRequestContext, *, instructions: str | None=None) -> ModelResponse
```


Compact messages to reduce conversation context size.

This method is optional and only supported by specific providers
(e.g. OpenAI Responses API). Providers that support compaction
override this method with their implementation.

#### `request_stream`

```python
async def request_stream(self, messages: list[ModelMessage], model_settings: ModelSettings | None, model_request_parameters: ModelRequestParameters, run_context: RunContext[Any] | None=None) -> AsyncGenerator[StreamedResponse]
```


Make a request to the model and return a streaming response.

#### `cancel_suspended_response`

```python
async def cancel_suspended_response(self, response: ModelResponse) -> None
```


Cancel a server-side suspended/background response (e.g. an OpenAI background job).

Called when a continuation is abandoned via cancellation or error. No-op by default;
model classes with cancellable server-side jobs override this.

#### `continuation_delay`

```python
def continuation_delay(self, response: ModelResponse) -> float | None
```


Seconds to wait before continuing a suspended response, or `None` to continue immediately.

Called between the segments of a suspended turn. `None` by default (e.g. Anthropic `pause_turn`
continues immediately); a model that polls a server-side job (e.g. OpenAI background mode)
overrides this to return a poll interval so the graph doesn't busy-poll.

#### `customize_request_parameters`

```python
def customize_request_parameters(self, model_request_parameters: ModelRequestParameters) -> ModelRequestParameters
```


Customize the request parameters for the model.

This method can be overridden by subclasses to modify the request parameters before sending them to the model.
In particular, this method can be used to make modifications to the generated tool JSON schemas if necessary
for vendor/model-specific reasons.







#### `prepare_request`

```python
def prepare_request(self, model_settings: ModelSettings | None, model_request_parameters: ModelRequestParameters) -> tuple[ModelSettings | None, ModelRequestParameters]
```


Prepare request inputs before they are passed to the provider.

This merges the given `model_settings` with the model's own `settings` attribute and ensures
`customize_request_parameters` is applied to the resolved
[`ModelRequestParameters`][pydantic_ai.models.ModelRequestParameters]. Subclasses can override this method if
they need to customize the preparation flow further, but most implementations should simply call
`self.prepare_request(...)` at the start of their `request` (and related) methods.

#### `prepare_messages`

```python
def prepare_messages(self, messages: list[ModelMessage], model_request_parameters: ModelRequestParameters | None=None) -> list[ModelMessage]
```


Pre-process the message history before it's handed to the adapter's message-prep step.

Translates typed `NativeToolSearch*Part` instances carried over from a
different provider (e.g. Anthropic to OpenAI Responses), or any native
provider when the active model doesn't support `ToolSearchTool`, into the
local-shape `ToolSearch*Part` instances. This splits the single
`ModelResponse(call+return)` carrying the inline server-side result into
`ModelResponse(call) + ModelRequest(return)` so the adapter can render the
provider-agnostic exchange.

Also wraps non-leading `SystemPromptPart`s as `<system>`-tagged `UserPromptPart`s when
the profile's `supports_inline_system_prompts` is `False`, and converts
`SpeechPart`s from realtime session history into `UserPromptPart`s /
`TextPart`s that any model can consume.

Subclasses normally don't need to override this; the framework calls it on the
agent's behalf in `_agent_graph._make_request` so per-adapter message-prep code
sees a homogeneous shape regardless of which provider produced the prior turn.

Args:
    messages: The history to pre-process.
    model_request_parameters: The parameters this history will be sent with. Optional, and
        only needed to render a `ToolAvailabilityDeltaPart` on a model with no native way to
        express one: whether that reveal has to be a mechanism or can just be a statement
        depends on whether any tool actually goes on the wire with its schema withheld, which
        the profile alone can't answer. Omitting it falls back to the adapter's effective mode,
        which differs only for a corpus mixing capability-gated and standalone deferred tools.
        Framework callers pass it.









#### `supported_native_tools`

```python
def supported_native_tools(cls) -> frozenset[type[AbstractNativeTool]]
```


Return the set of native tool types this model class can handle.

Subclasses should override this to reflect their actual capabilities.
Default is empty set - subclasses must explicitly declare support.

#### `context_window`

```python
def context_window(self) -> int | None
```


The resolved profile's [`context_window`][pydantic_ai.profiles.ModelProfile.context_window].

#### `profile`

```python
def profile(self) -> ModelProfile
```


The model profile.

Resolution order (later layers override earlier ones):
  1. `DEFAULT_PROFILE` — base values for every key in `ModelProfile`.
  2. The provider's `model_profile(model_name)` result — provider-specific defaults
     for this model.
  3. A best-effort `context_window` value from
     [genai-prices](https://github.com/pydantic/genai-prices), unless the provider or a
     partial user profile explicitly set the field (including to `None`).
  4. The user's `profile=` argument — partial dict merged on top, OR a callable
     `(default) -> profile` for full control.

After resolution we compute the intersection of the profile's `supported_native_tools`
and the model class's implemented tools, ensuring `model.profile['supported_native_tools']`
is the single source of truth for what's actually usable.





### `StreamedResponse`

```python
class StreamedResponse
```


Streamed response from an LLM when calling a tool.

```python
model_request_parameters: ModelRequestParameters
```

```python
final_result_event: FinalResultEvent | None = field(default=None, init=False)
```

```python
provider_response_id: str | None = field(default=None, init=False)
```

```python
provider_details: dict[str, Any] | None = field(default=None, init=False)
```

```python
finish_reason: FinishReason | None = field(default=None, init=False)
```

```python
state: ModelResponseState = field(default='complete', init=False)
```

```python
metadata: dict[str, Any] | None = field(default=None, init=False)
```

```python
_event_iterator: AsyncIterator[ModelResponseStreamEvent] | None = field(default=None, init=False)
```

```python
_usage: RequestUsage = field(default_factory=RequestUsage, init=False)
```

```python
_cancelled: bool = field(default=False, init=False)
```

```python
_finished: bool = field(default=False, init=False)
```

```python
_first_chunk_monotonic: float | None = field(default=None, init=False)
```



#### `cancel`

```python
async def cancel(self) -> None
```


Cancel local stream consumption and request provider shutdown.

Sets `self._cancelled = True` before delegating to `close_stream()`
so the flag is visible to any iterator that observes the transport error
raised when the underlying connection is torn down, even if
`close_stream()` itself raises.

#### `get_stream_cancel_errors`

```python
def get_stream_cancel_errors(self) -> tuple[type[BaseException], ...]
```


Return transport errors caused by `cancel()` tearing down the stream.

The default covers model classes whose SDKs iterate HTTP responses
directly (Anthropic, OpenAI, Groq, Mistral, Google GenAI, and HuggingFace),
since they let bare `httpx2` (or legacy `httpx`) errors propagate from
chunk reads. Model classes that use other transports (for example gRPC or
botocore) should override this method.

#### `close_stream`

```python
async def close_stream(self) -> None
```


Close the provider stream and any exposed HTTP or gRPC transport.

Model classes must override this to close the local stream and, where the
provider SDK exposes one, its transport. Integrations that cannot support
local cancellation should leave the default implementation so `cancel()`
fails clearly.



#### `get`

```python
def get(self) -> ModelResponse
```


Build a [`ModelResponse`][pydantic_ai.messages.ModelResponse] from the data received from the stream so far.

#### `usage`

```python
def usage(self) -> RequestUsage
```


Get the usage of the response so far. This will not be the final usage until the stream is exhausted.

#### `model_name`

```python
def model_name(self) -> str
```


Get the model name of the response.

#### `provider_name`

```python
def provider_name(self) -> str | None
```


Get the provider name.

#### `provider_url`

```python
def provider_url(self) -> str | None
```


Get the provider base URL.

#### `timestamp`

```python
def timestamp(self) -> datetime
```


Get the timestamp of the response.

#### `cancelled`

```python
def cancelled(self) -> bool
```


Whether the stream has been cancelled via `cancel()`.

#### `time_to_first_chunk`

```python
def time_to_first_chunk(self, request_start: float) -> float | None
```


Seconds from `request_start` to the first chunk surfaced to the consumer, or `None` if nothing was yielded.

`request_start` must be a `time.perf_counter()` reading taken when the request was issued.
The first-chunk instant is stamped on the first `async for` pull, so the result reflects when
the consumer *received* the first event: it includes any consumer-side iteration delay
(debouncing, batching, or awaiting other work) on top of the chunk's transit time, which for
eager consumers is negligible.

### `CompletedStreamedResponse`

```python
class CompletedStreamedResponse
```


A `StreamedResponse` that wraps an already-completed `ModelResponse`.

Used when a [`StreamedResponse`][pydantic_ai.models.StreamedResponse] is needed but no
live stream is available — for example, when an agent run is short-circuited by
[`SkipModelRequest`][pydantic_ai.exceptions.SkipModelRequest], when a capability's
[`wrap_model_request`][pydantic_ai.capabilities.AbstractCapability.wrap_model_request]
short-circuits without calling the handler, or when a durable-execution capability drains
the real stream inside an activity/step/task and only surfaces the final
[`ModelResponse`][pydantic_ai.messages.ModelResponse] to the workflow.

What the stream yields is controlled by `replay_events`:

- `False` (default): yield no events — the response is complete and no streaming
  consumer needs to observe it.
- `True`: synthesize `PartStartEvent` + `PartDeltaEvent` sequences from the response
  parts, so streaming consumers (`event_stream_handler`, `run_stream_events`, ...)
  keep working when only a complete `ModelResponse` exists.
- a list of events: replay events that were captured off the live stream elsewhere
  (e.g. inside a durable-execution activity/step/task), preserving the real
  event granularity.

### `check_allow_model_requests`

```python
def check_allow_model_requests() -> None
```


Check if model requests are allowed.

If you're defining your own models that have costs or latency associated with their use, you should call this at the
top of each method that sends a request to the provider: [`Model.request`][pydantic_ai.models.Model.request],
[`Model.request_stream`][pydantic_ai.models.Model.request_stream],
[`Model.count_tokens`][pydantic_ai.models.Model.count_tokens],
[`Model.compact_messages`][pydantic_ai.models.Model.compact_messages],
[`EmbeddingModel.embed`][pydantic_ai.embeddings.EmbeddingModel.embed],
[`EmbeddingModel.count_tokens`][pydantic_ai.embeddings.EmbeddingModel.count_tokens] and
[`ImageGenerationModel.generate`][pydantic_ai.images.ImageGenerationModel.generate].

Methods that produce their result locally don't need it — for example
[`OpenAIEmbeddingModel`][pydantic_ai.embeddings.openai.OpenAIEmbeddingModel]'s `count_tokens`, which tokenizes with
`tiktoken` and never calls the provider. Neither does
[`Model.cancel_suspended_response`][pydantic_ai.models.Model.cancel_suspended_response], which deliberately omits it
so an already-started job can still be cancelled after the flag is flipped.

Raises:
    RuntimeError: If model requests are not allowed.

### `override_allow_model_requests`

```python
def override_allow_model_requests(allow_model_requests: bool) -> Generator[None]
```


Context manager to temporarily override [`ALLOW_MODEL_REQUESTS`][pydantic_ai.models.ALLOW_MODEL_REQUESTS].

Args:
    allow_model_requests: Whether to allow model requests within the context.

### `parse_model_id`

```python
def parse_model_id(model: str) -> tuple[str | None, str]
```


Parse a model id string into its provider and model name components.

Args:
    model: A model identifier string in the form `provider:model_name`.

Returns:
    A tuple of `(provider_name, model_name)`. If the model string contains no
    `provider:` prefix, returns `(None, model)` so callers can decide how to
    handle the unknown provider.



### `infer_model_profile`

```python
def infer_model_profile(model: str) -> ModelProfile
```


Infer the model profile from a model id string without constructing a provider.

Uses `Provider.model_profile` to look up the profile for the given model, then fills an unset
`context_window` from genai-prices when available.
Returns `DEFAULT_PROFILE` for unknown or unrecognized providers.

Note: This returns the raw provider profile **without** intersecting with
`Model.supported_native_tools()`, unlike `Model.profile`. This means the returned
profile may claim support for native tools that a specific `Model` subclass doesn't
implement. This is acceptable for best-effort scenarios (e.g. `TemporalModel` with
unregistered model strings) where the actual `Model` class isn't available.

Args:
    model: A model identifier string (e.g. `'openai:gpt-5'`, `'anthropic:claude-sonnet-4-5'`).

Returns:
    The inferred `ModelProfile`, or `DEFAULT_PROFILE` if the provider is unknown.

### `infer_model`

```python
def infer_model(model: Model | KnownModelName | str, provider_factory: Callable[[str], Provider[Any]]=infer_provider) -> Model
```


Infer the model from the name.

Args:
    model:
        Model name to instantiate, in the format of `provider:model`. Use the string "test" to instantiate TestModel.
    provider_factory:
        Function that instantiates a provider object. The provider name is passed into the function parameter. Defaults to `provider.infer_provider`.

### `create_async_http_client`

```python
def create_async_http_client(*, timeout: int=DEFAULT_HTTP_TIMEOUT, connect: int=5) -> AsyncClient
```


Create a legacy HTTPX async client.

This factory serves the providers whose SDKs still require a legacy `httpx.AsyncClient`;
providers migrated to `httpx2` build their own `httpx2.AsyncClient` instead.

Each call creates a new client instance. A provider that calls this itself, because you didn't pass
an `http_client`, closes the client when the provider (or agent) exits. A client you create with it
and pass as `http_client` is yours to close.

The default timeouts and connection pool limits match those of OpenAI,
see <https://github.com/openai/openai-python/blob/v1.54.4/src/openai/_constants.py#L9>.

Raises:
    ImportError: If legacy `httpx` is not installed.

### `DownloadedItem`

```python
class DownloadedItem
```


The downloaded data and its type.

```python
data: DataT
```

```python
data_type: str
```

### `download_item`

```python
async def download_item(item: FileUrl, data_format: Literal['bytes', 'base64', 'base64_uri', 'text']='bytes', type_format: Literal['mime', 'extension']='mime') -> DownloadedItem[str] | DownloadedItem[bytes]
```


Download an item by URL and return the content as a bytes object or a (base64-encoded) string.

This function includes SSRF (Server-Side Request Forgery) protection:
- Only http:// and https:// protocols are allowed
- Private/internal IP addresses are blocked by default
- Cloud metadata endpoints (169.254.169.254) are always blocked
- Hostnames are resolved before requests to prevent DNS rebinding
- Response bodies are limited to 50 MiB

Set `item.force_download='allow-local'` to allow private IP addresses.

Args:
    item: The item to download.
    data_format: The format to return the content in:
        - `bytes`: The raw bytes of the content.
        - `base64`: The base64-encoded content.
        - `base64_uri`: The base64-encoded content as a data URI.
        - `text`: The content as a string.
    type_format: The format to return the media type in:
        - `mime`: The media type as a MIME type.
        - `extension`: The media type as an extension.

Raises:
    UserError: If the URL points to a YouTube video.
    ValueError: If the URL uses an unsupported protocol or targets a private/internal
        IP address (unless allow-local is set), or the body exceeds 50 MiB.

### `get_user_agent`

```python
def get_user_agent() -> str
```


Get the user agent string for the HTTP client.



### `resolve_request_tools`

```python
def resolve_request_tools(params: ModelRequestParameters, supported_types: frozenset[type[AbstractNativeTool]], *, can_withhold_tool_schemas: Callable[[Sequence[AbstractNativeTool]], bool] | None=None, tool_addition_mode: ToolAdditionMode | None=None) -> ModelRequestParameters
```


Resolve native tools, their local fallbacks, and deferred-tool visibility for the given supported-native-tool set.

Three rules drive the per-tool filter:

1. `unless_native` matches a supported native tool → drop from wire.
2. `with_native` matches an *unsupported* native tool → shed `with_native`. The tool is
   a member of a corpus the native tool would have managed; with that native tool absent
   the membership means nothing, and an adapter deriving a wire flag from it would emit
   the flag unpaired and earn a rejection.
3. `defer_loading` remains authored intent; this function resolves its provider representation
   into `tool_visibility` exactly once. A caller without a `can_withhold_tool_schemas` answer
   (the realtime session path) can't withhold schemas at all.

On top of the filter, two narrower drops apply, kept independent:

* `optional=True` only governs the *unsupported-on-this-model* path: an unsupported
  optional native tool is silently dropped (no error raised). It does NOT govern the
  corpus-empty drop.
* The corpus-empty drop is specific to the framework-managed tool-search native tool's
  corpus-management role: an *optional* `ToolSearchTool` is dropped when nothing is
  searchable, since sending it with no corpus to search would waste a tool slot. A
  non-optional `ToolSearchTool` stays — the user asked explicitly. Other native tools
  don't have a corpus and aren't subject to this drop, so making `optional` a base-class
  field doesn't accidentally cause e.g. `WebSearchTool(optional=True)` to be dropped here.

This is a module-level function rather than a `Model` method so both the classic agent-run
path (via `Model._resolve_request_tools`, which passes its profile-derived
`_can_withhold_tool_schemas` and `tool_addition_mode`) and the realtime session path can
share it — `RealtimeModel` is not a `Model` subclass.

### `prepare_return_schemas`

```python
def prepare_return_schemas(params: ModelRequestParameters, *, supports_tool_return_schema: bool) -> ModelRequestParameters
```


Resolve return schemas: clear on tools that haven't opted in, inject into descriptions for non-native models.

For tools with `include_return_schema=True` and a non-empty schema, models that natively support
return schemas keep the schema as-is; other models get it injected into the tool description.
Tools that haven't opted in have their `return_schema` cleared.

A module-level function taking the profile flag rather than a `Model` method so both the classic
path (via `Model.prepare_request`) and the realtime session path can share it — `RealtimeModel` is
not a `Model` subclass and carries its own profile type.























