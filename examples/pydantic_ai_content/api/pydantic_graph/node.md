# `pydantic_graph.node`

Core node types for graph construction and execution.

This module defines the fundamental node types used to build execution graphs,
including start/end nodes and fork nodes for parallel execution.

### `StartNode`

```python
class StartNode
```


Entry point node for graph execution.

The StartNode represents the beginning of a graph execution flow.

### `EndNode`

```python
class EndNode
```


Terminal node representing the completion of graph execution.

The EndNode marks the successful completion of a graph execution flow
and can collect the final output data.



### `Fork`

```python
class Fork
```


Fork node that creates parallel execution branches.

A Fork node splits the execution flow into multiple parallel branches,
enabling concurrent execution of downstream nodes. It can either map
a sequence across multiple branches or duplicate data to each branch.

```python
id: ForkID
```

```python
is_map: bool
```

```python
downstream_join_id: JoinID | None
```

