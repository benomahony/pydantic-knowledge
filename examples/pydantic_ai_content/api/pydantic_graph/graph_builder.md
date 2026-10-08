# `pydantic_graph.graph_builder`

Builder-based graph API: builder, graph runner, and mermaid rendering.

This module is the canonical home for the builder-based graph API:
[`GraphBuilder`][pydantic_graph.GraphBuilder] for declaratively constructing
executable graphs, [`Graph`][pydantic_graph.Graph] and
[`GraphRun`][pydantic_graph.GraphRun] for executing them, and the mermaid
rendering helpers used by `Graph.render()`. The same public symbols are
re-exported from `pydantic_graph` directly.

### `EndMarker`

```python
class EndMarker
```


A marker indicating the end of graph execution with a final value.

EndMarker is used internally to signal that the graph has completed
execution and carries the final output value.

Type Parameters:
    OutputT: The type of the final output value

```python
_value: OutputT
```

### `ErrorMarker`

```python
class ErrorMarker
```


A marker indicating that a graph node raised an exception.

Yielded by the graph iterator instead of raising immediately, allowing the caller
to recover by sending new tasks via `GraphRun.next()` or `GraphRun.override_next()`.
If the caller does not override, the error is re-raised on the next iteration.

```python
error: BaseException
```

### `JoinItem`

```python
class JoinItem
```


An item representing data flowing into a join operation.

JoinItem carries input data from a parallel execution path to a join
node, along with metadata about which execution 'fork' it originated from.

```python
join_id: JoinID
```

```python
inputs: Any
```

```python
fork_stack: ForkStack
```

### `Graph`

```python
class Graph
```


A complete graph definition ready for execution.

The Graph class represents a complete workflow graph with typed inputs,
outputs, state, and dependencies. It contains all nodes, edges, and
metadata needed for execution.

Type Parameters:
    StateT: The type of the graph state
    DepsT: The type of the dependencies
    InputT: The type of the input data
    OutputT: The type of the output data

```python
name: str | None
```

```python
state_type: type[StateT]
```

```python
deps_type: type[DepsT]
```

```python
input_type: type[InputT]
```

```python
output_type: type[OutputT]
```

```python
auto_instrument: bool
```

```python
nodes: dict[NodeID, AnyNode]
```

```python
edges_by_source: dict[NodeID, list[Path]]
```

```python
parent_forks: dict[JoinID, ParentFork[NodeID]]
```

```python
intermediate_join_nodes: dict[JoinID, set[JoinID]]
```

#### `get_parent_fork`

```python
def get_parent_fork(self, join_id: JoinID) -> ParentFork[NodeID]
```


Get the parent fork information for a join node.

Args:
    join_id: The ID of the join node

Returns:
    The parent fork information for the join

Raises:
    RuntimeError: If the join ID is not found or has no parent fork

#### `is_final_join`

```python
def is_final_join(self, join_id: JoinID) -> bool
```


Check if a join is 'final' (has no downstream joins with the same parent fork).

A join is non-final if it appears as an intermediate node for another join
with the same parent fork.

Args:
    join_id: The ID of the join node

Returns:
    True if the join is final, False if it's non-final

#### `run`

```python
async def run(self, *, state: StateT=None, deps: DepsT=None, inputs: InputT=None, span: AbstractContextManager[AbstractSpan] | None=None, infer_name: bool=True) -> OutputT
```


Execute the graph and return the final output.

This is the main entry point for graph execution. It runs the graph
to completion and returns the final output value.

Args:
    state: The graph state instance
    deps: The dependencies instance
    inputs: The input data for the graph
    span: Optional span for tracing/instrumentation
    infer_name: Whether to infer the graph name from the calling frame.

Returns:
    The final output from the graph execution

#### `run_sync`

```python
def run_sync(self, *, state: StateT=None, deps: DepsT=None, inputs: InputT=None, span: AbstractContextManager[AbstractSpan] | None=None, infer_name: bool=True) -> OutputT
```


Synchronously execute the graph and return the final output.

This is a convenience wrapper around [`run`][pydantic_graph.graph_builder.Graph.run] that runs the coroutine on the
current event loop via `loop.run_until_complete(...)`. As such, it cannot be called from inside async
code or when an event loop is already running.

Args:
    state: The graph state instance
    deps: The dependencies instance
    inputs: The input data for the graph
    span: Optional span for tracing/instrumentation
    infer_name: Whether to infer the graph name from the calling frame.

Returns:
    The final output from the graph execution

#### `iter`

```python
async def iter(self, *, state: StateT=None, deps: DepsT=None, inputs: InputT=None, span: AbstractContextManager[AbstractSpan] | None=None, infer_name: bool=True) -> AsyncGenerator[GraphRun[StateT, DepsT, OutputT]]
```


Create an iterator for step-by-step graph execution.

This method allows for more fine-grained control over graph execution,
enabling inspection of intermediate states and results.

Args:
    state: The graph state instance
    deps: The dependencies instance
    inputs: The input data for the graph
    span: Optional span for tracing/instrumentation
    infer_name: Whether to infer the graph name from the calling frame.

