# `pydantic_graph.join`

Join operations and reducers for graph execution.

This module provides the core components for joining parallel execution paths
in a graph, including various reducer types that aggregate data from multiple
sources into a single output.

### `JoinState`

```python
class JoinState
```


The state of a join during graph execution associated to a particular fork run.

```python
current: Any
```

```python
downstream_fork_stack: ForkStack
```

```python
cancelled_sibling_tasks: bool = False
```

### `ReducerContext`

```python
class ReducerContext
```


Context information passed to reducer functions during graph execution.

The reducer context provides access to the current graph state and dependencies.

Type Parameters:
    StateT: The type of the graph state
    DepsT: The type of the dependencies

```python
_state: StateT
```

```python
_deps: DepsT
```

```python
_join_state: JoinState
```

#### `state`

```python
def state(self) -> StateT
```


The state of the graph run.

#### `deps`

```python
def deps(self) -> DepsT
```


The deps for the graph run.

#### `cancel_sibling_tasks`

```python
def cancel_sibling_tasks(self)
```


Cancel all sibling tasks created from the same fork.

You can call this if you want your join to have early-stopping behavior.

### `reduce_null`

```python
def reduce_null(current: None, inputs: Any) -> None
```


A reducer that discards all input data and returns None.

### `reduce_list_append`

```python
def reduce_list_append(current: list[T], inputs: T) -> list[T]
```


A reducer that appends to a list.

### `reduce_list_extend`

```python
def reduce_list_extend(current: list[T], inputs: Iterable[T]) -> list[T]
```


A reducer that extends a list.

### `reduce_dict_update`

```python
def reduce_dict_update(current: dict[K, V], inputs: Mapping[K, V]) -> dict[K, V]
```


A reducer that updates a dict.

### `SupportsSum`

```python
class SupportsSum
```


A protocol for a type that supports adding to itself.

### `reduce_sum`

```python
def reduce_sum(current: NumericT, inputs: NumericT) -> NumericT
```


A reducer that sums numbers.

### `ReduceFirstValue`

```python
class ReduceFirstValue
```


A reducer that returns the first value it encounters, and cancels all other tasks.



### `Join`

```python
class Join
```


A join operation that synchronizes and aggregates parallel execution paths.

A join defines how to combine outputs from multiple parallel execution paths
using a [`ReducerFunction`][pydantic_graph.join.ReducerFunction]. It specifies which fork
it joins (if any) and manages the initialization of reducers.

Type Parameters:
    StateT: The type of the graph state
    DepsT: The type of the dependencies
    InputT: The type of input data to join
    OutputT: The type of the final joined output

```python
id: JoinID
```

```python
_reducer: ReducerFunction[StateT, DepsT, InputT, OutputT]
```

```python
_initial_factory: Callable[[], OutputT]
```

```python
parent_fork_id: ForkID | None
```

```python
preferred_parent_fork: Literal['closest', 'farthest']
```

#### `as_node`

```python
def as_node(self, inputs: InputT | None=None) -> JoinNode[StateT, DepsT]
```


Create a join node with bound inputs.

Args:
    inputs: The input data to bind to this join, or None

Returns:
    A [`JoinNode`][pydantic_graph.join.JoinNode] with this join and the bound inputs

### `JoinNode`

```python
class JoinNode
```


A `BaseNode` that represents a builder join with bound inputs.

`JoinNode` lets a [`BaseNode`][pydantic_graph.BaseNode] subclass hand off to a builder
[`Join`][pydantic_graph.join.Join] by wrapping the join together with the value it should
receive as `inputs`. It is not meant to be run directly; returning a `JoinNode` from a
`BaseNode.run` method tells the graph builder which join to invoke next.

```python
join: Join[StateT, DepsT, Any, Any]
```

```python
inputs: Any
```

#### `run`

```python
async def run(self, ctx: GraphRunContext[StateT, DepsT]) -> BaseNode[StateT, DepsT, Any] | End[Any]
```


Attempt to run the join node.

Args:
    ctx: The graph execution context

Returns:
    The result of step execution

Raises:
    NotImplementedError: Always raised as StepNode is not meant to be run directly