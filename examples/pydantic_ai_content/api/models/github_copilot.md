# `pydantic_ai.models.github_copilot`

## Setup

For details on how to set up authentication with this model, see [model configuration for GitHub Copilot](../../models/github-copilot.md).

GitHub Copilot model implementation using OpenAI-compatible API.

### `GitHubCopilotModel`

```python
class GitHubCopilotModel
```


A model that uses GitHub Copilot's OpenAI-compatible Chat Completions API.

Copilot serves Anthropic, OpenAI, Google, xAI and MoonshotAI models behind one endpoint, so the
model family — and with it the profile
[`GitHubCopilotProvider`][pydantic_ai.providers.github_copilot.GitHubCopilotProvider] resolves —
is derived from the prefix of the bare model id (`claude-`, `gpt-`, `gemini-`, …). Ids go out on
the wire exactly as given.

Apart from `__init__`, all methods are private or match those of the base class.

