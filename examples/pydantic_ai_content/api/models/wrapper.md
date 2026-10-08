# pydantic_ai.models.wrapper

### `WrapperModel`

```python
class WrapperModel
```


Model which wraps another model.

Does nothing on its own, used as a base class.

```python
wrapped: Model
```

#### `settings`

```python
def settings(self) -> ModelSettings | None
```


Get the settings from the wrapped model.