# `pydantic_ai.models.typesafe`

## Setup

For details on how to set up authentication with this model, see [model configuration for TypeSafe](../../models/typesafe.md).

### `TypeSafeModelSettings`

```python
class TypeSafeModelSettings
```


Settings used for a TypeSafe model request.

```python
typesafe_boolean_threshold: float
```

```python
typesafe_tool_call_threshold: float
```

### `TypeSafeModel`

```python
class TypeSafeModel
```


The model class for TypeSafe's Jev, a [decision model][pydantic_ai.models.decision.DecisionModel].

Jev answers typed questions about a text, each with a confidence, rather than writing text. An agent whose job is
to decide something runs on it like on any other model, with the `output_type` as the questions:

```python
from typing import Literal

from pydantic import BaseModel, Field

from pydantic_ai import Agent


class Handling(BaseModel):
    verdict: Literal['run', 'reject', 'ask'] = Field(description='How to handle this command.')
    irreversible: bool = Field(description='Would running this destroy data or leak secrets?')


agent = Agent('typesafe:jev-latest', output_type=Handling)
...
```

See [Decision models](https://pydantic.dev/docs/ai/models/decision/) for how an agent's output type and tools
become questions, and [TypeSafe (Jev)](https://pydantic.dev/docs/ai/models/typesafe/) for setup, Jev's limits,
and what it answers badly.

Apart from `__init__`, all methods are private or match those of the base class.

```python
max_choice_options: ClassVar[int | None] = _JEV_MAX_CHOICE_OPTIONS
```

```python
max_score_levels: ClassVar[int | None] = _JEV_MAX_SCORE_LEVELS
```

```python
_model_name: TypeSafeModelName = field(repr=False)
```

```python
_provider: Provider[AsyncTypeSafeClient] = field(repr=False)
```



#### `model_name`

```python
def model_name(self) -> TypeSafeModelName
```


The model name.

#### `system`

```python
def system(self) -> str
```


The system / model provider.

#### `decide`

```python
async def decide(self, request: DecisionRequest, model_settings: DecisionModelSettings) -> DecisionResponse
```


Send one request to TypeSafe's Decisions API.