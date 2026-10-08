# `pydantic_ai.models.groq`

## Setup

For details on how to set up authentication with this model, see [model configuration for Groq](../../models/groq.md).

### `GroqModelSettings`

```python
class GroqModelSettings
```


Settings used for a Groq model request.

```python
groq_reasoning_format: Literal['hidden', 'raw', 'parsed']
```

```python
groq_reasoning_effort: Literal['none', 'default', 'low', 'medium', 'high']
```

### `GroqModel`

```python
class GroqModel
```


A model that uses the Groq API.

Internally, this uses the [Groq Python client](https://github.com/groq/groq-python) to interact with the API.

Apart from `__init__`, all methods are private or match those of the base class.

```python
_model_name: GroqModelName = field(repr=False)
```

```python
_provider: Provider[AsyncGroq] = field(repr=False)
```



#### `model_name`

```python
def model_name(self) -> GroqModelName
```


The model name.

#### `system`

```python
def system(self) -> str
```


The model provider.

#### `supported_native_tools`

```python
def supported_native_tools(cls) -> frozenset[type[AbstractNativeTool]]
```


Return the set of builtin tool types this model can handle.











### `GroqStreamedResponse`

```python
class GroqStreamedResponse
```


Implementation of `StreamedResponse` for Groq models.

```python
_model_name: GroqModelName
```

```python
_model_profile: ModelProfile
```

```python
_response: _utils.PeekableAsyncStream[chat.ChatCompletionChunk, AsyncStream[chat.ChatCompletionChunk]]
```

```python
_provider_name: str
```

```python
_model_id_namespace: str
```

```python
_provider_url: str
```

```python
_provider_timestamp: datetime | None = None
```

```python
_timestamp: datetime = field(default_factory=_utils.now_utc)
```

#### `model_name`

```python
def model_name(self) -> GroqModelName
```


Get the model name of the response.

#### `provider_name`

```python
def provider_name(self) -> str
```


Get the provider name.

#### `provider_url`

```python
def provider_url(self) -> str
```


Get the provider base URL.

#### `timestamp`

```python
def timestamp(self) -> datetime
```


Get the timestamp of the response.