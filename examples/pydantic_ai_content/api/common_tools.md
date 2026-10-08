# `pydantic_ai.common_tools`

### `DuckDuckGoResult`

```python
class DuckDuckGoResult
```


A DuckDuckGo search result.

```python
title: str
```

```python
href: str
```

```python
body: str
```

### `DuckDuckGoSearchTool`

```python
class DuckDuckGoSearchTool
```


The DuckDuckGo search tool.

```python
client: DDGS
```

```python
_: KW_ONLY
```

```python
max_results: int | None
```



### `duckduckgo_search_tool`

```python
def duckduckgo_search_tool(duckduckgo_client: DDGS | None=None, max_results: int | None=None)
```


Creates a DuckDuckGo search tool.

Args:
    duckduckgo_client: The DuckDuckGo search client.
    max_results: The maximum number of results. If None, returns results only from the first response.Exa tools for Pydantic AI agents.

Provides web search, content retrieval, and AI-powered answer capabilities
using the Exa API, a neural search engine that finds high-quality, relevant
results across billions of web pages.

These tools are deprecated and will be removed in v3. Use the `ExaSearch` capability from the
[Pydantic AI Harness](https://pydantic.dev/docs/ai/harness/exa-search/) instead.

### `ExaSearchResult`

```python
class ExaSearchResult
```


An Exa search result with content.

See [Exa Search API documentation](https://docs.exa.ai/reference/search)
for more information.

```python
title: str
```

```python
url: str
```

```python
published_date: str | None
```

```python
author: str | None
```

```python
text: str
```

### `ExaAnswerResult`

```python
class ExaAnswerResult
```


An Exa answer result with citations.

See [Exa Answer API documentation](https://docs.exa.ai/reference/answer)
for more information.

```python
answer: str
```

```python
citations: list[dict[str, Any]]
```

### `ExaContentResult`

```python
class ExaContentResult
```


Content retrieved from a URL.

See [Exa Contents API documentation](https://docs.exa.ai/reference/get-contents)
for more information.

```python
url: str
```

```python
title: str
```

```python
text: str
```

```python
author: str | None
```

```python
published_date: str | None
```

### `ExaSearchTool`

```python
class ExaSearchTool
```


The Exa search tool.

```python
client: AsyncExa
```

```python
num_results: int
```

```python
max_characters: int | None
```



### `ExaFindSimilarTool`

```python
class ExaFindSimilarTool
```


The Exa find similar tool.

```python
client: AsyncExa
```

```python
num_results: int
```



### `ExaGetContentsTool`

```python
class ExaGetContentsTool
```


The Exa get contents tool.

```python
client: AsyncExa
```



### `ExaAnswerTool`

```python
class ExaAnswerTool
```


The Exa answer tool.

```python
client: AsyncExa
```



### `exa_search_tool`

```python
def exa_search_tool(api_key: str | None=None, *, client: AsyncExa | None=None, num_results: int=5, max_characters: int | None=None) -> Tool[Any]
```


Creates an Exa search tool.

Args:
    api_key: The Exa API key. Required if `client` is not provided.

        You can get one by signing up at [https://dashboard.exa.ai](https://dashboard.exa.ai).
    client: An existing AsyncExa client. If provided, `api_key` is ignored.
        This is useful for sharing a client across multiple tools.
    num_results: The number of results to return. Defaults to 5.
    max_characters: Maximum characters of text content per result. Use this to limit
        token usage. Defaults to None (no limit).

### `exa_find_similar_tool`

```python
def exa_find_similar_tool(api_key: str | None=None, *, client: AsyncExa | None=None, num_results: int=5) -> Tool[Any]
```


Creates an Exa find similar tool.

Args:
    api_key: The Exa API key. Required if `client` is not provided.

        You can get one by signing up at [https://dashboard.exa.ai](https://dashboard.exa.ai).
    client: An existing AsyncExa client. If provided, `api_key` is ignored.
        This is useful for sharing a client across multiple tools.
    num_results: The number of similar results to return. Defaults to 5.

### `exa_get_contents_tool`

```python
def exa_get_contents_tool(api_key: str | None=None, *, client: AsyncExa | None=None) -> Tool[Any]
```


Creates an Exa get contents tool.

Args:
    api_key: The Exa API key. Required if `client` is not provided.

        You can get one by signing up at [https://dashboard.exa.ai](https://dashboard.exa.ai).
    client: An existing AsyncExa client. If provided, `api_key` is ignored.
        This is useful for sharing a client across multiple tools.

### `exa_answer_tool`

```python
def exa_answer_tool(api_key: str | None=None, *, client: AsyncExa | None=None) -> Tool[Any]
```


Creates an Exa answer tool.

Args:
    api_key: The Exa API key. Required if `client` is not provided.

        You can get one by signing up at [https://dashboard.exa.ai](https://dashboard.exa.ai).
    client: An existing AsyncExa client. If provided, `api_key` is ignored.
        This is useful for sharing a client across multiple tools.

### `ExaToolset`

```python
class ExaToolset
```


A toolset that provides Exa search tools with a shared client.

Deprecated in favor of the [`ExaSearch`](https://pydantic.dev/docs/ai/harness/exa-search/)
capability in the Pydantic AI Harness:

```python {test="skip"}
from pydantic_ai_harness.exa import ExaSearch

from pydantic_ai import Agent

agent = Agent('openai:gpt-5.2', capabilities=[ExaSearch()])
```



### `ImageGenerationSubagentTool`

```python
class ImageGenerationSubagentTool
```


Local image generation tool that delegates to a subagent.

Uses a subagent with the specified model and native tool configuration
to generate images when the outer agent's model doesn't support image
generation natively.

```python
model: Model | KnownModelName | str | ImageGenerationFallbackModelFunc
```

```python
native_tool: ImageGenerationNativeTool[Any]
```

```python
instructions: str = 'Generate an image based on the user prompt. Do not ask clarifying questions.'
```



### `image_generation_tool`

```python
def image_generation_tool(model: Model | KnownModelName | str | ImageGenerationFallbackModelFunc, native_tool: ImageGenerationNativeTool[Any], *, instructions: str='Generate an image based on the user prompt. Do not ask clarifying questions.') -> Tool[Any]
```


Creates an image generation tool backed by a subagent.

Args:
    model: The model to use for image generation (e.g. `'openai-responses:gpt-5.4'`),
        or a callable taking `RunContext` that returns a model.
    native_tool: The image generation configuration, or a callable that resolves it from the outer run context.
    instructions: Instructions for the subagent that generates the image.### `TavilySearchResult`

```python
class TavilySearchResult
```


A Tavily search result.

See [Tavily Search Endpoint documentation](https://docs.tavily.com/api-reference/endpoint/search)
for more information.

```python
title: str
```

```python
url: str
```

```python
content: str
```

```python
score: float
```

### `TavilySearchTool`

```python
class TavilySearchTool
```


The Tavily search tool.

```python
client: AsyncTavilyClient
```

```python
_: KW_ONLY
```

```python
max_results: int | None = None
```



### `tavily_search_tool`

```python
def tavily_search_tool(api_key: str | None=None, *, client: AsyncTavilyClient | None=None, max_results: int | None=None, search_depth: Literal['basic', 'advanced', 'fast', 'ultra-fast']=_UNSET, topic: Literal['general', 'news', 'finance']=_UNSET, time_range: Literal['day', 'week', 'month', 'year'] | None=_UNSET, include_domains: list[str] | None=_UNSET, exclude_domains: list[str] | None=_UNSET) -> Tool[Any]
```


Creates a Tavily search tool.

`max_results` is always developer-controlled and does not appear in the LLM tool schema.
Other parameters, when provided, are fixed for all searches and hidden from the LLM's
tool schema. Parameters left unset remain available for the LLM to set per-call.

Args:
    api_key: The Tavily API key. Required if `client` is not provided.

        You can get one by signing up at [https://app.tavily.com/home](https://app.tavily.com/home).
    client: An existing AsyncTavilyClient. If provided, `api_key` is ignored.
        This is useful for sharing a client across multiple tool instances.
    max_results: The maximum number of results. If None, the Tavily default is used.
    search_depth: The depth of the search.
    topic: The category of the search.
    time_range: The time range back from the current date to filter results.
    include_domains: List of domains to specifically include in the search results.
    exclude_domains: List of domains to specifically exclude from the search results.Web fetch tool for Pydantic AI agents.

Fetches web pages and converts their content to markdown using SSRF-protected
HTTP requests and the `markdownify` library for HTML-to-markdown conversion.

### `WebFetchResult`

```python
class WebFetchResult
```


Result of fetching a web page.

```python
url: str
```

```python
title: str
```

```python
content: str
```

### `WebFetchLocalTool`

```python
class WebFetchLocalTool
```


Fetches a URL and converts the response to markdown.

```python
_: KW_ONLY
```

```python
max_content_length: int | None
```

```python
allow_local_urls: bool
```

```python
timeout: int
```

```python
max_download_bytes: int | None = field(default=_MAX_DOWNLOAD_BYTES)
```

```python
allowed_domains: list[str] | None = field(default=None)
```

```python
blocked_domains: list[str] | None = field(default=None)
```

```python
headers: dict[str, str] | None = field(default=None)
```















### `web_fetch_tool`

```python
def web_fetch_tool(*, max_content_length: int | None=50000, allow_local_urls: bool=False, timeout: int=30, max_download_bytes: int | None=_MAX_DOWNLOAD_BYTES, allowed_domains: list[str] | None=None, blocked_domains: list[str] | None=None, headers: dict[str, str] | None=None) -> Tool[Any]
```


Creates a web fetch tool that fetches URLs and converts content to markdown.

This tool uses SSRF protection via `pydantic_ai._ssrf.safe_download`.

By default, sends `Accept: text/markdown` to request markdown directly from
servers that support it (e.g. Cloudflare, Vercel, Mintlify). This reduces
token usage and improves content quality. Falls back to HTML-to-markdown
conversion when the server doesn't support markdown responses.

Args:
    max_content_length: Maximum character length of returned content.
        Defaults to 50,000 (~12,500 tokens). Use `None` for no limit.
    allow_local_urls: Whether to allow fetching from private/local IP addresses.
        Defaults to `False`.
    timeout: Request timeout in seconds. Defaults to 30.
    max_download_bytes: Maximum size in bytes of the response body to download, applied
        before the body is buffered. Defaults to 50 MiB. Use `None` for no limit, which
        lets a response of any size be read into memory.
    allowed_domains: Only fetch from these domains (exact hostname match, ignoring case and a
        trailing dot). Raises `ModelRetry` on violation.
    blocked_domains: Never fetch from these domains (exact hostname match, ignoring case and a
        trailing dot). Raises `ModelRetry` on violation.
    headers: Additional HTTP headers to include in requests.
        Overrides the default `Accept: text/markdown` header if `Accept` is provided.
        The URL is controlled by the model, so a credential configured here (e.g.
        `Authorization`) can be sent to any URL the model requests that passes the
        domain filters, which match the hostname only, not scheme or port. On
        redirects, configured sensitive headers (`Authorization`, `Cookie`,
        `Proxy-Authorization`) are only forwarded to the same origin (scheme,
        host, and port) or a same-host http→https upgrade on the default ports.### `XSearchSubagentTool`

```python
class XSearchSubagentTool
```


Local X search tool that delegates to a subagent.

Uses a subagent with the specified xAI model and `XSearchTool` native tool
to search X/Twitter when the outer agent's model doesn't support
X search natively.

```python
model: Model | KnownModelName | str | XSearchFallbackModelFunc
```

```python
native_tool: XSearchNativeTool[Any]
```

```python
instructions: str = 'Search X/Twitter based on the user query. Return a comprehensive summary of the results.'
```



### `x_search_tool`

```python
def x_search_tool(model: Model | KnownModelName | str | XSearchFallbackModelFunc, native_tool: XSearchNativeTool[Any], *, instructions: str='Search X/Twitter based on the user query. Return a comprehensive summary of the results.') -> Tool[Any]
```


Creates an X search tool backed by a subagent.

Args:
    model: The model to use for X search. Must be an xAI model that natively
        supports the `XSearchTool` native tool, e.g. `'xai:grok-4.3'`.
        Can also be a callable taking `RunContext` that returns such a model.
    native_tool: The X search tool configuration, or a callable that resolves it from the outer run context.
    instructions: Instructions for the subagent that performs the X search.