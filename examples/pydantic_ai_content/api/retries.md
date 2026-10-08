# `pydantic_ai.retries`

Retries utilities based on tenacity, especially for HTTP requests.

This module provides HTTP transport wrappers and wait strategies that integrate with
the tenacity library to add retry capabilities to HTTP requests. The transports can be
used with HTTP clients that support custom transports (such as `httpx2`), while the wait
strategies can be used with any tenacity retry decorator.

The module includes:
- HTTPX2TenacityTransport: Synchronous `httpx2` transport with retry capabilities
- AsyncHTTPX2TenacityTransport: Asynchronous `httpx2` transport with retry capabilities
- wait_retry_after: Wait strategy that respects HTTP Retry-After headers

### `RetryConfig`

```python
class RetryConfig
```


The configuration for tenacity-based retrying.

These are precisely the arguments to the tenacity `retry` decorator, and they are generally
used internally by passing them to that decorator via `@retry(**config)` or similar.

All fields are optional, and if not provided, the default values from the `tenacity.retry` decorator will be used.

```python
sleep: Callable[[int | float], None | Awaitable[None]]
```

```python
stop: StopBaseT
```

```python
wait: WaitBaseT
```

```python
retry: SyncRetryBaseT | RetryBaseT
```

```python
before: Callable[[RetryCallState], None | Awaitable[None]]
```

```python
after: Callable[[RetryCallState], None | Awaitable[None]]
```

```python
before_sleep: Callable[[RetryCallState], None | Awaitable[None]] | None
```

```python
reraise: bool
```

```python
retry_error_cls: type[RetryError]
```

```python
retry_error_callback: Callable[[RetryCallState], Any | Awaitable[Any]] | None
```

### `HTTPX2TenacityTransport`

```python
class HTTPX2TenacityTransport
```


Synchronous `httpx2` transport with Tenacity-based retry functionality.

This transport wraps another `httpx2` transport and adds retry capabilities using the tenacity library.
It can be configured to retry requests based on various conditions such as specific exception types,
response status codes, or custom validation logic.

The transport works by intercepting HTTP requests and responses, allowing the tenacity controller
to determine when and how to retry failed requests. The validate_response function can be used
to convert HTTP responses into exceptions that trigger retries.

Requests whose body is a non-replayable stream cannot be retried: the first attempt consumes the
stream, so a further attempt raises `httpx2.StreamConsumed`. Use a replayable body (e.g. bytes)
for requests that should be retried.

Args:
    config: The arguments to use for the tenacity `retry` decorator, including retry conditions,
        wait strategy, stop conditions, etc. See the tenacity docs for more info.
    wrapped: The underlying transport to wrap and add retry functionality to.
        Defaults to a new `httpx2.HTTPTransport`.
    validate_response: Optional callable that takes a Response and can raise an exception
        to be handled by the controller if the response should trigger a retry.
        Common use case is to raise exceptions for certain HTTP status codes.
        If None, no response validation is performed.

Example:
    ```python
    from httpx2 import Client, HTTPStatusError
    from tenacity import retry_if_exception_type, stop_after_attempt

    from pydantic_ai.retries import HTTPX2TenacityTransport, RetryConfig, wait_retry_after

    transport = HTTPX2TenacityTransport(
        RetryConfig(
            retry=retry_if_exception_type(HTTPStatusError),
            wait=wait_retry_after(max_wait=120),
            stop=stop_after_attempt(5),
            reraise=True
        ),
        validate_response=lambda r: r.raise_for_status()
    )
    client = Client(transport=transport)
    ```

#### `handle_request`

```python
def handle_request(self, request: httpx2.Request) -> httpx2.Response
```


Handle an HTTP request with retry logic.

Args:
    request: The HTTP request to handle.

Returns:
    The HTTP response.

Raises:
    RuntimeError: If the retry controller did not make any attempts.
    Exception: Any exception raised by the wrapped transport or validation function.

### `AsyncHTTPX2TenacityTransport`

```python
class AsyncHTTPX2TenacityTransport
```


Asynchronous `httpx2` transport with Tenacity-based retry functionality.

This transport wraps another async `httpx2` transport and adds retry capabilities using the tenacity library.
It can be configured to retry requests based on various conditions such as specific exception types,
response status codes, or custom validation logic.

The transport works by intercepting HTTP requests and responses, allowing the tenacity controller
to determine when and how to retry failed requests. The validate_response function can be used
to convert HTTP responses into exceptions that trigger retries.

Requests whose body is a non-replayable stream cannot be retried: the first attempt consumes the
stream, so a further attempt raises `httpx2.StreamConsumed`. Use a replayable body (e.g. bytes)
for requests that should be retried.

Args:
    config: The arguments to use for the tenacity `retry` decorator, including retry conditions,
        wait strategy, stop conditions, etc. See the tenacity docs for more info.
    wrapped: The underlying async transport to wrap and add retry functionality to.
        Defaults to a new `httpx2.AsyncHTTPTransport`.
    validate_response: Optional callable that takes a Response and can raise an exception
        to be handled by the controller if the response should trigger a retry.
        Common use case is to raise exceptions for certain HTTP status codes.
        If None, no response validation is performed.

