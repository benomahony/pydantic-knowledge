# `pydantic_ai` — Concurrency

## `ConcurrencyLimitedModel`

```python
class ConcurrencyLimitedModel
```


A model wrapper that limits concurrent requests to the underlying model.

This wrapper applies concurrency limiting at the model level, ensuring that
the number of concurrent requests to the model does not exceed the configured
limit. This is useful for:

- Respecting API rate limits
- Managing resource usage
- Sharing a concurrency pool across multiple models

Example usage:
```python
from pydantic_ai import Agent
from pydantic_ai.models.concurrency import ConcurrencyLimitedModel

# Limit to 5 concurrent requests
model = ConcurrencyLimitedModel('openai:gpt-4o', limiter=5)
agent = Agent(model)

# Or share a limiter across multiple models
from pydantic_ai import ConcurrencyLimiter  # noqa E402

shared_limiter = ConcurrencyLimiter(max_running=10, name='openai-pool')
model1 = ConcurrencyLimitedModel('openai:gpt-4o', limiter=shared_limiter)
model2 = ConcurrencyLimitedModel('openai:gpt-4o-mini', limiter=shared_limiter)
```

```python
_limiter: AbstractConcurrencyLimiter
```



### `request`

```python
async def request(self, messages: list[ModelMessage], model_settings: ModelSettings | None, model_request_parameters: ModelRequestParameters) -> ModelResponse
```


Make a request to the model with concurrency limiting.

### `count_tokens`

```python
async def count_tokens(self, messages: list[ModelMessage], model_settings: ModelSettings | None, model_request_parameters: ModelRequestParameters) -> RequestUsage
```


Count tokens with concurrency limiting.

### `compact_messages`

```python
async def compact_messages(self, request_context: ModelRequestContext, *, instructions: str | None=None) -> ModelResponse
```


Compact messages with concurrency limiting.

### `request_stream`

```python
async def request_stream(self, messages: list[ModelMessage], model_settings: ModelSettings | None, model_request_parameters: ModelRequestParameters, run_context: RunContext[Any] | None=None) -> AsyncGenerator[StreamedResponse]
```


Make a streaming request to the model with concurrency limiting.## `limit_model_concurrency`

```python
def limit_model_concurrency(model: Model | KnownModelName, limiter: AnyConcurrencyLimit) -> Model
```


Wrap a model with concurrency limiting.

This is a convenience function to wrap a model with concurrency limiting.
If the limiter is None, the model is returned unchanged.

Args:
    model: The model to wrap.
    limiter: The concurrency limit configuration.

Returns:
    The wrapped model with concurrency limiting, or the original model if limiter is None.

Example:
```python
from pydantic_ai.models.concurrency import limit_model_concurrency

model = limit_model_concurrency('openai:gpt-4o', limiter=5)
```## `AbstractConcurrencyLimiter`

```python
class AbstractConcurrencyLimiter
```


Abstract base class for concurrency limiters.

Subclass this to create custom concurrency limiters
(e.g., Redis-backed distributed limiters).

Example:
```python
from pydantic_ai.concurrency import AbstractConcurrencyLimiter


class RedisConcurrencyLimiter(AbstractConcurrencyLimiter):
    def __init__(self, redis_client, key: str, max_running: int):
        self._redis = redis_client
        self._key = key
        self._max_running = max_running

    async def acquire(self, source: str) -> None:
        # Implement Redis-based distributed locking
        ...

    def release(self) -> None:
        # Release the Redis lock
        ...
```

### `acquire`

```python
async def acquire(self, source: str) -> None
```


Acquire a slot, waiting if necessary.

Args:
    source: Identifier for observability (e.g., 'model:gpt-4o').

### `release`

```python
def release(self) -> None
```


Release a slot.

This can run on a different task than the matching `acquire()`: a streamed model response
is iterated and closed on whichever task consumes it.## `ConcurrencyLimiter`

```python
class ConcurrencyLimiter
```


A concurrency limiter that tracks waiting operations for observability.

This class wraps an anyio.Semaphore and tracks the number of waiting operations.
When an operation has to wait to acquire a slot, a span is created for
observability purposes.

Slots are not owned by tasks. Each successful `acquire()` must be paired with one
`release()`, which can run on a different task. Calling `acquire()` again consumes another
slot and waits if none is available.



### `from_limit`

```python
def from_limit(cls, limit: int | ConcurrencyLimit, *, name: str | None=None, tracer: Tracer | None=None) -> Self
```


Create a ConcurrencyLimiter from a ConcurrencyLimit configuration.

Args:
    limit: Either an int for simple limiting or a ConcurrencyLimit for full config.
    name: Optional name for this limiter, used for observability.
    tracer: OpenTelemetry tracer for span creation.

Returns:
    A configured ConcurrencyLimiter.

### `name`

```python
def name(self) -> str | None
```


Name of the limiter for observability.

### `waiting_count`

```python
def waiting_count(self) -> int
```


Number of operations currently waiting to acquire a slot.

### `running_count`

```python
def running_count(self) -> int
```


Number of operations currently running.

### `available_count`

```python
def available_count(self) -> int
```


Number of slots available.

### `max_running`

```python
def max_running(self) -> int
```


Maximum concurrent operations allowed.



### `acquire`

```python
async def acquire(self, source: str) -> None
```


Acquire a slot, creating a span if waiting is required.

Args:
    source: Identifier for the source of this acquisition (e.g., 'agent:my-agent' or 'model:gpt-4').

### `release`

```python
def release(self) -> None
```


Release a slot.## `ConcurrencyLimit`

```python
class ConcurrencyLimit
```


Configuration for concurrency limiting with optional backpressure.

Args:
    max_running: Maximum number of concurrent operations allowed. Must be >= 1.
    max_queued: Maximum number of operations waiting in the queue. Must be >= 0.
        If None, the queue is unlimited. If exceeded, raises `ConcurrencyLimitExceeded`.

```python
max_running: int
```

```python
max_queued: int | None = None
``````python
AnyConcurrencyLimit: TypeAlias = 'int | ConcurrencyLimit | AbstractConcurrencyLimiter | None'
```## `ConcurrencyLimitExceeded`

```python
class ConcurrencyLimitExceeded
```


Error raised when the concurrency queue depth exceeds max_queued.