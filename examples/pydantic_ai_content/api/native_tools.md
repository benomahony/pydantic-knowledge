# `pydantic_ai.native_tools`

### `AbstractNativeTool`

```python
class AbstractNativeTool
```


A native tool that can be used by an agent.

This class is abstract and cannot be instantiated directly.

The native tools are passed to the model as part of the `ModelRequestParameters`.

```python
kind: str = 'unknown_native_tool'
```

```python
optional: bool = False
```

#### `unique_id`

```python
def unique_id(self) -> str
```


A unique identifier for the native tool.

If multiple instances of the same native tool can be passed to the model, subclasses should override this property to allow them to be distinguished.

#### `label`

```python
def label(self) -> str
```


Human-readable label for UI display.

Subclasses should override this to provide a meaningful label.

### `WebSearchTool`

```python
class WebSearchTool
```


A native tool that allows your agent to search the web for information.

The parameters that PydanticAI passes depend on the model, as some parameters may not be supported by certain models.
OpenRouter uses its Beta web-search server tool, which lets the model decide whether to search and how often.
It accepts the portable settings below, though their effect depends on OpenRouter's selected
search engine and downstream provider.

Supported by:

* Anthropic
* OpenAI Responses
* Groq
* Google
* xAI
* OpenRouter

```python
search_context_size: Literal['low', 'medium', 'high'] = 'medium'
```

```python
user_location: WebSearchUserLocation | None = None
```

```python
blocked_domains: list[str] | None = None
```

```python
allowed_domains: list[str] | None = None
```

```python
max_uses: int | None = None
```

```python
external_web_access: bool | None = None
```

```python
kind: str = 'web_search'
```

### `WebSearchUserLocation`

```python
class WebSearchUserLocation
```


Allows you to localize search results based on a user's location.

Supported by:

* Anthropic
* OpenAI Responses
* xAI
* OpenRouter

```python
city: str
```

```python
country: str
```

```python
region: str
```

```python
timezone: str
```

### `XSearchTool`

```python
class XSearchTool
```


A native tool that allows your agent to search X/Twitter for posts and content.

See <https://docs.x.ai/developers/tools/x-search> for more details.

When used via the [`XSearch`][pydantic_ai.capabilities.XSearch] capability with a
`fallback_subagent_model` set, this tool also works with non-xAI models by delegating to a
subagent running the specified xAI model.

Supported by:

* xAI

```python
allowed_x_handles: list[str] | None = None
```

```python
excluded_x_handles: list[str] | None = None
```

```python
from_date: datetime | None = None
```

```python
to_date: datetime | None = None
```

```python
enable_image_understanding: bool = False
```

```python
enable_video_understanding: bool = False
```

```python
include_output: bool = False
```

```python
kind: str = 'x_search'
```

### `CodeExecutionTool`

```python
class CodeExecutionTool
```


A native tool that allows your agent to execute code.

Supported by:

* Anthropic
* OpenAI Responses
* Google
* Bedrock (Nova2.0)
* xAI

```python
files: list[UploadedFile] | None = None
```

```python
kind: str = 'code_execution'
```

### `WebFetchTool`

```python
class WebFetchTool
```


Allows your agent to access contents from URLs.

The parameters that PydanticAI passes depend on the model, as some parameters may not be supported by certain models.

Supported by:

* Anthropic
* Google

```python
max_uses: int | None = None
```

```python
allowed_domains: list[str] | None = None
```

```python
blocked_domains: list[str] | None = None
```

```python
enable_citations: bool = False
```

```python
max_content_tokens: int | None = None
```

```python
kind: str = 'web_fetch'
```

### `ImageGenerationTool`

```python
class ImageGenerationTool
```


A native tool that allows your agent to generate images.

Supported by:

* OpenAI Responses
* Google

```python
action: Literal['generate', 'edit', 'auto'] = 'auto'
```

```python
background: Literal['transparent', 'opaque', 'auto'] = 'auto'
```

```python
input_fidelity: Literal['high', 'low'] | None = None
```

```python
moderation: Literal['auto', 'low'] = 'auto'
```

```python
model: ImageGenerationModelName | None = None
```

```python
output_compression: int | None = None
```

```python
output_format: Literal['png', 'webp', 'jpeg'] | None = None
```

```python
partial_images: int = 0
```

```python
quality: Literal['low', 'medium', 'high', 'auto'] = 'auto'
```

```python
size: ImageSize | None = None
```

```python
aspect_ratio: ImageAspectRatio | None = None
```

```python
kind: str = 'image_generation'
```

### `MemoryTool`

```python
class MemoryTool
```


A native tool that allows your agent to use memory.

Supported by:

* Anthropic

```python
kind: str = 'memory'
```

### `MCPServerTool`

```python
class MCPServerTool
```


A native tool that allows your agent to use MCP servers.

Supported by:

* OpenAI Responses
* Anthropic
* xAI

```python
id: str
```

```python
url: str
```

```python
authorization_token: str | None = None
```

```python
description: str | None = None
```

```python
allowed_tools: list[str] | None = None
```

```python
headers: dict[str, str] | None = None
```

```python
kind: str = 'mcp_server'
```

### `FileSearchTool`

```python
class FileSearchTool
```


A native tool that allows your agent to search through uploaded files using vector search.

This tool provides a fully managed Retrieval-Augmented Generation (RAG) system that handles
file storage, chunking, embedding generation, and context injection into prompts.

Supported by:

* OpenAI Responses
* Google (Gemini)
* xAI (mapped to collections search)

```python
file_store_ids: Sequence[str]
```

```python
max_num_results: int | None = None
```

```python
instructions: str | None = None
```

```python
retrieval_mode: Literal['hybrid', 'semantic', 'keyword'] | None = None
```

```python
kind: str = 'file_search'
```

### `AdvisorTool`

```python
class AdvisorTool
```


A native tool that lets a faster executor model consult a stronger advisor model mid-generation.

The fields map 1:1 to the parameters of Anthropic's advisor tool definition. OpenRouter exposes
the advisor as a gateway server tool that honors a subset (`model`, `max_tokens`) and ignores
the unsupported fields; see the per-field docstrings for which provider supports each.

Supported by:

* Anthropic
* OpenRouter

```python
model: AdvisorModelName
```

```python
max_uses: int | None = None
```

```python
max_tokens: int | None = None
```

```python
caching: Literal['5m', '1h'] | None = None
```

```python
kind: str = 'advisor'
```