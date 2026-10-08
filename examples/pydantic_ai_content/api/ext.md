# `pydantic_ai.ext`

### `tool_from_langchain`

```python
def tool_from_langchain(langchain_tool: LangChainTool) -> Tool
```


Creates a Pydantic AI tool proxy from a LangChain tool.

Args:
    langchain_tool: The LangChain tool to wrap.

Returns:
    A Pydantic AI tool that corresponds to the LangChain tool.

### `LangChainToolset`

```python
class LangChainToolset
```


A toolset that wraps LangChain tools.