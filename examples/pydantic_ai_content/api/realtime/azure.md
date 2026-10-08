# `pydantic_ai.realtime.azure`

The Azure OpenAI realtime model reuses the OpenAI Realtime codec and connection, authenticates with
[`AzureProvider`][pydantic_ai.providers.azure.AzureProvider], and so needs the `realtime` and
`openai` optional groups (`pip install "pydantic-ai-slim[realtime,openai]"`).

Azure realtime support using the OpenAI GA or Azure AI Voice Live protocol.

### `AzureRealtimeModelProfile`

```python
class AzureRealtimeModelProfile
```


A [`RealtimeModelProfile`][pydantic_ai.realtime.RealtimeModelProfile] with the Azure-specific facts.

Read via [`AzureRealtimeModel.profile`][pydantic_ai.realtime.azure.AzureRealtimeModel]. Pass a partial
one as `profile=` to correct what's inferred from a deployment name that doesn't match its model.

```python
azure_realtime_apis: frozenset[AzureRealtimeApi]
```

```python
azure_voice_live_cascade: bool
```







### `AzureRealtimeConnection`

```python
class AzureRealtimeConnection
```


A live WebSocket connection to Azure OpenAI's realtime API.

Reuses [`OpenAIRealtimeConnection`][pydantic_ai.realtime.openai.OpenAIRealtimeConnection] for the
shared GA wire protocol, naming Azure as the vendor so a connection that drops or rejects content
doesn't send someone debugging an Azure session to OpenAI's status page.

### `AzureTokenCredential`

```python
class AzureTokenCredential
```


Structural type for a synchronous Microsoft Entra ID token credential.

### `AzureVoiceLiveVoice`

```python
class AzureVoiceLiveVoice
```


An Azure voice for an [Azure AI Voice Live](https://learn.microsoft.com/azure/ai-services/speech-service/voice-live-how-to#audio-output-through-azure-text-to-speech) session.

Sent as the session's `voice` object as-is, so it takes the fields Voice Live documents for each
voice `type`. Set it with
[`azure_voice_live_voice`][pydantic_ai.realtime.azure.AzureRealtimeModelSettings.azure_voice_live_voice].

```python
type: Required[Literal['azure-standard', 'azure-custom', 'azure-personal', 'azure-realtime-native']]
```

```python
name: Required[str]
```

```python
endpoint_id: str
```

```python
model: str
```

```python
temperature: float
```

```python
rate: str
```

```python
pitch: str
```

```python
volume: str
```

```python
style: str
```

```python
locale: str
```

```python
prefer_locales: list[str]
```

```python
custom_lexicon_url: str
```

### `AzureRealtimeModelSettings`

```python
class AzureRealtimeModelSettings
```


Settings specific to Azure realtime models.

This inherits every [`OpenAIRealtimeModelSettings`][pydantic_ai.realtime.openai.OpenAIRealtimeModelSettings]
field. When [`azure_voice_live`][pydantic_ai.realtime.azure.AzureRealtimeModelSettings.azure_voice_live]
is set, the Voice Live session config is built from the fields Voice Live's beta session object
has a counterpart for: `instructions`, `openai_voice` (by name, unless `azure_voice_live_voice` is
set), `turn_detection` (or `openai_turn_detection`, or `azure_voice_live_turn_detection`),
`openai_input_noise_reduction`, `thinking` (as `reasoning_effort`, on models whose profile reports
[`supports_thinking`][pydantic_ai.realtime.RealtimeModelProfile.supports_thinking]),
`input_transcription_model`, `output_modality`, `max_tokens`, `tool_choice`, and tools, plus the
`azure_voice_live_*` settings.

The remaining inherited fields — `openai_output_speed`, `openai_truncation`, and
`parallel_tool_calls` — are **silently ignored** under Voice Live; they still apply on the GA path.
Voice Live's own `truncation_strategy` takes different values from `openai_truncation` (`'auto'` or
`'last_messages'`, not a retention ratio), so the two don't map onto each other.

```python
azure_voice_live: bool
```

```python
azure_voice_live_turn_detection: ServerVAD | SemanticVAD
```

```python
azure_voice_live_voice: str | AzureVoiceLiveVoice
```

```python
azure_voice_live_temperature: float
```











### `AzureRealtimeModel`

```python
class AzureRealtimeModel
```


Azure realtime model using the OpenAI GA protocol or Azure AI Voice Live.

The existing [`AzureProvider`][pydantic_ai.providers.azure.AzureProvider] supplies the Azure
resource endpoint and API key. The WebSocket transport does not use its OpenAI SDK client or
`api_version`. By default it connects to the GA `/openai/v1/realtime` endpoint; set
[`azure_voice_live`][pydantic_ai.realtime.azure.AzureRealtimeModelSettings.azure_voice_live]
to connect to `/voice-live/realtime` with the Voice Live beta session protocol. Both use an
`api-key` header.

Pass a Microsoft Entra ID `credential` (e.g. `azure.identity.DefaultAzureCredential()`) to
authenticate every request to the resource — the realtime WebSocket session *and* the browser
WebRTC signaling calls — with a bearer token instead of the `api-key` (needed when the resource is
locked to managed identity). For browser WebRTC the browser still only ever receives the short-lived
ephemeral secret, never the Entra token or the API key.

A model served only by Voice Live (e.g. the cascade chat models like `gpt-5`, or `phi4-mm-realtime`)
routes there automatically; a model served by both defaults to GA and needs `azure_voice_live=True`
for Voice Live; a GA-only model rejects the setting. See
[`AzureRealtimeModelProfile.azure_realtime_apis`][pydantic_ai.realtime.azure.AzureRealtimeModelProfile.azure_realtime_apis].

```python
_connection_type: ClassVar[type[OpenAIRealtimeConnection]] = AzureRealtimeConnection
```

```python
_auto_transcription_model: ClassVar[str] = 'gpt-realtime-whisper'
```

```python
credential: AzureTokenCredential | None = None
```



#### `profile`

```python
def profile(self) -> RealtimeModelProfile
```


The Azure realtime profile, with the model's serving APIs and minus what Voice Live can't do.

Stamps [`azure_realtime_apis`][pydantic_ai.realtime.azure.AzureRealtimeModelProfile.azure_realtime_apis]
for a recognized model (a `profile=` override wins), which routes between the GA API and Voice
Live. And because Voice Live negotiates WebRTC over its own WebSocket control channel rather than
the GA signaling endpoints this model inherits, a model configured for Voice Live reports no
WebRTC support and the signaling methods refuse. Voice Live selected per session instead can't be
seen from here, so those calls still refuse at the point of use.





