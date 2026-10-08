# `pydantic_ai.realtime.google`

The Gemini Live API provider. Requires the `google` optional group
(`pip install "pydantic-ai-slim[google]"`).

[`GoogleRealtimeModel`][pydantic_ai.realtime.google.GoogleRealtimeModel] runs over the `google-genai`
SDK (which manages the WebSocket transport). Gemini expects **16 kHz** PCM input (output is 24 kHz),
produces one response modality per session, and natively accepts live video frames sent as
[`BinaryImage`][pydantic_ai.messages.BinaryImage]. It exposes Gemini Live's session and generation
configuration through [`GoogleRealtimeModelSettings`][pydantic_ai.realtime.google.GoogleRealtimeModelSettings] —
shared turn-taking via [`TurnDetection`][pydantic_ai.realtime.TurnDetection], with finer Gemini-specific
control via [`AutomaticVAD`][pydantic_ai.realtime.google.AutomaticVAD] in `google_vad` plus
`google_activity_handling`/`google_turn_coverage`, voice via `google_voice` or a
[`MultiSpeaker`][pydantic_ai.realtime.google.MultiSpeaker] in `google_multi_speaker`,
and long-session [`ContextCompression`][pydantic_ai.realtime.google.ContextCompression] — with
resilience via session resumption + a [`ReconnectPolicy`][pydantic_ai.realtime.ReconnectPolicy] in the
`reconnect` setting.

Gemini Live API provider for realtime speech-to-speech (and live video) sessions.

Built on the `google-genai` SDK, which manages the WebSocket transport for you. Available via the
`google` optional group:

    pip install "pydantic-ai-slim[google-realtime]"

Unlike the OpenAI provider, Gemini wants **16 kHz** PCM input audio (output is 24 kHz), produces a
single response modality per session (audio *or* text), and natively accepts a stream of video
frames sent as [`BinaryImage`][pydantic_ai.messages.BinaryImage].

Use `provider='google'` for the Gemini Developer API, or `provider='google-cloud'` /
[`GoogleCloudProvider`][pydantic_ai.providers.google_cloud.GoogleCloudProvider] for Google Cloud with
Application Default Credentials.

### `AutomaticVAD`

```python
class AutomaticVAD
```


Server-side voice activity detection — the default turn-taking mode for Gemini Live.

```python
disabled: bool
```

```python
start_sensitivity: Literal['high', 'low']
```

```python
end_sensitivity: Literal['high', 'low']
```

```python
prefix_padding_ms: int
```

```python
silence_duration_ms: int
```

### `MultiSpeaker`

```python
class MultiSpeaker
```


Assign prebuilt voices to named speakers for multi-speaker audio output.

```python
voices: dict[str, str]
```

### `ContextCompression`

```python
class ContextCompression
```


Sliding-window context compression so long sessions don't exceed the context window.

```python
trigger_tokens: int
```

```python
target_tokens: int
```

### `GoogleRealtimeModelSettings`

```python
class GoogleRealtimeModelSettings
```


