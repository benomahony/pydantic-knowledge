# `pydantic_ai.realtime.openai`

The OpenAI Realtime API provider. Requires the `realtime` and `openai` optional groups
(`pip install "pydantic-ai-slim[realtime,openai]"`).

[`OpenAIRealtimeModelSettings`][pydantic_ai.realtime.openai.OpenAIRealtimeModelSettings] configures
the session, including shared turn-taking via [`TurnDetection`][pydantic_ai.realtime.TurnDetection]
(or `False` for push-to-talk). For finer control, `openai_turn_detection` accepts
[`ServerVAD`][pydantic_ai.realtime.openai.ServerVAD] or
[`SemanticVAD`][pydantic_ai.realtime.openai.SemanticVAD] and fully overrides the shared setting.
Resilience comes from the `reconnect` setting: a
[`ReconnectPolicy`][pydantic_ai.realtime.ReconnectPolicy] in
[`RealtimeModelSettings`][pydantic_ai.realtime.RealtimeModelSettings].

OpenAI Realtime API provider for speech-to-speech sessions.

Connects to `wss://api.openai.com/v1/realtime` over a WebSocket and maps the OpenAI event
protocol to the shared realtime event types.

Requires the `websockets` and `openai` packages, available via the `realtime` and `openai` optional
groups:

    pip install "pydantic-ai-slim[openai-realtime]"



### `OpenAIRealtimeModelSettings`

```python
class OpenAIRealtimeModelSettings
```


Settings specific to OpenAI realtime models.

```python
openai_voice: KnownOpenAIRealtimeVoiceName | str | VoiceID
```

```python
openai_input_noise_reduction: Literal['near_field', 'far_field']
```

```python
openai_output_speed: float
```

```python
openai_turn_detection: ServerVAD | SemanticVAD
```

```python
openai_truncation: RealtimeTruncationParam
```















### `OpenAIRealtimeConnection`

```python
class OpenAIRealtimeConnection
```


A live WebSocket connection to the OpenAI Realtime API.

```python
_lifecycle_version: ClassVar[int] = 2
```



#### `message_history`

```python
def message_history(self) -> Callable[[], Sequence[ModelMessage]] | None
```


The call so far, when a session has offered it for replay on reconnect.



#### `send`

```python
async def send(self, content: RealtimeInput) -> None
```


Send content to the OpenAI Realtime API.

Accepts `BinaryAudio` (raw PCM16, 24kHz, mono), a `str` text turn, `TextContext` (text added
without soliciting a reply), `BinaryImage`, `ToolResult`, and the control verbs `CommitAudio`, `ClearAudio`, `CreateResponse`,
`CancelResponse`, and `TruncateOutput`.





























### `OpenAIRealtimeModel`

```python
class OpenAIRealtimeModel
```


OpenAI Realtime API model.

Authentication and the base URL come from a
[`Provider`][pydantic_ai.providers.Provider], mirroring [`OpenAIChatModel`][pydantic_ai.models.openai.OpenAIChatModel].
Pass `provider='openai'` (the default) to read `OPENAI_API_KEY` / `OPENAI_BASE_URL` from the
environment, or an [`OpenAIProvider`][pydantic_ai.providers.openai.OpenAIProvider] instance for a
custom key or base URL. The realtime transport is opened separately with `websockets`, so the
provider's `httpx` client is not used for the WebSocket connection. The realtime WebSocket URL is
derived from the provider's base URL (e.g. `https://api.openai.com/v1/` →
`wss://api.openai.com/v1/realtime`), so OpenAI-compatible endpoints that expose a realtime API
work too.

Args:
    model: The model name, e.g. `gpt-realtime` or `gpt-realtime-2.1-mini`.
    provider: The provider to use for authentication and the base URL. Defaults to `'openai'`.
        Azure OpenAI is not supported (its realtime endpoint uses a different URL and auth scheme).
    settings: [Model settings][pydantic_ai.realtime.RealtimeModelSettings] used as defaults for
        realtime sessions.
    profile: Optional override for the [realtime model profile][pydantic_ai.realtime.RealtimeModelProfile],
        merged over the provider's — a partial dict, or a callable taking the resolved profile and
        returning the one to use. Mirrors `profile=` on a standard
        [`Model`][pydantic_ai.models.Model], and is the escape hatch when a model name doesn't
        identify the model (e.g. an Azure deployment named something other than its model).

```python
_connection_type: ClassVar[type[OpenAIRealtimeConnection]] = OpenAIRealtimeConnection
```

```python
_auto_transcription_model: ClassVar[str] = 'gpt-live-transcribe'
```

```python
model: OpenAIRealtimeModelName
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



#### `client`

```python
def client(self) -> AsyncOpenAI
```


The underlying [`AsyncOpenAI`](https://github.com/openai/openai-python) client from the provider.



