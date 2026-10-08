# `pydantic_ai.models.cohere`

## Setup

For details on how to set up authentication with this model, see [model configuration for Cohere](../../models/cohere.md).

### `CohereModelSettings`

```python
class CohereModelSettings
```


Settings used for a Cohere model request.

### `CohereModel`

```python
class CohereModel
```


A model that uses the Cohere API.

Internally, this uses the [Cohere Python client](
https://github.com/cohere-ai/cohere-python) to interact with the API.

Apart from `__init__`, all methods are private or match those of the base class.

```python
_model_name: CohereModelName = field(repr=False)
```

```python
_provider: Provider[AsyncClientV2] = field(repr=False)
```



#### `model_name`

```python
def model_name(self) -> CohereModelName
```


The model name.

#### `system`

```python
def system(self) -> str
```


The model provider.





