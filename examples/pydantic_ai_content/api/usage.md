# `pydantic_ai.usage`

### `RequestUsage`

```python
class RequestUsage
```


LLM usage associated with a single request.

This is an implementation of `genai_prices.types.AbstractUsage` so it can be used to calculate the price of the
request using [genai-prices](https://github.com/pydantic/genai-prices).

#### `incr`

```python
def incr(self, incr_usage: RequestUsage) -> None
```


Increment the usage in place.

Args:
    incr_usage: The usage to increment by.



#### `extract`

```python
def extract(cls, data: Any, *, provider: str, provider_url: str, provider_fallback: str, api_flavor: str='default', details: dict[str, Any] | None=None) -> RequestUsage
```


Extract usage information from the response data using genai-prices.

Args:
    data: The response data from the model API.
    provider: The actual provider ID
    provider_url: The provider base_url
    provider_fallback: The fallback provider ID to use if the actual provider is not found in genai-prices.
        For example, an OpenAI model should set this to "openai" in case it has an obscure provider ID.
    api_flavor: The API flavor to use when extracting usage information,
        e.g. 'chat' or 'responses' for OpenAI.
    details: Becomes the `details` field on the returned `RequestUsage` for convenience.

### `RunUsage`

```python
class RunUsage
```


LLM usage associated with an agent run.

Responsibility for calculating request usage is on the model; Pydantic AI simply sums the usage information across requests.

```python
requests: int = 0
```

```python
tool_calls: int = 0
```

```python
input_tokens: int = 0
```

```python
cache_write_tokens: int = 0
```

```python
cache_read_tokens: int = 0
```

```python
input_audio_tokens: int = 0
```

```python
cache_audio_read_tokens: int = 0
```

```python
output_tokens: int = 0
```

```python
details: dict[str, int] = dataclasses.field(default_factory=dict[str, int])
```

#### `incr`

```python
def incr(self, incr_usage: RunUsage | RequestUsage) -> None
```


Increment the usage in place.

Args:
    incr_usage: The usage to increment by.







### `UsageLimits`

```python
class UsageLimits
```


Limits on model usage.

The request count is tracked by pydantic_ai, and the request limit is checked before each request to the model.
Token counts are provided in responses from the model, and the token limits are checked after each response.

Each of the limits can be set to `None` to disable that limit.

```python
cost_limit: Decimal | None = None
```

```python
request_limit: int | None = 50
```

```python
tool_calls_limit: int | None = None
```

```python
input_tokens_limit: int | None = None
```

```python
output_tokens_limit: int | None = None
```

```python
total_tokens_limit: int | None = None
```

```python
per_request_input_tokens_limit: int | None = None
```

```python
count_tokens_before_request: bool = False
```

#### `has_token_limits`

```python
def has_token_limits(self) -> bool
```


Returns `True` if this instance places any limits on token counts.

If this returns `False`, the `check_tokens` and `check_per_request_input_tokens` methods will never raise an error.

This is useful because if we have token limits, we need to check them after receiving each streamed message.
If there are no limits, we can skip that processing in the streaming response iterator.

#### `check_before_request`

```python
def check_before_request(self, usage: RunUsage) -> None
```


Raises a `UsageLimitExceeded` exception if the next request would exceed any of the limits.

#### `check_cost`

```python
def check_cost(self, usage: RunUsage, *, warn_if_cost_unavailable: bool=True) -> None
```


Check whether usage exceeds the cost limit.

Args:
    usage: The accumulated run usage to check.
    warn_if_cost_unavailable: Whether to warn when a `cost_limit` is set but no cost was calculated.

#### `check_tokens`

```python
def check_tokens(self, usage: RunUsage) -> None
```


Raises a `UsageLimitExceeded` exception if the usage exceeds any of the token limits.

#### `check_before_tool_call`

```python
def check_before_tool_call(self, projected_usage: RunUsage) -> None
```


Raises a `UsageLimitExceeded` exception if the next tool call(s) would exceed the tool call limit.

#### `check_per_request_input_tokens`

```python
def check_per_request_input_tokens(self, request_input_tokens: int) -> None
```


Raises a `UsageLimitExceeded` if the per-request input tokens exceed the limit.

This checks a single request's input token count — not the cumulative
`RunUsage.input_tokens` — against `per_request_input_tokens_limit`.## `pydantic_ai.prices`

Keep model prices up to date by downloading the latest price list in the background.

### `update_in_background`

```python
def update_in_background() -> UpdatePrices
```


Download the latest model prices now, and again every hour, in the background.

Pydantic AI bundles model prices at release time. Call this when your app starts to estimate
costs for models released after you installed it.

Downloads never block your code. If one fails, the last good price list stays in use and the
failure is logged to the `genai-prices` logger.

Returns the updater. Call `stop()` when your app shuts down.

To download from your own URL or on a different schedule, use
[`genai_prices.UpdatePrices`](https://github.com/pydantic/genai-prices/blob/main/packages/python/README.md#updateprices)
directly. It shares one background download with this function.