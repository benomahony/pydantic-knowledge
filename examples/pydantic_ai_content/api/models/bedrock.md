# `pydantic_ai.models.bedrock`

## Setup

For details on how to set up authentication with this model, see [model configuration for Bedrock](../../models/bedrock.md).







### `BedrockModelSettings`

```python
class BedrockModelSettings
```


Settings for Bedrock models.

See [the Bedrock Converse API docs](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html#API_runtime_Converse_RequestSyntax) for a full list.
See [the boto3 implementation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime/client/converse.html) of the Bedrock Converse API.

`extra_headers` are injected before the request is signed, so under SigV4 authentication they are covered by the
signature (except the few headers botocore never signs, e.g. `X-Amzn-Trace-Id`). Headers the AWS SDK computes
itself (e.g. `Authorization`, `User-Agent`, `X-Amz-Date`) are overwritten by botocore afterwards.

```python
bedrock_guardrail_config: GuardrailConfigurationTypeDef
```

```python
bedrock_performance_configuration: PerformanceConfigurationTypeDef
```

```python
bedrock_request_metadata: dict[str, str]
```

```python
bedrock_additional_model_response_fields_paths: list[str]
```

```python
bedrock_prompt_variables: Mapping[str, PromptVariableValuesTypeDef]
```

```python
bedrock_additional_model_requests_fields: Mapping[str, Any]
```

```python
bedrock_cache_tool_definitions: bool | Literal['5m', '1h']
```

```python
bedrock_cache_instructions: bool | Literal['5m', '1h']
```

```python
bedrock_cache_messages: bool | Literal['5m', '1h']
```

```python
bedrock_service_tier: ServiceTierTypeDef
```

```python
bedrock_inference_profile: str
```

### `BedrockConverseModel`

```python
class BedrockConverseModel
```


A model that uses the Bedrock Converse API.

```python
_model_name: BedrockModelName = field(repr=False)
```

```python
_provider: Provider[BaseClient] = field(repr=False)
```

```python
_client: BaseClient | None = field(default=None, repr=False)
```



#### `client`

```python
def client(self) -> BedrockRuntimeClient
```


The boto3 client used to make requests to the Bedrock Converse API.

Defaults to the client from the [`Provider`][pydantic_ai.providers.Provider]. It can be reassigned, e.g. to
rotate short-lived credentials in a long-running service, but prefer assigning to
[`BedrockProvider.client`][pydantic_ai.providers.bedrock.BedrockProvider.client] so all models sharing the
provider pick up the new client. Once you've assigned a client here, you're responsible for keeping it valid;
the provider's client is no longer consulted.

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

#### `resolve_cache_retention`

```python
def resolve_cache_retention(self, model_settings: ModelSettings | None) -> timedelta | None
```


Resolve the longest retention requested by supported Bedrock cache settings.

#### `supported_native_tools`

```python
def supported_native_tools(cls) -> frozenset[type[AbstractNativeTool]]
```


The set of builtin tool types this model can handle.







#### `count_tokens`

```python
async def count_tokens(self, messages: list[ModelMessage], model_settings: ModelSettings | None, model_request_parameters: ModelRequestParameters) -> usage.RequestUsage
```


Count the number of tokens, works with limited models.

Check the actual supported models on <https://docs.aws.amazon.com/bedrock/latest/userguide/count-tokens.html>













### `BedrockStreamedResponse`

```python
class BedrockStreamedResponse
```


Implementation of `StreamedResponse` for Bedrock models.

```python
_model_name: BedrockModelName
```

```python
_model_profile: BedrockModelProfile
```

```python
_event_stream: EventStream[ConverseStreamOutputTypeDef]
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
_timestamp: datetime = field(default_factory=_utils.now_utc)
```

```python
_provider_response_id: str | None = None
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







