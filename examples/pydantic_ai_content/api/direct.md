# `pydantic_ai.direct`

Methods for making imperative requests to language models with minimal abstraction.

These methods allow you to make requests to LLMs where the only abstraction is input and output schema
translation so you can use all models with the same API.

These methods are thin wrappers around [`Model`][pydantic_ai.models.Model] implementations.



### `model_request`

```python
async def model_request(model: models.Model | models.KnownModelName | str, messages: Sequence[messages.ModelMessage], *, model_settings: settings.ModelSettings | None=None, model_request_parameters: models.ModelRequestParameters | None=None, instrument: instrumented_models.InstrumentationSettings | bool | None=None) -> messages.ModelResponse
```


Make a non-streamed request to a model.

```py title="model_request_example.py"
from pydantic_ai import ModelRequest
from pydantic_ai.direct import model_request


async def main():
    model_response = await model_request(
        'anthropic:claude-haiku-4-5',
        [ModelRequest.user_text_prompt('What is the capital of France?')]  # (1)!
    )
    print(model_response)
    '''
    ModelResponse(
        parts=[TextPart(content='The capital of France is Paris.')],
        usage=RequestUsage(input_tokens=56, output_tokens=7),
        model_name='claude-haiku-4-5',
        timestamp=datetime.datetime(...),
    )
    '''
```

1. See [`ModelRequest.user_text_prompt`][pydantic_ai.messages.ModelRequest.user_text_prompt] for details.

Args:
    model: The model to make a request to. We allow `str` here since the actual list of allowed models changes frequently.
    messages: Messages to send to the model
    model_settings: optional model settings
    model_request_parameters: optional model request parameters
    instrument: Whether to instrument the request with OpenTelemetry/Logfire, if `None` the value from
        [`logfire.instrument_pydantic_ai`][logfire.Logfire.instrument_pydantic_ai] is used.

Returns:
    The model response and token usage associated with the request.

### `model_request_sync`

```python
def model_request_sync(model: models.Model | models.KnownModelName | str, messages: Sequence[messages.ModelMessage], *, model_settings: settings.ModelSettings | None=None, model_request_parameters: models.ModelRequestParameters | None=None, instrument: instrumented_models.InstrumentationSettings | bool | None=None) -> messages.ModelResponse
```


Make a Synchronous, non-streamed request to a model.

This is a convenience method that wraps [`model_request`][pydantic_ai.direct.model_request] with
`loop.run_until_complete(...)`. You therefore can't use this method inside async code or if there's an active event loop.

```py title="model_request_sync_example.py"
from pydantic_ai import ModelRequest
from pydantic_ai.direct import model_request_sync

model_response = model_request_sync(
    'anthropic:claude-haiku-4-5',
    [ModelRequest.user_text_prompt('What is the capital of France?')]  # (1)!
)
print(model_response)
'''
ModelResponse(
    parts=[TextPart(content='The capital of France is Paris.')],
    usage=RequestUsage(input_tokens=56, output_tokens=7),
    model_name='claude-haiku-4-5',
    timestamp=datetime.datetime(...),
)
'''
```

1. See [`ModelRequest.user_text_prompt`][pydantic_ai.messages.ModelRequest.user_text_prompt] for details.

Args:
    model: The model to make a request to. We allow `str` here since the actual list of allowed models changes frequently.
    messages: Messages to send to the model
    model_settings: optional model settings
    model_request_parameters: optional model request parameters
    instrument: Whether to instrument the request with OpenTelemetry/Logfire, if `None` the value from
        [`logfire.instrument_pydantic_ai`][logfire.Logfire.instrument_pydantic_ai] is used.

Returns:
    The model response and token usage associated with the request.

### `model_request_stream`

```python
def model_request_stream(model: models.Model | models.KnownModelName | str, messages: Sequence[messages.ModelMessage], *, model_settings: settings.ModelSettings | None=None, model_request_parameters: models.ModelRequestParameters | None=None, instrument: instrumented_models.InstrumentationSettings | bool | None=None) -> AbstractAsyncContextManager[models.StreamedResponse]
```


Make a streamed async request to a model.

