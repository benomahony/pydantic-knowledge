# `pydantic_ai.models.cerebras`

## Setup

For details on how to set up authentication with this model, see [model configuration for Cerebras](../../models/cerebras.md).

Cerebras model implementation using OpenAI-compatible API.

### `CerebrasModelSettings`

```python
class CerebrasModelSettings
```


Settings used for a Cerebras model request.

ALL FIELDS MUST BE `cerebras_` PREFIXED SO YOU CAN MERGE THEM WITH OTHER MODELS.

```python
cerebras_disable_reasoning: bool
```

```python
cerebras_clear_thinking: bool
```

### `CerebrasModel`

```python
class CerebrasModel
```


A model that uses Cerebras's OpenAI-compatible API.

Cerebras provides ultra-fast inference powered by the Wafer-Scale Engine (WSE).

Apart from `__init__`, all methods are private or match those of the base class.





