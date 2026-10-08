# pydantic_ai.models.mcp_sampling

### `MCPSamplingModelSettings`

```python
class MCPSamplingModelSettings
```


Settings used for an MCP Sampling model request.

```python
mcp_model_preferences: ModelPreferences
```

### `MCPSamplingModel`

```python
class MCPSamplingModel
```


A model that uses MCP Sampling.

[MCP Sampling](https://modelcontextprotocol.io/docs/concepts/sampling)
allows an MCP server to make requests to a model by calling back to the MCP client that connected to it.

```python
session: ServerSession
```

```python
_: KW_ONLY
```

```python
default_max_tokens: int = 16384
```

#### `model_name`

```python
def model_name(self) -> str
```


The model name.

Since the model name isn't known until the request is made, this property always returns `'mcp-sampling'`.

#### `system`

```python
def system(self) -> str
```


The system / model provider, returns `'MCP'`.