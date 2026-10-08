# `pydantic_graph.basenode`

### `GraphRunContext`

```python
class GraphRunContext
```


Context for a graph.

```python
state: StateT
```

```python
deps: DepsT
```

### `BaseNode`

```python
class BaseNode
```


Base class for a node.

#### `run`

```python
async def run(self, ctx: GraphRunContext[StateT, DepsT]) -> BaseNode[StateT, DepsT, Any] | End[NodeRunEndT]
```


Run the node.

This is an abstract method that must be implemented by subclasses.

!!! note "Return types used at runtime"
    The return type of this method are read by `pydantic_graph` at runtime and used to define which
    nodes can be called next in the graph, and enforced when running the graph.

Args:
    ctx: The graph context.

Returns:
    The next node to run or [`End`][pydantic_graph.basenode.End] to signal the end of the graph.

#### `get_node_id`

```python
def get_node_id(cls) -> str
```


Get the ID of the node.

### `End`

```python
class End
```


Type to return from a node to signal the end of the graph.

```python
data: RunEndT
```

### `Edge`

```python
class Edge
```


Annotation to apply a label to an edge in a graph.

```python
label: str | None
```