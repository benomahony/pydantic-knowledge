# `pydantic_ai.models.xai`

## Setup

For details on how to set up authentication with this model, see [model configuration for xAI](../../models/xai.md).

xAI model implementation using [xAI SDK](https://github.com/xai-org/xai-sdk-python).







### `XaiModelSettings`

```python
class XaiModelSettings
```


Settings specific to xAI models.

See [xAI SDK documentation](https://docs.x.ai/docs) for more details on these parameters.

```python
xai_logprobs: bool
```

```python
xai_top_logprobs: int
```

```python
xai_user: str
```

```python
xai_store_messages: bool
```

```python
xai_previous_response_id: str
```

```python
xai_include_encrypted_content: bool
```

```python
xai_include_code_execution_output: bool
```

```python
xai_include_web_search_output: bool
```

```python
xai_include_inline_citations: bool
```

```python
xai_include_mcp_output: bool
```

```python
xai_include_x_search_output: bool
```

```python
xai_include_collections_search_output: bool
```

```python
xai_include_attachment_search_output: bool
```

```python
xai_reasoning_effort: GrokReasoningEffort
```

```python
xai_max_turns: int
```

```python
xai_agent_count: int
```

### `XaiModel`

```python
class XaiModel
```


A model that uses the xAI SDK to interact with xAI models.

```python
_model_name: str
```

```python
_provider: Provider[AsyncClient]
```



#### `model_name`

```python
def model_name(self) -> str
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























#### `request`

```python
async def request(self, messages: list[ModelMessage], model_settings: ModelSettings | None, model_request_parameters: ModelRequestParameters) -> ModelResponse
```


Make a request to the xAI model.

#### `request_stream`

```python
async def request_stream(self, messages: list[ModelMessage], model_settings: ModelSettings | None, model_request_parameters: ModelRequestParameters, run_context: RunContext[Any] | None=None) -> AsyncGenerator[StreamedResponse]
```


Make a streaming request to the xAI model.





### `XaiStreamedResponse`

```python
class XaiStreamedResponse
```


Implementation of `StreamedResponse` for xAI SDK.

```python
_model_name: str
```

```python
_response: _utils.PeekableAsyncStream[tuple[chat_types.Response, chat_types.Chunk], AsyncIterator[tuple[chat_types.Response, Any]]]
```

```python
_timestamp: datetime
```

```python
_provider: Provider[AsyncClient]
```

#### `system`

```python
def system(self) -> str
```


The model provider system name.

#### `provider_url`

```python
def provider_url(self) -> str
```


Get the provider base URL.







#### `model_name`

```python
def model_name(self) -> str
```


Get the model name of the response.

#### `provider_name`

```python
def provider_name(self) -> str
```


The model provider.

#### `timestamp`

```python
def timestamp(self) -> datetime
```


Get the timestamp of the response.



























