# `pydantic_ai.models.test`

Utility model for quickly testing apps built with Pydantic AI.

Here's a minimal example:

```py {title="test_model_usage.py" call_name="test_my_agent" noqa="I001"}
from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel

my_agent = Agent('openai:gpt-5.2', instructions='...')


async def test_my_agent():
    """Unit test for my_agent, to be run by pytest."""
    m = TestModel()
    with my_agent.override(model=m):
        result = await my_agent.run('Testing my agent...')
        assert result.output == 'success (no tool calls)'
    assert m.last_model_request_parameters is not None
    assert m.last_model_request_parameters.function_tools == []
```

See [Unit testing with `TestModel`](../../testing.md#unit-testing-with-testmodel) for detailed documentation.





### `TestModel`

```python
class TestModel
```


A model specifically for testing purposes.

This will (by default) call all tools in the agent, then return a tool response if possible,
otherwise a plain response.

How useful this model is will vary significantly.

Apart from `__init__` derived by the `dataclass` decorator, all methods are private or match those
of the base class.

```python
call_tools: list[str] | Literal['all'] = 'all'
```

```python
custom_output_text: str | None = None
```

```python
custom_output_args: Any | None = None
```

```python
seed: int = 0
```

```python
last_model_request_parameters: ModelRequestParameters | None = field(default=None, init=False)
```

```python
_model_name: str = field(default='test', repr=False)
```

```python
_system: str = field(default='test', repr=False)
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


TestModel supports all native tools for testing flexibility.

`ToolSearchTool` is excluded because TestModel can't emulate provider-native
tool search. Auto-injected `ToolSearch` capabilities work transparently thanks
to the local `search_tools` fallback.

### `TestStreamedResponse`

```python
class TestStreamedResponse
```


A structured response that streams test data.

```python
_model_name: str
```

```python
_structured_response: ModelResponse
```

```python
_messages: InitVar[Iterable[ModelMessage]]
```

```python
_provider_name: str
```

```python
_provider_url: str | None = None
```

```python
_allow_tool_availability_deltas: bool = False
```

```python
_timestamp: datetime = field(default_factory=_utils.now_utc, init=False)
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
def provider_url(self) -> str | None
```


Get the provider base URL.

#### `timestamp`

```python
def timestamp(self) -> datetime
```


Get the timestamp of the response.

