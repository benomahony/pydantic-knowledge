# `pydantic_ai.models.openai_codex`

## Setup

For details on how to set up authentication with this model, see [model configuration for OpenAI Codex](../../models/openai-codex.md).

### `OpenAICodexModel`

```python
class OpenAICodexModel
```


A model that uses the OpenAI Codex backend under a ChatGPT/Codex subscription.

This model mirrors the official Codex client's prompt-cache affinity by sending the `session-id`,
`thread-id`, and `x-client-request-id` headers and the `prompt_cache_key` field, all derived from the
`conversation_id` of the message history. Explicit `extra_headers` and `openai_prompt_cache_key` settings win.

Apart from `__init__`, all methods are private or match those of the base class.

