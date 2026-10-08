# `pydantic_ai.models.huggingface`

## Setup

For details on how to set up authentication with this model, see [model configuration for Hugging Face](../../models/huggingface.md).

### `HuggingFaceModelSettings`

```python
class HuggingFaceModelSettings
```


Settings used for a Hugging Face model request.

### `HuggingFaceModel`

```python
class HuggingFaceModel
```


A model that uses Hugging Face Inference Providers.

Internally, this uses the [HF Python client](https://github.com/huggingface/huggingface_hub) to interact with the API.

Apart from `__init__`, all methods are private or match those of the base class.

```python
_model_name: str = field(repr=False)
```

```python
_provider: Provider[AsyncInferenceClient] = field(repr=False)
```



#### `base_url`

```python
def base_url(self) -> str
```


The base URL of the provider.

#### `model_name`

```python
def model_name(self) -> HuggingFaceModelName
```


The model name.

#### `system`

```python
def system(self) -> str
```


The system / model provider.









### `HuggingFaceStreamedResponse`

```python
class HuggingFaceStreamedResponse
```


Implementation of `StreamedResponse` for Hugging Face models.

```python
_model_name: str
```

```python
_model_profile: ModelProfile
```

```python
_response: _utils.PeekableAsyncStream[ChatCompletionStreamOutput, AsyncIterable[ChatCompletionStreamOutput]]
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
_timestamp: datetime = field(default_factory=_utils.now_utc)
```

#### `model_name`

```python
def model_name(self) -> str
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