Settings used for a Gemini Live session.

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
seed: int
```

```python
google_thinking_config: genai_types.ThinkingConfigDict
```

```python
google_video_resolution: genai_types.MediaResolution
```

```python
google_language_code: str
```

```python
google_voice: str
```

```python
google_multi_speaker: MultiSpeaker
```

```python
google_affective_dialog: bool
```

```python
google_proactive_audio: bool
```

```python
google_input_transcription: bool
```

```python
google_output_transcription: bool
```

```python
google_transcription_language_codes: list[str]
```

```python
google_vad: AutomaticVAD
```

```python
google_activity_handling: Literal['interrupts', 'no_interruption']
```

```python
google_turn_coverage: Literal['activity_only', 'all_input', 'all_video']
```

```python
google_context_compression: ContextCompression
```

```python
google_config_overrides: dict[str, Any]
```

```python
google_enable_session_resumption: bool
```

```python
google_async_tool_calls: bool
```

### `GoogleRealtimeModelProfile`

```python
class GoogleRealtimeModelProfile
```


Profile for Gemini Live models, adding the Gemini-specific fields to the shared realtime profile.

Mirrors the [`GoogleModelProfile`][pydantic_ai.profiles.google.GoogleModelProfile] /
[`ModelProfile`][pydantic_ai.profiles.ModelProfile] split on the request-response side.

```python
google_thinking_levels: frozenset[GoogleThinkingLevel]
```

```python
google_thinking_always_enabled: bool
```

```python
google_async_tool_calls_by_default: bool
```

```python
google_requires_async_tool_calls: bool
```

```python
google_closes_tool_call_turn_separately: bool
```

```python
google_supports_async_tool_call_scheduling: bool
```

```python
google_supports_affective_dialog: bool
```

```python
google_supported_mime_types_in_tool_returns: tuple[str, ...]
```

```python
google_supports_seeding_function_parts: bool
```

```python
google_text_turns_see_video_frames: bool
```



























### `GoogleRealtimeModel`

```python
class GoogleRealtimeModel
```


Gemini Live API model.

Session and generation configuration is read from
[`GoogleRealtimeModelSettings`][pydantic_ai.realtime.google.GoogleRealtimeModelSettings], passed
through `settings` as model-level defaults or as `model_settings` when opening a session.

Authentication and the underlying `google-genai` client come from a
[`Provider`][pydantic_ai.providers.Provider], mirroring [`GoogleModel`][pydantic_ai.models.google.GoogleModel].
Pass `provider='google'` (the default) for the Gemini Developer API (reads `GOOGLE_API_KEY` /
`GEMINI_API_KEY`), `provider='google-cloud'` for Vertex AI (Application Default Credentials, useful
where org policy disallows API keys), or a [`GoogleProvider`][pydantic_ai.providers.google.GoogleProvider] /
[`GoogleCloudProvider`][pydantic_ai.providers.google_cloud.GoogleCloudProvider] instance for a custom
key, client, or region. Gemini Live is available on both surfaces.

Args:
    model: The model name, e.g. `gemini-3.8-live` (low-latency voice), `gemini-3.8-live-extended-thinking`
        (reasons in the background while it speaks, and always runs tools asynchronously), or
        `gemini-2.5-flash-native-audio-latest` (an alias that tracks the newest native-audio Live model).
    provider: The provider to use for authentication and API access — `'google'` (Gemini Developer
        API, the default) or `'google-cloud'` (Vertex AI), or a `Provider` instance.
    settings: Model-level defaults for session and generation configuration.
    profile: Optional override for the [realtime model profile][pydantic_ai.realtime.RealtimeModelProfile],
        merged over the provider's — a partial dict, or a callable taking the resolved profile and
        returning the one to use. Mirrors `profile=` on a standard
        [`Model`][pydantic_ai.models.Model], and is the escape hatch when a model name doesn't
        identify the model (e.g. an Azure deployment named something other than its model).

```python
model: GoogleRealtimeModelName
```

```python
_: KW_ONLY
```

```python
settings: RealtimeModelSettings | None = None
```

```python
_provider: Provider[Client] = field(init=False, repr=False)
```

#### `client`

```python
def client(self) -> Client
```


The underlying `google.genai.Client` from the provider.

















### `GoogleRealtimeConnection`

```python
class GoogleRealtimeConnection
```


A live connection to the Gemini Live API, backed by a `google-genai` session.

#### `send`

```python
async def send(self, content: RealtimeInput) -> None
```


Send content to the Gemini Live API.

Accepts `BinaryAudio` (raw PCM16, 16kHz, mono), a `str` text turn, `TextContext` (text sent
with `turn_complete=False`, so it waits for the next turn), `BinaryImage` (a live video
frame), and `ToolResult`. The manual turn-taking verbs are not supported (Gemini uses
automatic VAD).









