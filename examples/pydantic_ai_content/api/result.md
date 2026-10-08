# `pydantic_ai.result`

### `StreamedRunResult`

```python
class StreamedRunResult
```


Result of a streamed run that returns structured data via a tool call.

```python
_all_messages: list[_messages.ModelMessage]
```

```python
_new_message_index: int
```

```python
_stream_response: AgentStream[AgentDepsT, OutputDataT] | None = None
```

```python
_on_complete: Callable[[], Awaitable[None]] | None = None
```

```python
_run_result: AgentRunResult[OutputDataT] | None = None
```

```python
is_complete: bool = field(default=False, init=False)
```

#### `result`

```python
def result(self) -> AgentRunResult[OutputDataT]
```


This run as an [`AgentRunResult`][pydantic_ai.run.AgentRunResult], once the stream has finished.

A `StreamedRunResult` reads its values off the stream that is producing them, so it lives only as
long as that stream does. `AgentRunResult` is the settled form of the same run — the same output,
messages, usage and IDs — and it has a
[serialized shape](../message-history.md#storing-complete-run-results) you can store and load. Reach
for this to hand the run to code that outlives the stream.

Raises:
    UserError: If the stream hasn't finished, or was cancelled before producing an output,
        so the run has no settled output to settle on.

#### `all_messages`

```python
def all_messages(self, *, output_tool_return_content: str | None=None) -> list[_messages.ModelMessage]
```


Return the history of _messages.

Args:
    output_tool_return_content: The return content of the tool call to set in the last message.
        This provides a convenient way to modify the content of the output tool call if you want to continue
        the conversation and want to set the response to the output tool call. If `None`, the last message will
        not be modified.

Returns:
    List of messages.

#### `all_messages_json`

```python
def all_messages_json(self, *, output_tool_return_content: str | None=None) -> bytes
```


Return all messages from [`all_messages`][pydantic_ai.result.StreamedRunResult.all_messages] as JSON bytes.

Args:
    output_tool_return_content: The return content of the tool call to set in the last message.
        This provides a convenient way to modify the content of the output tool call if you want to continue
        the conversation and want to set the response to the output tool call. If `None`, the last message will
        not be modified.

Returns:
    JSON bytes representing the messages.

#### `new_messages`

```python
def new_messages(self, *, output_tool_return_content: str | None=None) -> list[_messages.ModelMessage]
```


Return the messages produced during this run.

Messages provided via `message_history` and messages from older runs are excluded.

Args:
    output_tool_return_content: The return content of the tool call to set in the last message.
        This provides a convenient way to modify the content of the output tool call if you want to continue
        the conversation and want to set the response to the output tool call. If `None`, the last message will
        not be modified.

Returns:
    List of new messages.

#### `new_messages_json`

```python
def new_messages_json(self, *, output_tool_return_content: str | None=None) -> bytes
```


Return new messages from [`new_messages`][pydantic_ai.result.StreamedRunResult.new_messages] as JSON bytes.

Args:
    output_tool_return_content: The return content of the tool call to set in the last message.
        This provides a convenient way to modify the content of the output tool call if you want to continue
        the conversation and want to set the response to the output tool call. If `None`, the last message will
        not be modified.

Returns:
    JSON bytes representing the new messages.

#### `stream_output`

```python
async def stream_output(self, *, debounce_by: float | None=0.1) -> AsyncIterator[OutputDataT]
```


Stream the output as an async iterable.

The pydantic validator for structured data will be called in
[partial mode](https://docs.pydantic.dev/dev/concepts/experimental/#partial-validation)
on each iteration.

Args:
    debounce_by: by how much (if at all) to debounce/group the output chunks by. `None` means no debouncing.
        Debouncing is particularly important for long structured outputs to reduce the overhead of
        performing validation as each token is received.

Returns:
    An async iterable of the response data.

#### `stream_text`

```python
async def stream_text(self, *, delta: bool=False, debounce_by: float | None=0.1) -> AsyncIterator[str]
```


Stream the text result as an async iterable.

!!! note
    [`TextOutput`][pydantic_ai.output.TextOutput] functions are not applied — use
    [`stream_output()`][pydantic_ai.result.StreamedRunResult.stream_output] instead.
    Result validators will NOT be called on the text result if `delta=True`.

Args:
    delta: if `True`, yield each chunk of text as it is received, if `False` (default), yield the full text
        up to the current point.
    debounce_by: by how much (if at all) to debounce/group the response chunks by. `None` means no debouncing.
        Debouncing is particularly important for long structured responses to reduce the overhead of
        performing validation as each token is received.

#### `stream_response`

```python
async def stream_response(self, *, debounce_by: float | None=0.1) -> AsyncIterator[_messages.ModelResponse]
```


Stream the response as an async iterable of `ModelResponse` snapshots.

Each yielded `ModelResponse` is the current state of the response: `response.state` is
`'incomplete'` while streaming is in flight and `'complete'` (or `'interrupted'` if
[`cancel()`][pydantic_ai.result.StreamedRunResult.cancel] was called) on the final yield.

Args:
    debounce_by: by how much (if at all) to debounce/group the response chunks by. `None` means no debouncing.
        Debouncing is particularly important for long structured responses to reduce the overhead of
        performing validation as each token is received.

Returns:
    An async iterable of `ModelResponse` snapshots.

#### `get_output`

```python
async def get_output(self) -> OutputDataT
```


Stream the whole response, validate and return it.

#### `response`

```python
def response(self) -> _messages.ModelResponse
```


Return the current state of the response.

#### `metadata`

```python
def metadata(self) -> dict[str, Any] | None
```


Metadata associated with this agent run, if configured.

#### `workspace`

```python
def workspace(self) -> Workspace
```


The workspace used by this run.

#### `usage`

```python
def usage(self) -> RunUsage
```


Return the usage of the whole run.

!!! note
    This won't return the full usage until the stream is finished.

#### `timestamp`

```python
def timestamp(self) -> datetime
```


Get the timestamp of the response.

#### `run_id`

```python
def run_id(self) -> str
```


The unique identifier for the agent run.

#### `conversation_id`

```python
def conversation_id(self) -> str
```


The unique identifier for the conversation this run belongs to.

#### `validate_response_output`

```python
async def validate_response_output(self, message: _messages.ModelResponse, *, allow_partial: bool=False) -> OutputDataT
```


Validate a structured result message.



#### `cancel`

```python
async def cancel(self) -> None
```


Cancel local stream consumption and request provider shutdown.

Whether this stops remote generation or closes the underlying transport depends on the provider SDK.

The interrupted response state is recorded in the message history so that
`all_messages()` includes it.

This stops only the current model response; the run continues. To end the whole run,
use [`AgentRun.cancel()`][pydantic_ai.run.AgentRun.cancel] or
[`RunContext.cancel()`][pydantic_ai.tools.RunContext.cancel].

#### `cancelled`

```python
def cancelled(self) -> bool
```


Whether the stream has been cancelled via `cancel()`.

### `StreamedRunResultSync`

```python
class StreamedRunResultSync
```


Synchronous wrapper for [`StreamedRunResult`][pydantic_ai.result.StreamedRunResult] that only exposes sync methods.

All of the run's async work happens on the caller's event loop. Context-manager and iterator
lifecycles remain in stable tasks, so cancel scopes entered and exited by the agent graph never
straddle tasks and OpenTelemetry spans stay correctly nested. The wrapper must be used and closed
on the thread where it was created.

This is a synchronous context manager; the underlying stream is cleaned up on exit:

```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-5.2')

def main():
    with agent.run_stream_sync('What is the capital of the UK?') as response:
        print(response.get_output())
        #> The capital of the UK is London.
```

Using it without a `with` block also works for backwards compatibility. Garbage collection requests
best-effort cleanup on the owner loop, but it cannot drive a stopped owner loop from another thread
or while another loop is running. A `with` block should be used whenever deterministic cleanup matters.

```python
_streamed_run_result: StreamedRunResult[AgentDepsT, OutputDataT]
```

#### `all_messages`

```python
def all_messages(self, *, output_tool_return_content: str | None=None) -> list[_messages.ModelMessage]
```


Return the history of messages.

Args:
    output_tool_return_content: The return content of the tool call to set in the last message.
        This provides a convenient way to modify the content of the output tool call if you want to continue
        the conversation and want to set the response to the output tool call. If `None`, the last message will
        not be modified.

Returns:
    List of messages.

#### `all_messages_json`

```python
def all_messages_json(self, *, output_tool_return_content: str | None=None) -> bytes
```


Return all messages from [`all_messages`][pydantic_ai.result.StreamedRunResultSync.all_messages] as JSON bytes.

Args:
    output_tool_return_content: The return content of the tool call to set in the last message.
        This provides a convenient way to modify the content of the output tool call if you want to continue
        the conversation and want to set the response to the output tool call. If `None`, the last message will
        not be modified.

Returns:
    JSON bytes representing the messages.

#### `new_messages`

```python
def new_messages(self, *, output_tool_return_content: str | None=None) -> list[_messages.ModelMessage]
```


Return the messages produced during this run.

Messages provided via `message_history` and messages from older runs are excluded.

Args:
    output_tool_return_content: The return content of the tool call to set in the last message.
        This provides a convenient way to modify the content of the output tool call if you want to continue
        the conversation and want to set the response to the output tool call. If `None`, the last message will
        not be modified.

Returns:
    List of new messages.

#### `new_messages_json`

```python
def new_messages_json(self, *, output_tool_return_content: str | None=None) -> bytes
```


Return new messages from [`new_messages`][pydantic_ai.result.StreamedRunResultSync.new_messages] as JSON bytes.

Args:
    output_tool_return_content: The return content of the tool call to set in the last message.
        This provides a convenient way to modify the content of the output tool call if you want to continue
        the conversation and want to set the response to the output tool call. If `None`, the last message will
        not be modified.

Returns:
    JSON bytes representing the new messages.

#### `stream_output`

```python
def stream_output(self, *, debounce_by: float | None=0.1) -> Iterator[OutputDataT]
```


Stream the output as an iterable.

The pydantic validator for structured data will be called in
[partial mode](https://docs.pydantic.dev/dev/concepts/experimental/#partial-validation)
on each iteration.

Args:
    debounce_by: by how much (if at all) to debounce/group the output chunks by. `None` means no debouncing.
        Debouncing is particularly important for long structured outputs to reduce the overhead of
        performing validation as each token is received.

Returns:
    An iterable of the response data.

#### `stream_text`

```python
def stream_text(self, *, delta: bool=False, debounce_by: float | None=0.1) -> Iterator[str]
```


Stream the text result as an iterable.

!!! note
    [`TextOutput`][pydantic_ai.output.TextOutput] functions are not applied — use
    [`stream_output()`][pydantic_ai.result.StreamedRunResultSync.stream_output] instead.
    Result validators will NOT be called on the text result if `delta=True`.

Args:
    delta: if `True`, yield each chunk of text as it is received, if `False` (default), yield the full text
        up to the current point.
    debounce_by: by how much (if at all) to debounce/group the response chunks by. `None` means no debouncing.
        Debouncing is particularly important for long structured responses to reduce the overhead of
        performing validation as each token is received.

#### `stream_response`

```python
def stream_response(self, *, debounce_by: float | None=0.1) -> Iterator[_messages.ModelResponse]
```


Stream the response as an iterable of `ModelResponse` snapshots.

Each yielded `ModelResponse` is the current state of the response: `response.state` is
`'incomplete'` while streaming is in flight and `'complete'` on the final yield.

Args:
    debounce_by: by how much (if at all) to debounce/group the response chunks by. `None` means no debouncing.
        Debouncing is particularly important for long structured responses to reduce the overhead of
        performing validation as each token is received.

Returns:
    An iterable of `ModelResponse` snapshots.

#### `get_output`

```python
def get_output(self) -> OutputDataT
```


Stream the whole response, validate and return it.

#### `response`

```python
def response(self) -> _messages.ModelResponse
```


Return the current state of the response.

#### `usage`

```python
def usage(self) -> RunUsage
```


Return the usage of the whole run.

!!! note
    This won't return the full usage until the stream is finished.

#### `timestamp`

```python
def timestamp(self) -> datetime
```


Get the timestamp of the response.

#### `run_id`

```python
def run_id(self) -> str
```


The unique identifier for the agent run.

#### `conversation_id`

```python
def conversation_id(self) -> str
```


The unique identifier for the conversation this run belongs to.

#### `metadata`

```python
def metadata(self) -> dict[str, Any] | None
```


Metadata associated with this agent run, if configured.

#### `workspace`

```python
def workspace(self) -> Workspace
```


The workspace used by this run.

#### `validate_response_output`

```python
def validate_response_output(self, message: _messages.ModelResponse, *, allow_partial: bool=False) -> OutputDataT
```


Validate a structured result message.

#### `is_complete`

```python
def is_complete(self) -> bool
```


Whether the stream has all been received.

This is set to `True` when one of
[`stream_output`][pydantic_ai.result.StreamedRunResultSync.stream_output],
[`stream_text`][pydantic_ai.result.StreamedRunResultSync.stream_text],
[`stream_response`][pydantic_ai.result.StreamedRunResultSync.stream_response] or
[`get_output`][pydantic_ai.result.StreamedRunResultSync.get_output] completes.

### `FinalResult`

```python
class FinalResult
```


Marker class storing the final output of an agent run and associated metadata.

```python
output: OutputDataT
```

```python
tool_name: str | None = None
```

```python
tool_call_id: str | None = None
```

