# `pydantic_ai.realtime.codec`

The lower-level *codec* vocabulary, for implementing a realtime provider or consuming a
[`RealtimeConnection`][pydantic_ai.realtime.codec.RealtimeConnection] directly: the raw events a
connection yields, the turn-control verbs and inputs it accepts, and the model-profile merge helpers.
Most users only need the session-level API in [`pydantic_ai.realtime`](../realtime.md).

Low-level *codec* vocabulary for realtime providers.

Most users only need the session-level API in [`pydantic_ai.realtime`][pydantic_ai.realtime]
([`AgentRealtime.session`][pydantic_ai.agent.AgentRealtime.session], the events a session yields,
and the content passed to [`RealtimeSession.send`][pydantic_ai.realtime.RealtimeSession.send]). This
submodule holds the lower-level vocabulary used when *implementing* a realtime provider or consuming a
[`RealtimeConnection`][pydantic_ai.realtime.codec.RealtimeConnection] directly: the raw codec events a
connection yields to the session, the turn-control verbs and inputs a connection accepts, and the
model-profile merge helpers.

### `ToolResult`

```python
class ToolResult
```


The result of a tool call, rendered for the wire and sent back to the model.

Built and sent by [`RealtimeSession`][pydantic_ai.realtime.RealtimeSession] after it settles a
call: the string-only realtime tool channel and the retry/failure error-key wrapping mean the
session renders the [`ToolReturnPart`][pydantic_ai.messages.ToolReturnPart] or
[`RetryPromptPart`][pydantic_ai.messages.RetryPromptPart] it records in history down to this flat
shape, so every provider sends exactly the same rendering.

```python
tool_call_id: str
```

```python
_: KW_ONLY
```

```python
output: str
```

```python
content: Sequence[UserContent] | None = None
```

### `TextContext`

```python
class TextContext
```


A text item added to the conversation as context, without asking the model to respond (like an image).

```python
text: str
```

### `CommitAudio`

```python
class CommitAudio
```


Commit the buffered input audio as a user turn (manual turn-taking / push-to-talk).

Only needed when automatic voice activity detection is disabled; with server-side VAD the
provider commits audio and triggers a response automatically.

### `ClearAudio`

```python
class ClearAudio
```


Discard any buffered, uncommitted input audio.

### `CreateResponse`

```python
class CreateResponse
```


Ask the model to generate a response now (manual turn-taking, after `CommitAudio`).

### `CancelResponse`

```python
class CancelResponse
```


Cancel the model's in-progress response (maps to the provider's response-cancel).

### `TruncateOutput`

```python
class TruncateOutput
```


Truncate the model's current audio output at `audio_end_ms`.

After a barge-in the user only heard part of the model's audio. Truncating tells the provider how
much was actually played, so its stored transcript matches and the conversation context stays
consistent. The provider resolves which output item to truncate from its own state unless
`item_id` names one.

```python
audio_end_ms: int
```

```python
_: KW_ONLY
```

```python
item_id: str | None = None
```

### `AudioDelta`

```python
class AudioDelta
```


A chunk of audio output from the model.

```python
data: bytes
```

```python
_: KW_ONLY
```

```python
item_id: str | None = None
```

```python
response_id: str | None = None
```

### `OutputTranscript`

```python
class OutputTranscript
```


The model's textual output (partial or final): an audio transcript, or plain text output.

```python
text: str
```

```python
_: KW_ONLY
```

```python
is_final: bool = False
```

```python
output_text: bool = False
```

```python
item_id: str | None = None
```

```python
response_id: str | None = None
```

### `InputTranscript`

```python
class InputTranscript
```


A transcription of the user's audio input (partial or final).

Providers with per-item IDs use `item_id` to associate interleaved transcripts with the correct
user turn. Providers without them retain arrival-order association.

```python
text: str
```

```python
_: KW_ONLY
```

```python
is_final: bool = False
```

