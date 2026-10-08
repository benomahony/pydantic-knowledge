# `pydantic_ai.mcp`



### `MCPError`

```python
class MCPError
```


Raised when an MCP server returns an error response.

This exception wraps error responses from MCP servers, following the ErrorData schema
from the MCP specification.

```python
message: str
```

```python
code: int
```

```python
data: dict[str, Any] | None
```

#### `from_mcp_sdk`

```python
def from_mcp_sdk(cls, error: McpError) -> MCPError
```


Create an MCPError from an MCP SDK McpError.

Args:
    error: An McpError from the MCP SDK.

### `ResourceAnnotations`

```python
class ResourceAnnotations
```


Additional properties describing MCP entities.

See the [resource annotations in the MCP specification](https://modelcontextprotocol.io/specification/2025-11-25/server/resources#annotations).

```python
audience: list[mcp_types.Role] | None = None
```

```python
priority: Annotated[float, Field(ge=0.0, le=1.0)] | None = None
```

```python
last_modified: str | None = None
```

#### `from_mcp_sdk`

```python
def from_mcp_sdk(cls, mcp_annotations: mcp_types.Annotations) -> ResourceAnnotations
```


Convert from MCP SDK Annotations to ResourceAnnotations.

Args:
    mcp_annotations: The MCP SDK annotations object.

### `Icon`

```python
class Icon
```


An icon for display in user interfaces.

```python
src: str
```

```python
mime_type: str | None = None
```

```python
sizes: list[str] | None = None
```

### `BaseResource`

```python
class BaseResource
```


Base class for MCP resources.

```python
name: str
```

```python
title: str | None = None
```

```python
description: str | None = None
```

```python
mime_type: str | None = None
```

```python
annotations: ResourceAnnotations | None = None
```

```python
icons: list[Icon] | None = None
```

```python
metadata: dict[str, Any] | None = None
```

### `Resource`

```python
class Resource
```


A resource that can be read from an MCP server.

See the [resources in the MCP specification](https://modelcontextprotocol.io/specification/2025-11-25/server/resources).

```python
uri: str
```

```python
size: int | None = None
```

#### `from_mcp_sdk`

```python
def from_mcp_sdk(cls, mcp_resource: mcp_types.Resource) -> Resource
```


Convert from MCP SDK Resource to PydanticAI Resource.

Args:
    mcp_resource: The MCP SDK Resource object.

### `ResourceTemplate`

```python
class ResourceTemplate
```


A template for parameterized resources on an MCP server.

See the [resource templates in the MCP specification](https://modelcontextprotocol.io/specification/2025-11-25/server/resources#resource-templates).

```python
uri_template: str
```

#### `from_mcp_sdk`

```python
def from_mcp_sdk(cls, mcp_template: mcp_types.ResourceTemplate) -> ResourceTemplate
```


Convert from MCP SDK ResourceTemplate to PydanticAI ResourceTemplate.

Args:
    mcp_template: The MCP SDK ResourceTemplate object.

### `ResourceLink`

```python
class ResourceLink
```


A resource link referenced in a prompt or tool call result.

Unlike [`EmbeddedResource`][pydantic_ai.mcp.EmbeddedResource], this does not include the resource
content directly — it is a reference to a resource that the server can read.

Note: resource links returned by tools are not guaranteed to appear in the results of
`resources/list` requests.

See the [MCP specification](https://modelcontextprotocol.io/specification/2025-11-25/server/resources).

```python
uri: str
```

```python
name: str
```

```python
title: str | None = None
```

```python
description: str | None = None
```

```python
mime_type: str | None = None
```

```python
size: int | None = None
```

```python
annotations: ResourceAnnotations | None = None
```

```python
icons: list[Icon] | None = None
```

```python
metadata: dict[str, Any] | None = None
```

```python
type: Literal['resource_link'] = 'resource_link'
```

#### `from_mcp_sdk`

```python
def from_mcp_sdk(cls, mcp_resource_link: mcp_types.ResourceLink) -> ResourceLink
```


Convert from MCP SDK ResourceLink to PydanticAI ResourceLink.

### `PromptArgument`

```python
class PromptArgument
```


An argument for a prompt template.

```python
name: str
```

```python
title: str | None = None
```

```python
description: str | None = None
```

```python
required: bool | None = None
```

### `Prompt`

```python
class Prompt
```


A prompt or prompt template that the server offers.

```python
name: str
```

```python
title: str | None = None
```

```python
description: str | None = None
```

```python
arguments: list[PromptArgument] | None = None
```

```python
icons: list[Icon] | None = None
```

```python
metadata: dict[str, Any] | None = None
```

#### `from_mcp_sdk`

```python
def from_mcp_sdk(cls, mcp_prompt: mcp_types.Prompt) -> Prompt
```


Convert from MCP SDK Prompt to PydanticAI Prompt.

Args:
    mcp_prompt: The MCP SDK Prompt object.

### `EmbeddedResource`

```python
class EmbeddedResource
```


A resource embedded into a prompt or tool call result.

Contains the actual resource content alongside its metadata, unlike
[`ResourceLink`][pydantic_ai.mcp.ResourceLink] which is only a reference.

See the [MCP specification](https://modelcontextprotocol.io/specification/2025-11-25/server/resources).

```python
uri: str
```

```python
content: str | messages.BinaryContent
```

```python
type: Literal['resource'] = 'resource'
```

```python
mime_type: str | None = None
```

```python
annotations: ResourceAnnotations | None = None
```

```python
metadata: dict[str, Any] | None = None
```

```python
resource_metadata: dict[str, Any] | None = None
```

#### `from_mcp_sdk`

```python
def from_mcp_sdk(cls, part: mcp_types.EmbeddedResource, content: str | messages.BinaryContent) -> EmbeddedResource
```


Convert from MCP SDK EmbeddedResource to PydanticAI EmbeddedResource.

### `PromptMessage`

```python
class PromptMessage
```


A message returned as part of a prompt result.

```python
role: PromptRole
```

```python
content: ContentBlock
```

### `PromptResult`

```python
class PromptResult
```


The result of a [`get_prompt`][pydantic_ai.mcp.MCPToolset.get_prompt] request.

```python
messages: list[PromptMessage]
```

```python
description: str | None = None
```

```python
metadata: dict[str, Any] | None = None
```

### `ServerCapabilities`

```python
class ServerCapabilities
```


Capabilities that an MCP server supports.

```python
experimental: list[str] | None = None
```

```python
logging: bool = False
```

```python
prompts: bool = False
```

```python
prompts_list_changed: bool = False
```

```python
resources: bool = False
```

```python
resources_list_changed: bool = False
```

```python
tools: bool = False
```

```python
tools_list_changed: bool = False
```

```python
completions: bool = False
```

#### `from_mcp_sdk`

```python
def from_mcp_sdk(cls, mcp_capabilities: mcp_types.ServerCapabilities) -> ServerCapabilities
```


Convert from MCP SDK ServerCapabilities to PydanticAI ServerCapabilities.

Args:
    mcp_capabilities: The MCP SDK ServerCapabilities object.

### `CallToolFunc`

```python
class CallToolFunc
```


A callable that invokes an MCP tool — typically `MCPToolset.direct_call_tool` or its legacy equivalent.

Passed to user-defined [`ProcessToolCallback`][pydantic_ai.mcp.ProcessToolCallback] functions as
the underlying call hook. `metadata` is keyword-only — pass it as
`await call_tool(name, args, metadata=...)`.

### `MCPToolset`

```python
class MCPToolset
```


A toolset for connecting to an MCP server.

`MCPToolset` is the recommended way to use [Model Context Protocol](https://modelcontextprotocol.io)
servers in Pydantic AI. It is built on the [FastMCP](https://gofastmcp.com) `Client`, which
supports the full MCP protocol — tools, resources, sampling, elicitation, OAuth — and a wide
range of transports (HTTP, SSE, stdio, in-process FastMCP servers, multi-server configs).

Pass any input that FastMCP can build a transport from — a URL, a script path, a `FastMCP`
server instance for in-process testing — or a pre-built `fastmcp.Client` for full control over
its configuration. For multi-server JSON config files, use
[`load_mcp_toolsets`][pydantic_ai.mcp.load_mcp_toolsets] instead.

Example — connect to a streamable-HTTP MCP server:

```python {test="skip"}
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPToolset

toolset = MCPToolset('http://localhost:8000/mcp')
agent = Agent('openai:gpt-5', toolsets=[toolset])
```

Example — connect to a local stdio MCP server:

```python {test="skip"}
from pydantic_ai.mcp import MCPToolset

toolset = MCPToolset('my_mcp_server.py')
```

Example — pass a pre-built FastMCP Client for full configuration control:

```python {test="skip"}
from fastmcp.client import Client
from fastmcp.client.transports import StreamableHttpTransport

from pydantic_ai.mcp import MCPToolset

client = Client(StreamableHttpTransport('http://localhost:8000/mcp'), auth='oauth')
toolset = MCPToolset(client)
```

```python
client: FastMCPClient[Any]
```

```python
tool_error_behavior: Literal['retry', 'error', 'failed']
```

```python
max_retries: int | None
```

```python
prefer_tasks: bool
```

```python
cache_tools: bool
```

```python
cache_resources: bool
```

```python
cache_prompts: bool
```

```python
include_instructions: bool
```

```python
include_return_schema: bool | None
```

```python
process_tool_call: ProcessToolCallback | None
```

```python
sampling_model: models.Model | None
```

```python
log_level: mcp_types.LoggingLevel | None
```

```python
_id: str | None
```

```python
_server_info: mcp_types.Implementation | None
```

```python
_server_capabilities: ServerCapabilities | None
```

```python
_instructions: str | None
```

```python
_cached_tools: list[mcp_types.Tool] | None
```

```python
_cached_resources: list[Resource] | None
```

```python
_cached_prompts: list[Prompt] | None
```

```python
_running_count: int
```

```python
_exit_stack: AsyncExitStack | None
```

```python
_user_message_handler: MessageHandlerT | None
```

```python
_call_tool_task: _CallToolTask | None
```

```python
_server_initiated_handlers: list[str]
```



#### `server_info`

```python
def server_info(self) -> mcp_types.Implementation
```


The server's implementation info, when the server provided it.

Raises [`AttributeError`][AttributeError] when accessed before the toolset has been entered,
or when a modern MCP session's server omitted the optional `serverInfo` stamp.

#### `capabilities`

```python
def capabilities(self) -> ServerCapabilities
```


The capabilities advertised by the server during initialization.

Raises [`AttributeError`][AttributeError] when accessed before the toolset has been entered.

#### `instructions`

```python
def instructions(self) -> str | None
```


The instructions sent by the server during initialization.

Raises [`AttributeError`][AttributeError] when accessed before the toolset has been entered.

#### `is_running`

```python
def is_running(self) -> bool
```


Whether the toolset is currently entered (the FastMCP session is open).

#### `set_sampling_model`

```python
def set_sampling_model(self, model: models.Model) -> None
```


Set the [`sampling_model`][pydantic_ai.mcp.MCPToolset.sampling_model] on an already-constructed toolset.

Swaps both the public attribute and the underlying FastMCP client's sampling callback.
Takes effect on the next session opened by the client; calls already in flight on an
existing session continue using the previously configured handler.

#### `get_instructions`

```python
async def get_instructions(self, ctx: RunContext[AgentDepsT]) -> messages.InstructionPart | None
```


Return the server's instructions if `include_instructions` is enabled.

#### `list_tools`

```python
async def list_tools(self) -> list[mcp_types.Tool]
```


Retrieve the tools currently exposed by the server.

When [`cache_tools`][pydantic_ai.mcp.MCPToolset.cache_tools] is enabled (default), results
are cached and invalidated by `notifications/tools/list_changed` or the toolset's last
`__aexit__`.

#### `tool_for_tool_def`

```python
def tool_for_tool_def(self, tool_def: ToolDefinition, *, ctx: RunContext[AgentDepsT]) -> ToolsetTool[AgentDepsT]
```


Build the tool to call for a tool definition that was already prepared elsewhere.

Args:
    tool_def: The prepared tool definition to build the tool from.
    ctx: The run context used to resolve the tool's retry budget.



#### `direct_call_tool`

```python
async def direct_call_tool(self, name: str, args: dict[str, Any], *, metadata: dict[str, Any] | None=None, use_task: bool=False) -> Any
```


Call a tool on the server directly.

Args:
    name: The name of the tool to call.
    args: The arguments to pass to the tool.
    metadata: Optional request-level `_meta` payload sent alongside the call.
    use_task: When `True`, ask the server to run the call as a durable, cancelable, pollable task.
        FastMCP 3 uses the MCP SEP-1686 `task=True` call path, while FastMCP 4 uses its tasks
        extension (SEP-2663). Only valid for tools that support task execution. Both paths wait for
        and return the completed tool result; on FastMCP 4, `use_task=True` explicitly selects the
        tasks extension even though an ordinary call can also drive a task-only tool to completion.

Raises:
    ModelRetry: If a completed tool error occurs with `tool_error_behavior='retry'` (the default), or
        if a protocol-level `McpError` occurs and `tool_error_behavior` is not `'error'`.
    fastmcp.exceptions.ToolError or the MCP SDK's McpError: If an error occurs and
        `tool_error_behavior='error'`.
    ToolFailed: If a completed tool error occurs and `tool_error_behavior='failed'`.
    UserError: If `use_task=True` and the FastMCP 4 client negotiated a legacy protocol
        session, which has no task path.
    ImportError: If `use_task=True` on FastMCP 4 and `fastmcp-tasks` is not installed.

#### `list_prompts`

```python
async def list_prompts(self) -> list[Prompt]
```


Retrieve the prompts currently exposed by the server.

When [`cache_prompts`][pydantic_ai.mcp.MCPToolset.cache_prompts] is enabled (default),
results are cached and invalidated by `notifications/prompts/list_changed` or the
toolset's last `__aexit__`.

Returns an empty list if the server does not advertise the `prompts` capability.

Raises:
    MCPError: If the server returns an error.

#### `get_prompt`

```python
async def get_prompt(self, name: str, arguments: dict[str, str] | None=None) -> PromptResult
```


Retrieve a specific prompt from the server, optionally parameterized.

Args:
    name: The name of the prompt to retrieve.
    arguments: Arguments to parameterize the prompt, if applicable.

Raises:
    MCPError: If the server doesn't advertise the `prompts` capability, or if it returns
        an error response.

#### `list_resources`

```python
async def list_resources(self) -> list[Resource]
```


Retrieve the resources currently exposed by the server.

When [`cache_resources`][pydantic_ai.mcp.MCPToolset.cache_resources] is enabled (default),
results are cached and invalidated by `notifications/resources/list_changed` or the
toolset's last `__aexit__`.

Returns an empty list if the server does not advertise the `resources` capability.

Raises:
    MCPError: If the server returns an error.

#### `list_resource_templates`

```python
async def list_resource_templates(self) -> list[ResourceTemplate]
```


Retrieve the resource templates currently exposed by the server.

Returns an empty list if the server does not advertise the `resources` capability.

Raises:
    MCPError: If the server returns an error.

#### `read_resource`

```python
async def read_resource(self, uri: str | Resource) -> str | messages.BinaryContent | list[str | messages.BinaryContent]
```


Read the contents of a specific resource by URI.

Args:
    uri: The URI of the resource to read, or a [`Resource`][pydantic_ai.mcp.Resource] object.

Returns:
    The resource contents — a single value if the resource has one content item, or a list
    otherwise. Text content is returned as `str`, binary content as
    [`BinaryContent`][pydantic_ai.messages.BinaryContent].

Raises:
    MCPError: If the server returns an error.















### `load_mcp_toolsets`

```python
def load_mcp_toolsets(config_path: str | Path) -> list[AbstractToolset[Any]]
```


Load `MCPToolset`s from a configuration file.

The configuration file uses the same `mcpServers` JSON shape as Claude Desktop, Claude Code,
and Cursor. Each server entry produces one [`MCPToolset`][pydantic_ai.mcp.MCPToolset], wrapped
in a [`PrefixedToolset`][pydantic_ai.toolsets.PrefixedToolset] using the server's name as prefix
to disambiguate tools across multiple servers.

Environment variables can be referenced in the configuration file using:

- `${VAR_NAME}` syntax — expands to the value of `VAR_NAME`, raises if not defined
- `${VAR_NAME:-default}` syntax — expands to `VAR_NAME` if set, otherwise the default

Args:
    config_path: Path to the JSON configuration file.

Returns:
    A list of toolsets, one per server in the config file, each prefixed with the server name.

Raises:
    OSError: If the configuration file does not exist (`FileNotFoundError`), or exists but
        cannot be read — a directory, or a file without read permission.
    ValidationError: If the configuration does not match the `mcpServers` shape above. This is
        a `ValueError` subclass, so catching `ValueError` covers it too.
    ValueError: If the file is not valid JSON, a server entry has neither `command` nor `url`,
        or an environment variable referenced in the configuration is not defined and no
        default is provided.