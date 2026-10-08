# `pydantic_ai.models.zai`

## Setup

For details on how to set up authentication with this model, see [model configuration for Z.AI](../../models/zai.md).

Z.AI (Zhipu AI) model implementation using OpenAI-compatible API.





### `ZaiModelSettings`

```python
class ZaiModelSettings
```


Settings used for a Z.AI model request.

ALL FIELDS MUST BE `zai_` PREFIXED SO YOU CAN MERGE THEM WITH OTHER MODELS.

```python
zai_clear_thinking: bool
```

### `ZaiModel`

```python
class ZaiModel
```


A model that uses Z.AI's OpenAI-compatible API.

Z.AI (Zhipu AI) provides GLM models with support for thinking/reasoning mode
and preserved thinking across turns.

Apart from `__init__`, all methods are private or match those of the base class.



### `ZaiStreamedResponse`

```python
class ZaiStreamedResponse
```


Implementation of `StreamedResponse` for Z.AI models.

Streamed chunks need no widened type: the openai SDK builds them leniently, so Z.AI's
non-standard `finish_reason` reaches us as-is and only the mapping below has to know about it.

