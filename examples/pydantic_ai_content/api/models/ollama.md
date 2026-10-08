# `pydantic_ai.models.ollama`

## Setup

For details on how to set up authentication with this model, see [model configuration for Ollama](../../models/ollama.md).

Ollama model implementation using OpenAI-compatible API.



### `OllamaModel`

```python
class OllamaModel
```


A model that uses Ollama's OpenAI-compatible Chat Completions API.

Self-hosted Ollama (v0.5.0+) honors `response_format` with `json_schema` via
`llama.cpp`'s grammar-constrained decoder, so `NativeOutput` produces
schema-valid output at generation time.

Ollama Cloud currently accepts `response_format` with `json_schema` without
error but does not enforce the schema upstream (see
[pydantic-ai#4917](https://github.com/pydantic/pydantic-ai/issues/4917) and
[ollama/ollama#12362](https://github.com/ollama/ollama/issues/12362)). When
this model detects a Cloud path — either a `base_url` on `ollama.com` or a
model name ending in `-cloud` — it disables `supports_json_schema_output`
on the resolved profile. With that flag off,
[`NativeOutput`][pydantic_ai.output.NativeOutput] raises a clear
[`UserError`][pydantic_ai.exceptions.UserError] so users pick a mode that
actually works on Cloud ([`ToolOutput`][pydantic_ai.output.ToolOutput] —
the default — and [`PromptedOutput`][pydantic_ai.output.PromptedOutput] are
both verified to work).

Apart from `__init__`, all methods are inherited from the base class.

