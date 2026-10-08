# `pydantic_ai.models.system_one`

## Setup

For details on how to connect to a decision model over the `/v1/systemone` API, see [model configuration for the System One API](../../models/system-one.md).

### `SystemOneModelSettings`

```python
class SystemOneModelSettings
```


Settings used for a System One API request.

### `SystemOneModel`

```python
class SystemOneModel
```


The model class for [decision models][pydantic_ai.models.decision.DecisionModel] served over the `/v1/systemone` API.

Decision models such as [Contrastive Language Models](https://huggingface.co/Contrastive-LM/CLM-v0.1-8B) and
[Laya](https://huggingface.co/convaiinnovations/laya) are available over this API, and an agent whose job is to
decide something runs on one like on any other model, with the `output_type` as the questions:

```python
from pydantic import BaseModel, Field

from pydantic_ai import Agent


class Handling(BaseModel):
    irreversible: bool = Field(description='Would running this destroy data or leak secrets?')


agent = Agent('system-one:clm-latest', output_type=Handling)
...
```

See [Decision models](https://pydantic.dev/docs/ai/models/decision/) for how an agent's output type and tools
become questions, and [System One API](https://pydantic.dev/docs/ai/models/system-one/) for connecting to one.

Apart from `__init__`, all methods are private or match those of the base class.

```python
_model_name: SystemOneModelName = field(repr=False)
```

```python
_provider: Provider[httpx2.AsyncClient] = field(repr=False)
```

```python
_api_key: str | None = field(repr=False)
```



#### `model_name`

```python
def model_name(self) -> SystemOneModelName
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


Send one request to the `/v1/systemone` endpoint.