```py {title="model_request_stream_example.py"}

from pydantic_ai import ModelRequest
from pydantic_ai.direct import model_request_stream


async def main():
    messages = [ModelRequest.user_text_prompt('Who was Albert Einstein?')]  # (1)!
    async with model_request_stream('openai:gpt-5-mini', messages) as stream:
        chunks = []
        async for chunk in stream:
            chunks.append(chunk)
        print(chunks)
        '''
        [
            PartStartEvent(index=0, part=TextPart(content='Albert Einstein was ')),
            FinalResultEvent(tool_name=None, tool_call_id=None),
            PartDeltaEvent(
                index=0, delta=TextPartDelta(content_delta='a German-born theoretical ')
            ),
            PartDeltaEvent(index=0, delta=TextPartDelta(content_delta='physicist.')),
            PartEndEvent(
                index=0,
                part=TextPart(
                    content='Albert Einstein was a German-born theoretical physicist.'
                ),
            ),
        ]
        '''
```

1. See [`ModelRequest.user_text_prompt`][pydantic_ai.messages.ModelRequest.user_text_prompt] for details.

Args:
    model: The model to make a request to. We allow `str` here since the actual list of allowed models changes frequently.
    messages: Messages to send to the model
    model_settings: optional model settings
    model_request_parameters: optional model request parameters
    instrument: Whether to instrument the request with OpenTelemetry/Logfire, if `None` the value from
        [`logfire.instrument_pydantic_ai`][logfire.Logfire.instrument_pydantic_ai] is used.

Returns:
    A [stream response][pydantic_ai.models.StreamedResponse] async context manager.

### `model_request_stream_sync`

```python
def model_request_stream_sync(model: models.Model | models.KnownModelName | str, messages: Sequence[messages.ModelMessage], *, model_settings: settings.ModelSettings | None=None, model_request_parameters: models.ModelRequestParameters | None=None, instrument: instrumented_models.InstrumentationSettings | bool | None=None) -> StreamedResponseSync
```


Make a streamed synchronous request to a model.

This is the synchronous version of [`model_request_stream`][pydantic_ai.direct.model_request_stream].
It drives the asynchronous stream on the caller's event loop while providing a synchronous iterator interface.
The returned context manager must be used and closed on the thread where the synchronous stream is created.

```py {title="model_request_stream_sync_example.py"}

from pydantic_ai import ModelRequest
from pydantic_ai.direct import model_request_stream_sync

messages = [ModelRequest.user_text_prompt('Who was Albert Einstein?')]
with model_request_stream_sync('openai:gpt-5-mini', messages) as stream:
    chunks = []
    for chunk in stream:
        chunks.append(chunk)
    print(chunks)
    '''
    [
        PartStartEvent(index=0, part=TextPart(content='Albert Einstein was ')),
        FinalResultEvent(tool_name=None, tool_call_id=None),
        PartDeltaEvent(
            index=0, delta=TextPartDelta(content_delta='a German-born theoretical ')
        ),
        PartDeltaEvent(index=0, delta=TextPartDelta(content_delta='physicist.')),
        PartEndEvent(
            index=0,
            part=TextPart(
                content='Albert Einstein was a German-born theoretical physicist.'
            ),
        ),
    ]
    '''
```

Args:
    model: The model to make a request to. We allow `str` here since the actual list of allowed models changes frequently.
    messages: Messages to send to the model
    model_settings: optional model settings
    model_request_parameters: optional model request parameters
    instrument: Whether to instrument the request with OpenTelemetry/Logfire, if `None` the value from
        [`logfire.instrument_pydantic_ai`][logfire.Logfire.instrument_pydantic_ai] is used.

Returns:
    A [sync stream response][pydantic_ai.direct.StreamedResponseSync] context manager.

### `StreamedResponseSync`

```python
class StreamedResponseSync
```


Synchronous wrapper for an async streaming response, running the whole stream on the caller's event loop.

The stream uses the internal `SyncStreamBridge` to keep context-manager
and iterator lifecycles in stable tasks. Exiting the `with` block cancels the underlying request promptly
and closes the connection instead of waiting for the whole response to arrive.

This class must be used as a context manager with the `with` statement. The synchronous stream is created
when the `with` block is entered and must be used and closed on that thread.

```python
_async_stream_cm: AbstractAsyncContextManager[StreamedResponse]
```

```python
_bridge: SyncStreamBridge[StreamedResponse] | None = field(default=None, init=False)
```

```python
_context_entered: bool = field(default=False, init=False)
```



#### `response`

```python
def response(self) -> messages.ModelResponse
```


Get the current state of the response.

#### `usage`

```python
def usage(self) -> RequestUsage
```


Get the usage of the response so far.

#### `model_name`

```python
def model_name(self) -> str
```


Get the model name of the response.

#### `timestamp`

```python
def timestamp(self) -> datetime
```


Get the timestamp of the response.