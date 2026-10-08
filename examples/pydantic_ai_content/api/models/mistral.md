# `pydantic_ai.models.mistral`

## Setup

For details on how to set up authentication with this model, see [model configuration for Mistral](../../models/mistral.md).

### `MistralModelSettings`

```python
class MistralModelSettings
```


Settings used for a Mistral model request.

```python
mistral_prompt_cache_key: str
```

### `MistralModel`

```python
class MistralModel
```


A model that uses Mistral.

Internally, this uses the [Mistral Python client](https://github.com/mistralai/client-python) to interact with the API.

[API Documentation](https://docs.mistral.ai/)

```python
json_mode_schema_prompt: str
```

```python
_model_name: MistralModelName = field(repr=False)
```

```python
_provider: Provider[Mistral] = field(repr=False)
```



#### `model_name`

```python
def model_name(self) -> MistralModelName
```


The model name.

#### `system`

```python
def system(self) -> str
```


The model provider.

#### `request`

```python
async def request(self, messages: list[ModelMessage], model_settings: ModelSettings | None, model_request_parameters: ModelRequestParameters) -> ModelResponse
```


Make a non-streaming request to the model from Pydantic AI call.

#### `request_stream`

```python
async def request_stream(self, messages: list[ModelMessage], model_settings: ModelSettings | None, model_request_parameters: ModelRequestParameters, run_context: RunContext[Any] | None=None) -> AsyncGenerator[StreamedResponse]
```


Make a streaming request to the model from Pydantic AI call.

























### `MistralStreamedResponse`

```python
class MistralStreamedResponse
```


Implementation of `StreamedResponse` for Mistral models.

```python
_model_name: MistralModelName
```

```python
_response: _utils.PeekableAsyncStream[MistralCompletionEvent, MistralEventStreamAsync[MistralCompletionEvent]]
```

```python
_provider_name: str
```

```python
_provider_url: str
```

```python
_provider_timestamp: datetime | None = None
```

```python
_timestamp: datetime = field(default_factory=_now_utc)
```

```python
_delta_content: str = field(default='', init=False)
```

#### `model_name`

```python
def model_name(self) -> MistralModelName
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







