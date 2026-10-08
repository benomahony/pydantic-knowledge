# pydantic_ai.models.fallback

### `ResponseRejected`

```python
class ResponseRejected
```


Raised within a `FallbackExceptionGroup` when model responses are rejected by a response handler.





### `FallbackModel`

```python
class FallbackModel
```


A model that uses one or more fallback models upon failure.

Apart from `__init__`, all methods are private or match those of the base class.

```python
models: list[Model]
```

```python
_exception_handlers: list[ExceptionHandler] = field(repr=False)
```

```python
_response_handlers: list[ResponseHandler] = field(repr=False)
```













#### `model_name`

```python
def model_name(self) -> str
```


The model name.

#### `model_id`

```python
def model_id(self) -> str
```


The fully qualified model identifier, combining the wrapped models' IDs.

#### `request`

```python
async def request(self, messages: list[ModelMessage], model_settings: ModelSettings | None, model_request_parameters: ModelRequestParameters) -> ModelResponse
```


Try each model in sequence until one succeeds.

In case of failure, raise a FallbackExceptionGroup with all exceptions.

If a previous response set `state='suspended'`, the request is routed directly
to the pinned continuation model, bypassing the fallback chain. If the pinned model
raises a fallback-eligible error during continuation, the messages are rewound
(stripping the suspended response and trailing continuation request) and the
normal fallback chain is tried.

#### `request_stream`

```python
async def request_stream(self, messages: list[ModelMessage], model_settings: ModelSettings | None, model_request_parameters: ModelRequestParameters, run_context: RunContext[Any] | None=None) -> AsyncGenerator[StreamedResponse]
```


Try each model in sequence until one succeeds.

If a previous response set `state='suspended'`, the request is routed directly
to the pinned continuation model, bypassing the fallback chain. If the pinned model
raises a fallback-eligible error while opening the stream, the messages are rewound
and the normal fallback chain is tried. Mid-stream failures still propagate.

#### `cancel_suspended_response`

```python
async def cancel_suspended_response(self, response: ModelResponse) -> None
```


Cancel a suspended continuation on the underlying model holding the server-side job.

When the response carries a continuation pin, resolve that model and delegate to it. Resolve
the pin directly from metadata rather than via `_get_continuation_model`: the cancel path is
driven by `_ContinuationStreamedResponse.get()`, whose `state` is already
`'interrupted'`/`'incomplete'`/`'complete'` (never `'suspended'`) by the time cancellation
unwinds, so gating on `state == 'suspended'` here would never find the pin.

When no pin resolves, the response can still hold a live server-side job: the pin is only
stamped when a segment *ends* suspended, so a streamed background job cancelled during its
first segment (e.g. OpenAI background mode, marked by `provider_details['background']` +
`provider_response_id`) has no pin yet. Best-effort delegate to every inner model so the job
is torn down rather than leaked. This is safe because each model's own cancel guard is strict
(OpenAI only acts on its own `background` marker with a matching `provider_name`; others
no-op), and a raising model doesn't stop the rest.

#### `context_window`

```python
def context_window(self) -> int | None
```


The smallest known context window among the candidate models, or `None` if none is known.

Any candidate may end up answering, and history that fits the smallest window fits them all,
so compacting against it errs towards compacting early rather than overflowing a fallback.
Candidates with an unknown window don't constrain the result.