```python
item_id: str | None = None
```

```python
cumulative: bool = False
```

### `ToolCall`

```python
class ToolCall
```


The model is requesting a tool call.

```python
tool_call_id: str
```

```python
_: KW_ONLY
```

```python
tool_name: str
```

```python
args: str
```

```python
response_usage_follows: bool = False
```

```python
item_id: str | None = None
```

```python
response_id: str | None = None
```

### `ToolCallCancelled`

```python
class ToolCallCancelled
```


The model cancelled in-flight tool calls (e.g. the user barged in before they finished).

Gemini Live sends this as `toolCallCancellation`; the session cancels the matching running tool
tasks so their now-unwanted results are never sent back to the model.

```python
tool_call_ids: list[str]
```

### `ResponseDone`

```python
class ResponseDone
```


The provider reported that its current response is done.

This codec event is consumed by the session to finalize a
[`ModelResponse`][pydantic_ai.messages.ModelResponse]. Providers do not necessarily report a
terminal for every model response the session records in history.

```python
_: KW_ONLY
```

```python
interrupted: bool = False
```

```python
provider_response_id: str | None = None
```

```python
finish_reason: FinishReason | None = None
```

```python
provider_details: dict[str, Any] | None = None
```

```python
more_expected: bool = False
```

```python
event_kind: Literal['response_done'] = 'response_done'
```

### `SessionUsage`

```python
class SessionUsage
```


Usage reported by the provider for a model response or another run-level operation.

```python
usage: RequestUsage
```

```python
_: KW_ONLY
```

```python
provider_response_id: str | None = None
```

```python
finish_reason: FinishReason | None = None
```

```python
provider_details: dict[str, Any] | None = None
```

```python
response_scoped: bool = True
```

```python
context_window_used: float | None = None
```

```python
event_kind: Literal['session_usage'] = 'session_usage'
```

### `ConversationCreated`

```python
class ConversationCreated
```


An OpenAI-protocol server assigned a conversation ID.

This is a codec-level control event. Providers consume it during their handshake when possible;
the session silently consumes any instance that reaches the live stream.

```python
conversation_id: str
```

### `ConversationItemCreated`

```python
class ConversationItemCreated
```


An OpenAI-protocol server reported a conversation item.

xAI uses `replayed=True` for item events emitted during the resume handshake. The session consumes
those items and remembers their newly assigned IDs so any follow-on content or tool events aren't
appended or executed again.

```python
_: KW_ONLY
```

```python
item_id: str | None = None
```

```python
tool_call_id: str | None = None
```

```python
replayed: bool = False
```

### `InputRejected`

```python
class InputRejected
```


The provider refused part of an input this connection was sent, so it had no effect.

Yielded just ahead of the [`RealtimeSessionErrorEvent`][pydantic_ai.realtime.RealtimeSessionErrorEvent]
that explains the refusal, and only when the provider's error identifies the frame it refused (the
OpenAI protocol echoes the client `event_id`). A connection that can't tell which input an error was
about yields the error alone. A reconnect whose new session no longer has an input (Gemini resumes
from a handle that can predate a typed turn) yields it too, ahead of the
[`RealtimeSessionReconnectEvent`][pydantic_ai.realtime.RealtimeSessionReconnectEvent]. The session
uses it to take back what it assumed the input did: a
refused request for a response releases the reply
[`wait_for_reply()`][pydantic_ai.realtime.RealtimeSession.wait_for_reply] would otherwise wait for
forever, and refused content is removed from history.

```python
input_index: int
```

```python
_: KW_ONLY
```

```python
refused: Literal['content', 'response']
```

### `RealtimeConnection`

```python
class RealtimeConnection
```


A live connection to a realtime model.

Providers implement this to handle protocol-specific framing (WebSocket frames,
HTTP/2 messages, etc.). Content is fed in via [`send`][pydantic_ai.realtime.codec.RealtimeConnection.send]
and events are consumed by iterating the connection.

