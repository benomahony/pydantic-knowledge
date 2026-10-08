# `pydantic_ai.models.google`

Interface that uses the [`google-genai`](https://pypi.org/project/google-genai/) package under the hood to
access Google's Gemini models via both the Gemini API and Google Cloud (formerly known as Vertex AI).

## Setup

For details on how to set up authentication with this model, see [model configuration for Google](../../models/google.md).

### `GoogleModelSettings`

```python
class GoogleModelSettings
```


Settings used for a Gemini model request.

```python
google_safety_settings: list[SafetySettingDict]
```

```python
google_thinking_config: ThinkingConfigDict
```

```python
google_labels: dict[str, str]
```

```python
google_video_resolution: MediaResolution
```

```python
google_cached_content: str
```

```python
google_logprobs: bool
```

```python
google_top_logprobs: int
```

```python
google_cloud_service_tier: GoogleCloudServiceTier
```

```python
google_model_armor_config: ModelArmorConfigDict
```

















### `GoogleModel`

```python
class GoogleModel
```


A model that uses Gemini via `generativelanguage.googleapis.com` API.

This is implemented from scratch rather than using a dedicated SDK, good API documentation is
available [here](https://ai.google.dev/api).

Apart from `__init__`, all methods are private or match those of the base class.

```python
_model_name: GoogleModelName = field(repr=False)
```

```python
_provider: Provider[Client] = field(repr=False)
```



#### `model_name`

```python
def model_name(self) -> GoogleModelName
```


The model name.

#### `system`

```python
def system(self) -> str
```


The model provider.



#### `profile`

```python
def profile(self) -> GoogleModelProfile
```


The model profile.

When the client talks to the Gemini API, `gemini-3.1-flash-image` models default to
`google_thinking_levels` of `MINIMAL` and `HIGH`; on Vertex AI they keep the full scale. A
`google_thinking_levels` set by the provider or the `profile=` argument takes precedence.

`ImageGenerationTool` is only supported when `supports_image_output` is true, so a text model
falls back to the local tool an `ImageGeneration` capability provides.

#### `supported_native_tools`

```python
def supported_native_tools(cls) -> frozenset[type[AbstractNativeTool]]
```


Return the set of native tool types this model can handle.





















### `GeminiStreamedResponse`

```python
class GeminiStreamedResponse
```


Implementation of `StreamedResponse` for the Gemini model.

```python
_model_name: GoogleModelName
```

```python
_response: _utils.PeekableAsyncStream[GenerateContentResponse, AsyncIterator[GenerateContentResponse]]
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
_web_search_billed_per_prompt: bool = False
```

```python
_timestamp: datetime = field(default_factory=_utils.now_utc)
```

```python
_file_search_tool_call_ids: list[str] = field(default_factory=list[str], init=False)
```

```python
_code_execution_tool_call_id: str | None = field(default=None, init=False)
```

```python
_has_content_filter: bool = field(default=False, init=False)
```

```python
_has_tool_invocations: bool = field(default=False, init=False)
```

```python
_pending_file_search_returns: list[NativeToolReturnPart] = field(default_factory=list[NativeToolReturnPart], init=False)
```

```python
_pending_web_search_return: NativeToolReturnPart | None = field(default=None, init=False)
```







#### `model_name`

```python
def model_name(self) -> GoogleModelName
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























