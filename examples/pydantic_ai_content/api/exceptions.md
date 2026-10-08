# `pydantic_ai.exceptions`

### `ModelRetry`

```python
class ModelRetry
```


Exception to raise to request a model retry.

Can be raised from tool functions, output validators, and capability hooks
(such as `after_model_request`, `after_tool_execute`, etc.) to send
a retry prompt back to the model asking it to try again.

For a terminal failure the model should see but not retry, raise
[`ToolFailed`][pydantic_ai.exceptions.ToolFailed] instead.

```python
message: str
```



### `ToolFailed`

```python
class ToolFailed
```


Exception to raise to report a terminal tool failure to the model.

Raise this when a tool call is done and has failed — a missing resource, an unsupported
operation, a definitive upstream error — and you want the model to see the failure
and adapt rather than try the same call again. Can be raised from tool functions, args
validators, and tool validation/execution hooks.

Like [`ModelRetry`][pydantic_ai.exceptions.ModelRetry], this produces a failed tool result the
model sees; unlike `ModelRetry` it does not prepend retry/correction instructions and does not
consume the tool's retry budget. Bound repeated failures with
[`UsageLimits`][pydantic_ai.usage.UsageLimits] at the run level instead.

```python
message: str
```



### `CallDeferred`

```python
class CallDeferred
```


Exception to raise when a tool call should be deferred.