Yields:
    A GraphRun instance that can be iterated for step-by-step execution

#### `render`

```python
def render(self, *, title: str | None=None, direction: StateDiagramDirection | None=None) -> str
```


Render the graph as a Mermaid diagram string.

Args:
    title: Optional title for the diagram
    direction: Optional direction for the diagram layout

Returns:
    A string containing the Mermaid diagram representation



### `GraphTaskRequest`

```python
class GraphTaskRequest
```


A request to run a task representing the execution of a node in the graph.

GraphTaskRequest encapsulates all the information needed to execute a specific
node, including its inputs and the fork context it's executing within.

```python
node_id: NodeID
```

```python
inputs: Any
```

```python
fork_stack: ForkStack = field(repr=False)
```

### `GraphTask`

```python
class GraphTask
```


A task representing the execution of a node in the graph.

GraphTask encapsulates all the information needed to execute a specific
node, including its inputs and the fork context it's executing within,
and has a unique ID to identify the task within the graph run.

```python
task_id: TaskID = field(repr=False)
```

### `GraphRun`

```python
class GraphRun
```


A single execution instance of a graph.

GraphRun manages the execution state for a single run of a graph,
including task scheduling, fork/join coordination, and result tracking.

Type Parameters:
    StateT: The type of the graph state
    DepsT: The type of the dependencies
    OutputT: The type of the output data









#### `next`

```python
async def next(self, value: EndMarker[OutputT] | Sequence[GraphTaskRequest] | None=None) -> EndMarker[OutputT] | Sequence[GraphTask]
```


Advance the graph execution by one step.

This method allows for sending a value to the iterator, which is useful
for resuming iteration or overriding intermediate results.

Args:
    value: Optional value to send to the iterator

Returns:
    The next execution result: either an EndMarker, or sequence of GraphTasks

#### `override_next`

```python
def override_next(self, value: Sequence[GraphTaskRequest] | EndMarker[OutputT]) -> None
```


Override the next pending step, allowing the graph to continue after an `End` or error.

This is used by hook systems (like `after_node_run` or `on_node_run_error`) to redirect
the graph to a new node when the current step produced an `End` result or raised an error,
or to signal early completion by passing an `EndMarker`.

Must only be called between iterations (not while an iteration is in flight).

Args:
    value: New task requests to execute next, or an `EndMarker` to signal completion.

#### `next_task`

```python
def next_task(self) -> EndMarker[OutputT] | ErrorMarker | Sequence[GraphTask]
```


Get the next task(s) to be executed.

Returns:
    The next execution item, or the initial task if none is set

#### `output`

```python
def output(self) -> OutputT | None
```


Get the final output if the graph has completed.

Returns:
    The output value if execution is complete, None otherwise

### `GraphBuilder`

```python
class GraphBuilder
```


A builder for constructing executable graph definitions.

GraphBuilder provides a fluent interface for defining nodes, edges, and
routing in a graph workflow. It supports typed state, dependencies, and
input/output validation.

Type Parameters:
    StateT: The type of the graph state
    DepsT: The type of the dependencies
    GraphInputT: The type of the graph input data
    GraphOutputT: The type of the graph output data

```python
name: str | None
```

```python
state_type: TypeOrTypeExpression[StateT]
```

```python
deps_type: TypeOrTypeExpression[DepsT]
```

```python
input_type: TypeOrTypeExpression[GraphInputT]
```

```python
output_type: TypeOrTypeExpression[GraphOutputT]
```

```python
auto_instrument: bool
```

```python
_nodes: dict[NodeID, AnyNode]
```

```python
_edges_by_source: dict[NodeID, list[Path]]
```

```python
_decision_index: int
```



#### `start_node`

```python
def start_node(self) -> StartNode[GraphInputT]
```


Get the start node for the graph.

Returns:
    The start node that receives the initial graph input

#### `end_node`

```python
def end_node(self) -> EndNode[GraphOutputT]
```


Get the end node for the graph.

Returns:
    The end node that produces the final graph output

#### `step`

```python
def step(self, call: StepFunction[StateT, DepsT, InputT, OutputT] | None=None, *, node_id: str | None=None, label: str | None=None) -> Step[StateT, DepsT, InputT, OutputT] | Callable[[StepFunction[StateT, DepsT, InputT, OutputT]], Step[StateT, DepsT, InputT, OutputT]]
```


Create a step from a step function.

This method can be used as a decorator or called directly to create
a step node from an async function.

Args:
    call: The step function to wrap
    node_id: Optional ID for the node
    label: Optional human-readable label

Returns:
    Either a Step instance or a decorator function

#### `stream`

```python
def stream(self, call: StreamFunction[StateT, DepsT, InputT, OutputT] | None=None, *, node_id: str | None=None, label: str | None=None) -> Step[StateT, DepsT, InputT, AsyncIterable[OutputT]] | Callable[[StreamFunction[StateT, DepsT, InputT, OutputT]], Step[StateT, DepsT, InputT, AsyncIterable[OutputT]]]
```


