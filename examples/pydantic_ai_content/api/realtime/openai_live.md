# `pydantic_ai.realtime.openai_live`

The OpenAI GPT-Live API provider. Requires the `openai-realtime` optional group
(`pip install "pydantic-ai-slim[openai-realtime]"`), which floors `openai` at 3.12, the release that
added Live's event types.

GPT-Live is a different protocol from the [OpenAI Realtime API](openai.md), not a model served by it,
so [`OpenAILiveModel`][pydantic_ai.realtime.openai_live.OpenAILiveModel] shares no event mapping with
[`OpenAIRealtimeModel`][pydantic_ai.realtime.openai.OpenAIRealtimeModel]; the model name is what picks
between them. The Live model runs the spoken conversation and delegates the work to a backend model
configured through
[`OpenAILiveResponsesDelegation`][pydantic_ai.realtime.openai_live.OpenAILiveResponsesDelegation] in
[`OpenAILiveModelSettings`][pydantic_ai.realtime.openai_live.OpenAILiveModelSettings], which receives the
agent's instructions and tools and calls them as ordinary
[`ToolCall`][pydantic_ai.realtime.codec.ToolCall]s.

Live owns turn-taking entirely, so there is no manual turn control, interruption, or truncation, and
no turn-detection setting. It sends no end-of-response frame either: the connection synthesizes
[`ResponseDone`][pydantic_ai.realtime.codec.ResponseDone] after `openai_live_turn_silence_ms` of
silence, and the profile reports `synthesizes_turn_boundary=True`. Text is delivered as context
rather than as a user turn, seeding is text-only, and usage is reported as billable audio seconds
instead of tokens. Authentication comes from an
[`OpenAIProvider`][pydantic_ai.providers.openai.OpenAIProvider]; Azure OpenAI does not serve Live. See
the [GPT-Live documentation](../../realtime/openai.md#gpt-live-models) for the full story.

OpenAI GPT-Live realtime support.

GPT-Live is a separate protocol from the [OpenAI Realtime API][pydantic_ai.realtime.openai], not a
model served by it, so none of its event mapping is shared: what it borrows from
`_openai_protocol.py` is the parts that are about the *provider* rather than the protocol (deriving
the WebSocket URL, resolving authentication, and mapping handshake failures). The differences that
shape the adapter:

- **Audio drives the session.** Live has no user-turn event for text: text arrives as *context*
  through `session.commentary.append` (speakable) and `session.thinking.append` (silent), each
  capped at 500 tokens. Both are placed on the session's audio timeline, which only advances while
  audio flows — so a session whose microphone isn't streaming silently defers everything sent to it.
- **There is no turn terminal.** Live has no `response.done` equivalent and no transcript-done
  event; transcripts arrive as timeline fragments. The connection synthesizes
  [`ResponseDone`][pydantic_ai.realtime.codec.ResponseDone] once the model has been quiet for
  `openai_live_turn_silence_ms` and no delegated work is outstanding, and the profile reports
  `synthesizes_turn_boundary=True` so consumers know the boundary is inferred.
- **Work is delegated, not tool-called.** The Live model hands a task either to your application
  (`client` delegation) or to a Responses backend it drives itself (`responses` delegation). Only
  the latter produces typed function calls, so it is what this adapter configures: the agent's tools
  are advertised to the backend, its calls arrive nested inside `response.event`, and their results
  go back as Responses input items. See
  [the Live docs](https://pydantic.dev/docs/ai/realtime/openai#gpt-live-models) for the split.
- **Usage has two meters.** Live reports its own audio as a cumulative duration in seconds and no
  tokens at all; the backend it delegates to reports ordinary Responses token usage, which is where
  most of a call's token cost is.

### `OpenAILiveResponsesDelegation`

```python
class OpenAILiveResponsesDelegation
```


Settings for the Responses backend a Live session delegates work to.

The Live model runs the conversation; the backend model does the reasoning and calls the agent's
tools. OpenAI's prompting guide asks for the two prompts to stay separate, and Pydantic AI keeps
them separate by construction: the agent's instructions become the *backend* prompt, because they
describe the work, while `live_instructions` describes how to speak.

```python
model: str
```

```python
instructions: str
```

```python
max_output_tokens: int
```

```python
parallel_tool_calls: bool
```

```python
reasoning_effort: Literal['none', 'minimal', 'low', 'medium', 'high', 'xhigh']
```

```python
verbosity: Literal['low', 'medium', 'high']
```

```python
service_tier: Literal['auto', 'default', 'flex', 'priority']
```

### `OpenAILiveModelSettings`

```python
class OpenAILiveModelSettings
```


Settings for OpenAI GPT-Live sessions.

See [`RealtimeModelSettings`][pydantic_ai.realtime.RealtimeModelSettings] for the shared settings.
Live has no turn-detection, truncation, token-limit, or temperature controls: it owns turn-taking
entirely, and voice, audio format and instructions are immutable once the session has started.

```python
openai_voice: str
```

```python
openai_live_instructions: str
```

```python
openai_live_delegation: OpenAILiveResponsesDelegation
```

```python
openai_live_turn_silence_ms: int
```

```python
openai_live_store: bool
```

```python
openai_live_data_channel: DataChannelConfigParam
```

### `tool_def_to_live`

```python
def tool_def_to_live(tool: ToolDefinition) -> dict[str, Any]
```


Convert a [`ToolDefinition`][pydantic_ai.tools.ToolDefinition] to a Live backend function tool.







### `seed_input_items`

```python
def seed_input_items(messages: Sequence[ModelMessage], *, provider_name: str) -> list[dict[str, Any]]
```


Map prior history to Live's startup `input` list.

Live seeds from text only: user and assistant messages with one text part each. Tool
rounds are rendered as readable text because the protocol has no place to put function parts in
seeded history. Audio, images, and other media
cannot be seeded at all, and the profile says so, which is what makes the session reject them
before we get here.



### `replay_input_items`

```python
async def replay_input_items(messages: Sequence[ModelMessage], *, provider_name: str) -> list[dict[str, Any]]
```


Map a session's own history to the `input` of the Live session that replaces it after a drop.

Unlike seeding a new session, nothing here is the caller's to fix, so nothing raises: media is left
out, and a long call is cut to its most recent end within Live's seeding caps rather than refused.



### `OpenAILiveConnection`

```python
class OpenAILiveConnection
```


A live WebSocket connection to the OpenAI GPT-Live API.

Translates Live's session-timeline events into the shared codec vocabulary, including the two
boundaries Live itself never sends: the end of the user's turn and the end of the model's reply.

Live streams output audio as a continuous telephony-style track — ten 100 ms frames a second for
as long as the session is open, digitally silent when the model isn't speaking. So a frame
arriving means nothing about whether anyone is talking, and *voice* (a transcript fragment or a
non-silent audio frame) is what drives the turn clock.

```python
transport_errors: ClassVar[tuple[type[Exception], ...]] = (websockets.WebSocketException, OSError)
```

#### `input_transcription_enabled`

```python
def input_transcription_enabled(self) -> bool
```


Live always transcribes both directions; there is no way to turn it off.

#### `reconnect_restores_in_flight_state`

```python
def reconnect_restores_in_flight_state(self) -> bool
```


Neither way of re-opening a Live session carries on what was in flight.

A fork has the conversation, but not the reply or the delegated work the drop cut off: it has no
record of the tool calls that work asked for (checked live). A replacement session has only the
history it was seeded with.







#### `aclose`

```python
async def aclose(self) -> None
```


Cancel the read in flight so closing the socket doesn't strand its exception.



























































### `OpenAILiveModel`

```python
class OpenAILiveModel
```


OpenAI GPT-Live model.

GPT-Live runs the spoken conversation and delegates the thinking to a Responses backend that
Pydantic AI configures with the agent's instructions and tools, so tools, dependencies,
validation, and message history stay on the Pydantic AI side. Reach it through
[`Agent.realtime`][pydantic_ai.agent.Agent.realtime] as `'openai:gpt-live-1'`, or construct it
directly for model-level configuration.

Live differs from the [Realtime API][pydantic_ai.realtime.openai.OpenAIRealtimeModel] in ways that
change what a session can do — no text input, an inferred turn boundary, no manual turn control or
interruption, and duration-based usage. See
[the Live docs](https://pydantic.dev/docs/ai/realtime/openai#gpt-live-models).

Args:
    model: The model name, e.g. `gpt-live-1`.
    provider: The provider to use for authentication and the base URL. Defaults to `'openai'`.
    settings: [Model settings][pydantic_ai.realtime.RealtimeModelSettings] used as defaults for
        realtime sessions.
    profile: Optional override for the [realtime model profile][pydantic_ai.realtime.RealtimeModelProfile].

```python
model: OpenAILiveModelName
```

```python
_: KW_ONLY
```

```python
settings: RealtimeModelSettings | None = None
```

```python
_provider: Provider[AsyncOpenAI] = field(init=False, repr=False)
```

#### `supported_native_tools`

```python
def supported_native_tools(cls) -> frozenset[type[AbstractNativeTool]]
```


Web search, which the delegated backend runs: the only native tool Live lets it have.

#### `client`

```python
def client(self) -> AsyncOpenAI
```


The underlying [`AsyncOpenAI`](https://github.com/openai/openai-python) client from the provider.













#### `create_client_secret`

```python
async def create_client_secret(self, *, instructions: str | None=None, tools: Sequence[ToolDefinition] | None=None, model_settings: RealtimeModelSettings | None=None, expires_after_seconds: int | None=None) -> RealtimeClientSecret
```


GPT-Live has no ephemeral client secrets, so this always raises.

Negotiate the call from your server with
[`answer_webrtc_offer`][pydantic_ai.realtime.openai_live.OpenAILiveModel.answer_webrtc_offer] instead,
so the browser never needs a token.

#### `answer_webrtc_offer`

```python
async def answer_webrtc_offer(self, sdp_offer: str, *, instructions: str | None=None, tools: Sequence[ToolDefinition] | None=None, model_settings: RealtimeModelSettings | None=None) -> WebRTCAnswer
```


Start a Live session for a browser's WebRTC offer, and return the SDP answer and the session to attach to.

Live's configuration is fixed when the session starts, so everything is set here: the voice and
instructions, and the delegated backend with the agent's instructions and tools. The browser's
data channel is closed unless `openai_live_data_channel` opens it. The audio format is negotiated
by WebRTC, so the profile's sample rates don't apply.

#### `connect_webrtc`

```python
async def connect_webrtc(self, session: RealtimeProviderSession, *, messages: Sequence[ModelMessage], model_settings: RealtimeModelSettings | None, model_request_parameters: ModelRequestParameters) -> AsyncGenerator[OpenAILiveConnection]
```


Attach a sideband to a Live session started by [`answer_webrtc_offer`][pydantic_ai.realtime.openai_live.OpenAILiveModel.answer_webrtc_offer].

The session was fully configured when it started, and Live can't reconfigure it, so the sideband
only runs it: it executes the backend's tool calls and records the conversation, while the browser
holds the audio. For the same reason it can't be seeded with `message_history`.