See [tools docs](../deferred-tools.md#deferred-tools) for more information.

Args:
    metadata: Optional dictionary of metadata to attach to the deferred tool call.
        This metadata will be available in `DeferredToolRequests.metadata` keyed by `tool_call_id`.

### `ApprovalRequired`

```python
class ApprovalRequired
```


Exception to raise when a tool call requires human-in-the-loop approval.

See [tools docs](../deferred-tools.md#human-in-the-loop-tool-approval) for more information.

Args:
    metadata: Optional dictionary of metadata to attach to the deferred tool call.
        This metadata will be available in `DeferredToolRequests.metadata` keyed by `tool_call_id`.

### `SkipModelRequest`

```python
class SkipModelRequest
```


Exception to raise in before/wrap model request hooks to skip the model call.

The provided response will be used instead of calling the model.

Note: when raised in `before_model_request`, any message history modifications
made by earlier capabilities in that hook will not be persisted to the agent's
message history, since the request preparation is aborted.

```python
response: ModelResponse
```

### `SkipToolValidation`

```python
class SkipToolValidation
```


Exception to raise in before/wrap tool validate hooks to skip validation.

The provided args will be used as the validated arguments.

```python
validated_args: dict[str, Any]
```

### `SkipToolExecution`

```python
class SkipToolExecution
```


Exception to raise in before/wrap tool execute hooks to skip execution.

The provided result will be used as the tool result.

```python
result: Any
```

### `UserError`

```python
class UserError
```


Error caused by a usage mistake by the application developer — You!

```python
message: str
```

### `UndrainedPendingMessagesError`

```python
class UndrainedPendingMessagesError
```


Error that used to be raised when an agent run ended with messages still queued via `enqueue`.

A bare `async for node in agent_run` loop used to skip the node hooks, so `'when_idle'`
messages and end-of-run redirects (which drain in `after_node_run`) were stranded. Bare
iteration now advances through [`AgentRun.next()`][pydantic_ai.run.AgentRun.next] like every
other way of driving a run, so pending messages always drain and this error is no longer
raised. It is kept so existing `except` clauses keep working.

### `AgentRunError`

```python
class AgentRunError
```


Base class for errors occurring during an agent run.

```python
message: str
```

### `RunCancelled`

```python
class RunCancelled
```


Raised when the agent run was cancelled by the application itself.

Raised by [`AgentRun.cancel()`][pydantic_ai.run.AgentRun.cancel] and
[`RunContext.cancel()`][pydantic_ai.tools.RunContext.cancel].
This is a normal, catchable application-level outcome: the run stopped because your own code
asked it to. External cancellation of the task running the agent (`asyncio.Task.cancel()`,
a timeout scope, workflow cancellation under durable execution) is infrastructure-level and
keeps propagating as `asyncio.CancelledError` instead — it is never translated into this
exception, and when both race, the external cancellation wins. (On Python 3.10, which lacks
`Task.uncancel()`, the race cannot be disambiguated and a requested first-party cancellation
wins instead.)

Everything the run completed before the cancellation took effect — including the partial
response of an interrupted stream and the results of tool calls that finished — is preserved
in [`all_messages()`][pydantic_ai.exceptions.RunCancelled.all_messages]: pass it as
`message_history` to a new run (with a new user prompt or not) to resume the conversation; any
tool calls that never produced a result are automatically closed out with synthesized
`outcome='interrupted'` returns before the history is sent to a model.

Cancellation is terminal: capability hooks (`wrap_run`, `wrap_node_run`, `on_run_error`) may
observe it and clean up, but cannot recover a cancelled run into a successful result.

#### `from_cancellation`

```python
def from_cancellation(cls, exc: BaseException) -> RunCancelled | None
```


Recover run state from a cancellation-related exception.

External cancellation of a plain `agent.run()` keeps its standard asyncio semantics. Catch
it with `except asyncio.CancelledError as exc`, then call
`RunCancelled.from_cancellation(exc)` to access the partial run state attached by Pydantic
AI. This also works with the `TimeoutError` raised by `asyncio.timeout()` or
`asyncio.wait_for()`, whose exception chain contains the original `CancelledError`, and with
the `KeyboardInterrupt` raised by pressing Ctrl-C during `agent.run_sync()`. An
external `CancelledError` must keep propagating for timeouts and task groups to tear down
correctly, so re-raise it after capturing the state rather than returning from the handler;
only a first-party `RunCancelled` is yours to consume.

Passing a `RunCancelled` directly returns the same instance, providing uniform handling for
first-party and external cancellation paths.

Python 3.11+ preserves the exception instance across an `await task` boundary. Python 3.10
recreates the `CancelledError` there, but chains the original exception — and the attached
run state — via `__context__`, which this method traverses; the chain is attached only to
the first `await` of the cancelled task, so later awaits of the same task see an unchained
exception. Use `capture_run_messages()` as the fallback when only message history is needed.

#### `all_messages`

```python
def all_messages(self) -> list[ModelMessage]
```


Return the complete resumable history of the cancelled run.

This is a DETACHED snapshot of the run's message history at termination, ready to pass as
`message_history` for a resumed run.

Returns:
    List of messages.

#### `all_messages_json`

```python
def all_messages_json(self) -> bytes
```


Return all messages from [`all_messages`][pydantic_ai.exceptions.RunCancelled.all_messages] as JSON bytes.

Returns:
    JSON bytes representing the messages.

#### `new_messages`

```python
def new_messages(self) -> list[ModelMessage]
```


Return the messages produced during the cancelled run.

Messages provided via `message_history` and messages from older runs are excluded.

Returns:
    List of new messages.

#### `new_messages_json`

```python
def new_messages_json(self) -> bytes
```


Return new messages from [`new_messages`][pydantic_ai.exceptions.RunCancelled.new_messages] as JSON bytes.

Returns:
    JSON bytes representing the new messages.

#### `response`

```python
def response(self) -> ModelResponse
```


Return the last response from the message history.

Raises:
    ValueError: If the run was cancelled before receiving any model response.

#### `timestamp`

```python
def timestamp(self) -> datetime
```


Return the timestamp of the last response.

Raises:
    ValueError: If the run was cancelled before receiving any model response.

#### `usage`

```python
def usage(self) -> RunUsage
```


Return the usage of the cancelled run.

#### `metadata`

```python
def metadata(self) -> dict[str, Any] | None
```


Metadata associated with this agent run, if configured.

#### `run_id`

```python
def run_id(self) -> str | None
```


The unique identifier for the agent run, or `None` if it was cancelled before starting.

#### `conversation_id`

```python
def conversation_id(self) -> str | None
```


The conversation identifier, or `None` if the run was cancelled before starting.

### `SuspendedResponseExpired`

```python
class SuspendedResponseExpired
```


Raised when resuming a suspended response whose server-side job is no longer available.

Suspended/background jobs are only resumable within the provider's retention window (e.g. ~10
minutes for OpenAI background mode). Resuming a persisted suspended response after that window
raises this instead of an opaque provider HTTP error; start a new run from the preceding messages
to retry from scratch.

### `UsageLimitExceeded`

```python
class UsageLimitExceeded
```


Error raised when a Model's usage exceeds the specified limits.

### `ConcurrencyLimitExceeded`

```python
class ConcurrencyLimitExceeded
```


Error raised when the concurrency queue depth exceeds max_queued.

### `UnexpectedModelBehavior`

```python
class UnexpectedModelBehavior
```


Error caused by unexpected Model behavior, e.g. an unexpected response code.

```python
message: str
```

```python
body: str | None
```

### `ContentFilterError`

```python
class ContentFilterError
```


Raised when content filtering is triggered by the model provider.

### `ModelAPIError`

```python
class ModelAPIError
```


Raised when a model provider API request fails.

```python
model_name: str
```

### `ModelHTTPError`

```python
class ModelHTTPError
```


Raised when a model provider response has a status code of 4xx or 5xx.

```python
status_code: int
```

```python
body: object | None
```

```python
headers: dict[str, str] | None
```

```python
suggested_model_id: str | None
```

#### `retry_after`

```python
def retry_after(self) -> float | None
```


Seconds to wait before retrying, parsed from the `Retry-After` response header.

Returns `None` when the header is absent or cannot be parsed. The header value
is interpreted first as an integer number of seconds, then as an
[HTTP-date](https://httpwg.org/specs/rfc9110.html#http.date) string.

### `FallbackExceptionGroup`

```python
class FallbackExceptionGroup
```


A group of exceptions that can be raised when all fallback models fail.

### `ToolRetryError`

```python
class ToolRetryError
```


Exception used to signal a `ToolRetry` message should be returned to the LLM.



### `ToolFailedError`

```python
class ToolFailedError
```


Exception used to signal a failed `ToolReturnPart` should be returned to the LLM.

### `IncompleteToolCall`

```python
class IncompleteToolCall
```


Error raised when a model stops due to token limit while emitting a tool call.

### `MessageHistoryMutatedWarning`

```python
class MessageHistoryMutatedWarning
```


Warning raised when in-place mutation of the message history is detected at the end of a run.

Mutating messages that are already part of the run's history in place (e.g.
`ctx.messages[0].parts[0].content = '...'` from a tool) is not supported: the per-request
`gen_ai.input.messages` span attribute caches each message's serialized form, so spans recorded
after the mutation may not match the messages actually sent to the model. The run-level
`pydantic_ai.all_messages` attribute is always serialized fresh and does reflect the mutation.
To transform history mid-run, build new message or part objects instead — e.g. with
`dataclasses.replace`, passing the message a new `parts` list (replacing a message in the
history and reassigning its `parts` list are both safe) — for instance in a history processor
([`ProcessHistory`][pydantic_ai.capabilities.ProcessHistory]).

The warning is best-effort: it's raised when a mutation is detected at the end of a successful
run, which covers messages still present in the final history. Errored runs aren't checked —
with warnings configured as errors, the warning would displace the run's own exception. Its
absence does not guarantee that no stale span was recorded.