Create a step from an async iterator (which functions like a "stream").

This method can be used as a decorator or called directly to create
a step node from an async function.

Args:
    call: The step function to wrap
    node_id: Optional ID for the node
    label: Optional human-readable label

Returns:
    Either a Step instance or a decorator function

#### `add`

```python
def add(self, *edges: EdgePath[StateT, DepsT]) -> None
```


Add one or more edge paths to the graph.

This method processes edge paths and automatically creates any necessary
fork nodes for broadcasts and maps.

Args:
    *edges: The edge paths to add to the graph

#### `add_edge`

```python
def add_edge(self, source: Source[T], destination: Destination[T], *, label: str | None=None) -> None
```


Add a simple edge between two nodes.

Args:
    source: The source node
    destination: The destination node
    label: Optional label for the edge

#### `add_mapping_edge`

```python
def add_mapping_edge(self, source: Source[Iterable[T]], map_to: Destination[T], *, pre_map_label: str | None=None, post_map_label: str | None=None, fork_id: ForkID | None=None, downstream_join_id: JoinID | None=None) -> None
```


Add an edge that maps iterable data across parallel paths.

Args:
    source: The source node that produces iterable data
    map_to: The destination node that receives individual items
    pre_map_label: Optional label before the map operation
    post_map_label: Optional label after the map operation
    fork_id: Optional ID for the fork node produced for this map operation
    downstream_join_id: Optional ID of a join node that will always be downstream of this map.
        Specifying this ensures correct handling if you try to map an empty iterable.

#### `edge_from`

```python
def edge_from(self, *sources: Source[SourceOutputT]) -> EdgePathBuilder[StateT, DepsT, SourceOutputT]
```


Create an edge path builder starting from the given source nodes.

Args:
    *sources: The source nodes to start the edge path from

Returns:
    An EdgePathBuilder for constructing the complete edge path

#### `decision`

```python
def decision(self, *, note: str | None=None, node_id: str | None=None) -> Decision[StateT, DepsT, Never]
```


Create a new decision node.

Args:
    note: Optional note to describe the decision logic
    node_id: Optional ID for the node produced for this decision logic

Returns:
    A new Decision node with no branches

#### `match`

```python
def match(self, source: TypeOrTypeExpression[SourceT], *, matches: Callable[[Any], bool] | None=None) -> DecisionBranchBuilder[StateT, DepsT, SourceT, SourceT, Never]
```


Create a decision branch matcher.

Args:
    source: The type or type expression to match against
    matches: Optional custom matching function

Returns:
    A DecisionBranchBuilder for constructing the branch

#### `match_node`

```python
def match_node(self, source: type[SourceNodeT], *, matches: Callable[[Any], bool] | None=None) -> DecisionBranch[SourceNodeT]
```


Create a decision branch for `BaseNode` subclasses.

This is similar to `match()` but specifically designed for matching against `BaseNode` types.

Args:
    source: The `BaseNode` subclass to match against
    matches: Optional custom matching function

Returns:
    A `DecisionBranch` for the `BaseNode` type

#### `node`

```python
def node(self, node_type: type[BaseNode[StateT, DepsT, GraphOutputT]]) -> EdgePath[StateT, DepsT]
```


Create an edge path from a `BaseNode` class.

This method integrates a `BaseNode` subclass into the builder graph by
analyzing its `run` return type hints and creating appropriate edges.

Args:
    node_type: The `BaseNode` subclass to integrate

Returns:
    An `EdgePath` representing the node and its connections

Raises:
    GraphSetupError: If the node type is missing required type hints





#### `build`

```python
def build(self, validate_graph_structure: bool=True) -> Graph[StateT, DepsT, GraphInputT, GraphOutputT]
```


Build the final executable graph from the accumulated nodes and edges.

This method performs validation, normalization, and analysis of the graph
structure to create a complete, executable graph instance.

Args:
    validate_graph_structure: whether to perform validation of the graph structure
        See the docstring of _validate_graph_structure below for more details.

Returns:
    A complete Graph instance ready for execution

Raises:
    ValueError: If the graph structure is invalid (e.g., join without parent fork)











### `MermaidNode`

```python
class MermaidNode
```


A mermaid node.

```python
id: str
```

```python
kind: NodeKind
```

```python
label: str | None
```

```python
note: str | None
```

### `MermaidEdge`

```python
class MermaidEdge
```


A mermaid edge.

```python
start_id: str
```

```python
end_id: str
```

```python
label: str | None
```

### `build_mermaid_graph`

```python
def build_mermaid_graph(graph_nodes: dict[NodeID, AnyNode], graph_edges_by_source: dict[NodeID, list[Path]]) -> MermaidGraph
```


Build a mermaid graph.

### `MermaidGraph`

```python
class MermaidGraph
```


A mermaid graph.

```python
nodes: list[MermaidNode]
```

```python
edges: list[MermaidEdge]
```

```python
title: str | None = None
```

```python
direction: StateDiagramDirection | None = None
```