```python
transport_errors: ClassVar[tuple[type[Exception], ...]] = ()
```

#### `send`

```python
async def send(self, content: RealtimeInput) -> None
```


Feed content into the session.

Concrete connections accept provider-specific data and control inputs. OpenAI accepts audio,
text, images, tool results, manual turn controls, cancellation, and truncation; Gemini accepts
audio, text, images, and tool results. A high-level
[`RealtimeSession`][pydantic_ai.realtime.RealtimeSession] checks profile-gated operations and
raises [`UserError`][pydantic_ai.exceptions.UserError], as does a connection handed an input it
can't send.



```python
_lifecycle_version: ClassVar[int] = 1
```





#### `model_name`

```python
def model_name(self) -> str | None
```


The model id the server reported serving this session, when the provider reports one.

Captured from the connect handshake (e.g. the OpenAI protocol's `session.created`). It can
differ from the requested model id: xAI accepts any model slug and silently substitutes its
current default, reporting the actually-served model only here. `None` when the provider
doesn't report one (e.g. Gemini Live). The session stamps this on each
[`ModelResponse.model_name`][pydantic_ai.messages.ModelResponse.model_name], mirroring how
request-response models record the response's reported model rather than the requested one.

#### `set_message_history`

```python
def set_message_history(self, message_history: Callable[[], Sequence[ModelMessage]]) -> None
```


Tell the connection how to read the message history as it currently stands.

A [`RealtimeSession`][pydantic_ai.realtime.RealtimeSession] calls this when it takes ownership of
the connection, so a provider that loses server-side state on
[reconnect][pydantic_ai.realtime.ReconnectPolicy] can replay the conversation into the new
session instead of resuming with total amnesia. The session's history grows as the call goes on,
hence a callable rather than a snapshot.

A no-op by default: providers with native session resumption (Gemini Live, xAI) have nothing to
replay, and one that can't seed a session at all has nowhere to put it.

#### `input_transcription_enabled`

```python
def input_transcription_enabled(self) -> bool
```


Whether this connection will emit [`InputTranscript`][pydantic_ai.realtime.codec.InputTranscript] events for the user's audio.

Providers that transcribe the user's input (the default) leave this `True`. When it is `False`,
no transcript arrives, so [`RealtimeSession`][pydantic_ai.realtime.RealtimeSession] finalizes a
user turn from retained input audio instead (see `audio_retention`). Defaults to `True` so a
connection that doesn't override it never triggers the audio-only path (which would risk a
duplicate turn if transcripts did arrive).

#### `interrupts_response_on_speech`

```python
def interrupts_response_on_speech(self) -> bool
```


Whether the configured turn detection makes the *server* cancel the active response when user speech starts.

OpenAI-protocol server VAD with `interrupt_response` enabled (the default) cancels the
in-progress response on speech onset by itself. A client cancel sent at that same moment can
race the server's own cancellation and be applied to the *next* response instead, silencing
the reply to the barge-in — so the session's automatic barge-in handling sends only the
truncation when this is `True`. Defaults to `False`, which keeps the client-side cancel.







#### `reconnect_restores_in_flight_state`

```python
def reconnect_restores_in_flight_state(self) -> bool
```


Whether a reconnect continues the response and tool calls that were in flight when the socket dropped.

Otherwise it only brings back the finalized conversation. Native session resumption (xAI Grok Voice) restores the in-flight generation server-side, and
Gemini Live settles the cut turn in the connection before its
[`RealtimeSessionReconnectEvent`][pydantic_ai.messages.RealtimeSessionReconnectEvent], so in
both the [`RealtimeSession`][pydantic_ai.realtime.RealtimeSession] must not settle again and
trusts `state_restored`. Local replay (OpenAI, Azure OpenAI) restores only finalized turns, so
the session settles the interrupted turn itself and reports `state_restored=False`. Defaults to
`True`; the OpenAI connection overrides it.