Example:
    ```python
    from httpx2 import AsyncClient, HTTPStatusError
    from tenacity import retry_if_exception_type, stop_after_attempt

    from pydantic_ai.retries import (
        AsyncHTTPX2TenacityTransport,
        RetryConfig,
        wait_retry_after,
    )

    transport = AsyncHTTPX2TenacityTransport(
        RetryConfig(
            retry=retry_if_exception_type(HTTPStatusError),
            wait=wait_retry_after(max_wait=120),
            stop=stop_after_attempt(5),
            reraise=True
        ),
        validate_response=lambda r: r.raise_for_status()
    )
    client = AsyncClient(transport=transport)
    ```

#### `handle_async_request`

```python
async def handle_async_request(self, request: httpx2.Request) -> httpx2.Response
```


Handle an async HTTP request with retry logic.

Args:
    request: The HTTP request to handle.

Returns:
    The HTTP response.

Raises:
    RuntimeError: If the retry controller did not make any attempts.
    Exception: Any exception raised by the wrapped transport or validation function.

### `TenacityTransport`

```python
class TenacityTransport
```


Deprecated synchronous HTTPX transport with Tenacity-based retry functionality.

This transport wraps another BaseTransport and adds retry capabilities using the tenacity library.
It can be configured to retry requests based on various conditions such as specific exception types,
response status codes, or custom validation logic.

The transport works by intercepting HTTP requests and responses, allowing the tenacity controller
to determine when and how to retry failed requests. The validate_response function can be used
to convert HTTP responses into exceptions that trigger retries.

Args:
    wrapped: The underlying transport to wrap and add retry functionality to.
    config: The arguments to use for the tenacity `retry` decorator, including retry conditions,
        wait strategy, stop conditions, etc. See the tenacity docs for more info.
    validate_response: Optional callable that takes a Response and can raise an exception
        to be handled by the controller if the response should trigger a retry.
        Common use case is to raise exceptions for certain HTTP status codes.
        If None, no response validation is performed.

#### `handle_request`

```python
def handle_request(self, request: Request) -> Response
```


Handle an HTTP request with retry logic.

Args:
    request: The HTTP request to handle.

Returns:
    The HTTP response.

Raises:
    RuntimeError: If the retry controller did not make any attempts.
    Exception: Any exception raised by the wrapped transport or validation function.

### `AsyncTenacityTransport`

```python
class AsyncTenacityTransport
```


Deprecated asynchronous HTTPX transport with Tenacity-based retry functionality.

This transport wraps another AsyncBaseTransport and adds retry capabilities using the tenacity library.
It can be configured to retry requests based on various conditions such as specific exception types,
response status codes, or custom validation logic.

The transport works by intercepting HTTP requests and responses, allowing the tenacity controller
to determine when and how to retry failed requests. The validate_response function can be used
to convert HTTP responses into exceptions that trigger retries.

Args:
    wrapped: The underlying async transport to wrap and add retry functionality to.
    config: The arguments to use for the tenacity `retry` decorator, including retry conditions,
        wait strategy, stop conditions, etc. See the tenacity docs for more info.
    validate_response: Optional callable that takes a Response and can raise an exception
        to be handled by the controller if the response should trigger a retry.
        Common use case is to raise exceptions for certain HTTP status codes.
        If None, no response validation is performed.

#### `handle_async_request`

```python
async def handle_async_request(self, request: Request) -> Response
```


Handle an async HTTP request with retry logic.

Args:
    request: The HTTP request to handle.

Returns:
    The HTTP response.

Raises:
    RuntimeError: If the retry controller did not make any attempts.
    Exception: Any exception raised by the wrapped transport or validation function.

### `wait_retry_after`

```python
def wait_retry_after(fallback_strategy: Callable[[RetryCallState], float] | None=None, max_wait: float=300) -> Callable[[RetryCallState], float]
```


Create a tenacity-compatible wait strategy that respects HTTP Retry-After headers.

This wait strategy checks if the exception contains an httpx or httpx2 HTTPStatusError
with a Retry-After header, and if so, waits for the time specified in the header.
If no header is present or parsing fails, it falls back to the provided strategy.

The Retry-After header can be in two formats:
- An integer representing seconds to wait
- An HTTP date string representing when to retry

Args:
    fallback_strategy: Wait strategy to use when no Retry-After header is present
                      or parsing fails. Defaults to exponential backoff with max 60s.
    max_wait: Maximum time to wait in seconds, regardless of header value.
             Defaults to 300 (5 minutes).

Returns:
    A wait function that can be used with tenacity retry decorators.

Example:
    ```python
    from httpx2 import AsyncClient, HTTPStatusError
    from tenacity import retry_if_exception_type, stop_after_attempt

    from pydantic_ai.retries import (
        AsyncHTTPX2TenacityTransport,
        RetryConfig,
        wait_retry_after,
    )

    transport = AsyncHTTPX2TenacityTransport(
        RetryConfig(
            retry=retry_if_exception_type(HTTPStatusError),
            wait=wait_retry_after(max_wait=120),
            stop=stop_after_attempt(5),
            reraise=True
        ),
        validate_response=lambda r: r.raise_for_status()
    )
    client = AsyncClient(transport=transport)
    ```