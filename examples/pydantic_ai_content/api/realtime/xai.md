# `pydantic_ai.realtime.xai`

The xAI Grok Voice realtime API provider. Requires the `realtime`, `xai`, and `openai` optional
groups (`pip install "pydantic-ai-slim[realtime,xai,openai]"`) — `openai` because the model reuses
the OpenAI Realtime codec, whose event types come from the OpenAI SDK.

xAI's realtime API is a clone of the OpenAI Realtime protocol, so
[`XaiRealtimeModel`][pydantic_ai.realtime.xai.XaiRealtimeModel] reuses the OpenAI codec (event
mapping, seeding, the WebSocket connection). Turn-taking uses the shared
[`TurnDetection`][pydantic_ai.realtime.TurnDetection] (or `False` for push-to-talk); for exact
server-VAD control, `xai_turn_detection` accepts
[`ServerVAD`][pydantic_ai.realtime.openai.ServerVAD] and fully overrides the shared setting. It
diverges only where xAI does: it supports
cancellation-based interruption but not output truncation, has no image input, and streams input
transcription as cumulative snapshots that may revise earlier text, rather than as incremental deltas.
Authentication comes from an
[`XaiProvider`][pydantic_ai.providers.xai.XaiProvider], mirroring [`XaiModel`][pydantic_ai.models.xai.XaiModel].

xAI Grok Voice realtime API provider for speech-to-speech sessions.

Connects to `wss://api.x.ai/v1/realtime` over a WebSocket. xAI's realtime API is a deliberate clone of
the OpenAI Realtime protocol, so this provider reuses the OpenAI codec from
[`pydantic_ai.realtime.openai`][pydantic_ai.realtime.openai] — event mapping, session seeding, tool
conversion, server-VAD config, and the WebSocket connection itself — and diverges only where xAI does:

- the `session.update` shape (`voice`/`turn_detection` sit at the session top level, not nested under
  `audio` as on OpenAI's GA surface);
- input audio transcription, delivered as cumulative
  `conversation.item.input_audio_transcription.updated` snapshots plus a final `.completed`, rather
  than OpenAI's incremental `.delta` events (see [`map_event`][pydantic_ai.realtime.xai.map_event]);
- native conversation resumption when a reconnect policy is configured: the provider-assigned
  `conversation.id` is reused and its replay burst is suppressed from local history;
- no output truncation at barge-in: xAI's `conversation.item.truncate` only lands once the response
  has ended, and unreliably even then, so
  [`RealtimeModelProfile.supports_output_truncation`][pydantic_ai.realtime.RealtimeModelProfile.supports_output_truncation]
  is `False` while cancellation-based interruption still works;
- no text output — the API has no response-modality control and always speaks — so
  [`RealtimeModelProfile.supports_text_output`][pydantic_ai.realtime.RealtimeModelProfile.supports_text_output]
  is `False` and `output_modality='text'` raises rather than silently coming back as audio.

Requires the `websockets` package (the `realtime` optional group), `xai-sdk` (the `xai` group, for
[`XaiProvider`][pydantic_ai.providers.xai.XaiProvider]), and `openai` (the `openai` group, whose SDK
supplies the event types the shared OpenAI codec is built on):

    pip install "pydantic-ai-slim[xai-realtime]"



### `map_conversation_event`

```python
def map_conversation_event(data: dict[str, Any], *, replayed: bool | None=None) -> ConversationCreated | ConversationItemCreated | None
```


Map xAI's conversation handshake and item lifecycle events to codec control events.





### `XaiRealtimeModelSettings`

```python
class XaiRealtimeModelSettings
```


Settings specific to xAI realtime models.

Grok Voice always produces audio, so its profile reports
[`supports_text_output=False`][pydantic_ai.realtime.RealtimeModelProfile.supports_text_output] and
the inherited `output_modality='text'` is rejected up front rather than quietly ignored.

```python
xai_voice: str
```

```python
xai_turn_detection: ServerVAD
```

### `map_event`

```python
def map_event(data: dict[str, Any]) -> RealtimeCodecEvent | None
```


Map a raw xAI Grok Voice realtime event to a [`RealtimeCodecEvent`][pydantic_ai.realtime.codec.RealtimeCodecEvent].

xAI clones the OpenAI Realtime protocol, so most events map identically via the OpenAI codec.
The first exception is input audio transcription: xAI emits cumulative
`conversation.item.input_audio_transcription.updated` snapshots (which may retroactively *correct*
earlier text — `'Hello?'` becomes `'Hello, my name is'`) plus cumulative `.completed` snapshots,
rather than OpenAI's incremental `.delta`. The partials are surfaced as cumulative
[`InputTranscript`][pydantic_ai.realtime.codec.InputTranscript]s so a live transcript can render
the user's words as they are spoken; the session adopts each snapshot wholesale, appending when it
merely extends and replacing when xAI revises itself. The shared codec still drops interim
`.completed` snapshots.
The other exception is xAI's conversation lifecycle events, which are surfaced as codec control
events so the connection can capture `conversation.id` and the session can suppress resume replay.

### `XaiRealtimeConnection`

```python
class XaiRealtimeConnection
```


A live WebSocket connection to the xAI Grok Voice realtime API.

Reuses [`OpenAIRealtimeConnection`][pydantic_ai.realtime.openai.OpenAIRealtimeConnection] for the
shared wire protocol, while mapping xAI's cumulative input transcription and conversation lifecycle
events and emitting the resumption replay controls captured during reconnect handshakes.











#### `set_message_history`

```python
def set_message_history(self, message_history: Callable[[], Sequence[ModelMessage]]) -> None
```


Ignored: xAI restores the conversation itself, so replaying it would say everything twice.

#### `conversation_id`

```python
def conversation_id(self) -> str | None
```


The xAI conversation ID used for native session resumption.

### `XaiRealtimeModel`

```python
class XaiRealtimeModel
```


xAI Grok Voice realtime API model.

Pass `provider='xai'` (the default, which reads `XAI_API_KEY`) or an
[`XaiProvider`][pydantic_ai.providers.xai.XaiProvider] constructed with `api_key=`. A custom
`api_host` is not supported, and a provider constructed only with `xai_client=` cannot be used
because the WebSocket connection needs access to the API key. The realtime WebSocket URL is
`wss://api.x.ai/v1/realtime`.

Args:
    model: The model name, e.g. `grok-voice-latest` (which tracks the current model) or a
        pinned version like `grok-voice-think-fast-1.0`. The `model` query parameter is required by
        the server, which otherwise falls back to a default silently.
    provider: The provider to use for authentication and the base URL. Defaults to `'xai'`.
    settings: [Model settings][pydantic_ai.realtime.RealtimeModelSettings] used as defaults for
        realtime sessions. A [`reconnect`][pydantic_ai.realtime.RealtimeModelSettings.reconnect]
        policy enables xAI's native session resumption: prior turns are restored when reconnecting
        within xAI's resumption window (30 minutes of inactivity).
    profile: Optional override for the [realtime model profile][pydantic_ai.realtime.RealtimeModelProfile],
        merged over the provider's — a partial dict, or a callable taking the resolved profile and
        returning the one to use. Mirrors `profile=` on a standard
        [`Model`][pydantic_ai.models.Model], and is the escape hatch when a model name doesn't
        identify the model (e.g. an Azure deployment named something other than its model).

```python
model: XaiRealtimeModelName
```

```python
_: KW_ONLY
```

```python
settings: RealtimeModelSettings | None = None
```

```python
_provider: XaiProvider = field(init=False, repr=False)
```

```python
_api_key: str = field(init=False, repr=False)
```