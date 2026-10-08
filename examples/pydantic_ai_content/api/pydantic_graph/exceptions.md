# `pydantic_graph.exceptions`

### `GraphSetupError`

```python
class GraphSetupError
```


Error caused by an incorrectly configured graph.

```python
message: str
```

### `GraphBuildingError`

```python
class GraphBuildingError
```


An error raised during graph-building.

```python
message: str
```

### `GraphValidationError`

```python
class GraphValidationError
```


An error raised during graph validation.

```python
message: str
```

### `GraphRuntimeError`

```python
class GraphRuntimeError
```


Error caused by an issue during graph execution.

```python
message: str
```

### `UnsupportedEventLoopError`

```python
class UnsupportedEventLoopError
```


Error caused by calling a synchronous method on an event loop that cannot be driven by the caller.

Synchronous methods run their asynchronous implementation using `loop.run_until_complete()`, which not every
event loop implements. Temporal's workflow event loop is one that doesn't: it can only be driven by Temporal.

Pydantic AI's synchronous methods report this as a `pydantic_ai.exceptions.UserError` instead.

```python
message: str
```