# `pydantic_ai.models.crusoe`

## Setup

For details on how to set up authentication with this model, see [model configuration for Crusoe](../../models/crusoe.md).

Crusoe model implementation using OpenAI-compatible API.

### `CrusoeModel`

```python
class CrusoeModel
```


A model that uses Crusoe's OpenAI-compatible Serverless Inference API.

Crusoe serves open-weight models from many labs behind one endpoint, so the model family — and with
it the profile [`CrusoeProvider`][pydantic_ai.providers.crusoe.CrusoeProvider] resolves — is derived
from the vendor prefix on the model name (`zai/`, `deepseek-ai/`, `meta-llama/`, …).

Every model is served with guided decoding, so [`NativeOutput`][pydantic_ai.output.NativeOutput] works
across the catalog, including for families whose own profiles don't claim native structured output
support. Thinking is returned in a non-standard field (`reasoning`, or `reasoning_content` for
DeepSeek), both of which `OpenAIChatModel` reads.

Apart from `__init__`, all methods are inherited from the base class.

