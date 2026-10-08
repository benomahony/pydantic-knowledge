# `pydantic_graph.step`

Step-based graph execution components.

This module provides the core abstractions for step-based graph execution,
including step contexts, step functions, and step nodes that bridge between
the declarative `BaseNode` API and the builder graph.

### `StepContext`

```python
class StepContext
```


Context information passed to step functions during graph execution.

The step context provides access to the current graph state, dependencies, and input data for a step.

Type Parameters:
    StateT: The type of the graph state
    DepsT: The type of the dependencies
    InputT: The type of the input data

```python
_state: StateT
```

```python
_deps: DepsT
```

```python
_inputs: InputT
```

#### `inputs`

```python
def inputs(self) -> InputT
```


The input data for this step.

This must be a property to ensure correct variance behavior

### `StepFunction`

```python
class StepFunction
```


Protocol for step functions that can be executed in the graph.

Step functions are async callables that receive a step context and return a result.

Type Parameters:
    StateT: The type of the graph state
    DepsT: The type of the dependencies
    InputT: The type of the input data
    OutputT: The type of the output data



### `StreamFunction`

```python
class StreamFunction
```


Protocol for stream functions that can be executed in the graph.

Stream functions are async callables that receive a step context and return an async iterator.

Type Parameters:
    StateT: The type of the graph state
    DepsT: The type of the dependencies
    InputT: The type of the input data
    OutputT: The type of the output data



### `Step`

```python
class Step
```


A step in the graph execution that wraps a step function.

Steps represent individual units of execution in the graph, encapsulating
a step function along with metadata like ID and label.

Type Parameters:
    StateT: The type of the graph state
    DepsT: The type of the dependencies
    InputT: The type of the input data
    OutputT: The type of the output data

```python
id: NodeID
```

```python
_call: StepFunction[StateT, DepsT, InputT, OutputT]
```

```python
label: str | None
```

#### `call`

```python
def call(self) -> StepFunction[StateT, DepsT, InputT, OutputT]
```


The step function to execute. This needs to be a property for proper variance inference.

#### `as_node`

```python
def as_node(self, inputs: InputT | None=None) -> StepNode[StateT, DepsT]
```


Create a step node with bound inputs.

Args:
    inputs: The input data to bind to this step, or None

Returns:
    A [`StepNode`][pydantic_graph.step.StepNode] with this step and the bound inputs

### `StepNode`

```python
class StepNode
```


A `BaseNode` that represents a builder step with bound inputs.

`StepNode` lets a [`BaseNode`][pydantic_graph.BaseNode] subclass hand off to a builder
[`Step`][pydantic_graph.step.Step] by wrapping the step together with the value it should
receive as `inputs`. It is not meant to be run directly; returning a `StepNode` from a
`BaseNode.run` method tells the graph builder which step to invoke next.

```python
step: Step[StateT, DepsT, Any, Any]
```

```python
inputs: Any
```

#### `run`

```python
async def run(self, ctx: GraphRunContext[StateT, DepsT]) -> BaseNode[StateT, DepsT, Any] | End[Any]
```


Attempt to run the step node.

Args:
    ctx: The graph execution context

Returns:
    The result of step execution

Raises:
    NotImplementedError: Always raised as StepNode is not meant to be run directly

### `NodeStep`

```python
class NodeStep
```


A step that wraps a `BaseNode` type for execution by the builder graph.

`NodeStep` lets a [`BaseNode`][pydantic_graph.BaseNode] subclass participate as a step in the
builder graph. It validates that the input is an instance of the expected node type and runs
it with the appropriate graph context.

```python
node_type: type[BaseNode[StateT, DepsT, Any]]
```



