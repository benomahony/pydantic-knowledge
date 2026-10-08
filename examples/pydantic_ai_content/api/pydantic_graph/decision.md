# `pydantic_graph.decision`

Decision node implementation for conditional branching in graph execution.

This module provides the Decision node type and related classes for implementing
conditional branching logic in parallel control flow graphs. Decision nodes allow the graph
to choose different execution paths based on runtime conditions.

### `Decision`

```python
class Decision
```


Decision node for conditional branching in graph execution.

A Decision node evaluates conditions and routes execution to different
branches based on the input data type or custom matching logic.

```python
id: NodeID
```

```python
branches: list[DecisionBranch[Any]]
```

```python
note: str | None
```

#### `branch`

```python
def branch(self, branch: DecisionBranch[T]) -> Decision[StateT, DepsT, HandledT | T]
```


Add a new branch to this decision.

Args:
    branch: The branch to add to this decision.

Returns:
    A new Decision with the additional branch.



### `DecisionBranch`

```python
class DecisionBranch
```


Represents a single branch within a decision node.

Each branch defines the conditions under which it should be taken
and the path to follow when those conditions are met.

Note: with the current design, it is actually _critical_ that this class is invariant in SourceT for the sake
of type-checking that inputs to a Decision are actually handled. See the `# type: ignore` comment in
`tests.graph.builder.test_graph_edge_cases.test_decision_no_matching_branch` for an example of how this works.

```python
source: TypeOrTypeExpression[SourceT]
```

```python
matches: Callable[[Any], bool] | None
```

```python
path: Path
```

```python
destinations: list[AnyDestinationNode]
```

### `DecisionBranchBuilder`

```python
class DecisionBranchBuilder
```


Builder for constructing decision branches with fluent API.

This builder provides methods to configure branches with destinations,
forks, and transformations in a type-safe manner.

Instances of this class should be created using [`GraphBuilder.match`][pydantic_graph.graph_builder.GraphBuilder],
not created directly.

```python
_decision: Decision[StateT, DepsT, HandledT]
```

```python
_source: TypeOrTypeExpression[SourceT]
```

```python
_matches: Callable[[Any], bool] | None
```

```python
_path_builder: PathBuilder[StateT, DepsT, OutputT]
```

#### `to`

```python
def to(self, destination: DestinationNode[StateT, DepsT, OutputT] | type[BaseNode[StateT, DepsT, Any]], /, *extra_destinations: DestinationNode[StateT, DepsT, OutputT] | type[BaseNode[StateT, DepsT, Any]], fork_id: str | None=None) -> DecisionBranch[SourceT]
```


Set the destination(s) for this branch.

Args:
    destination: The primary destination node.
    *extra_destinations: Additional destination nodes.
    fork_id: Optional node ID to use for the resulting broadcast fork if multiple destinations are provided.

Returns:
    A completed DecisionBranch with the specified destinations.

#### `broadcast`

```python
def broadcast(self, get_forks: Callable[[Self], Sequence[DecisionBranch[SourceT]]], /, *, fork_id: str | None=None) -> DecisionBranch[SourceT]
```


Broadcast this decision branch into multiple destinations.

Args:
    get_forks: The callback that will return a sequence of decision branches to broadcast to.
    fork_id: Optional node ID to use for the resulting broadcast fork.

Returns:
    A completed DecisionBranch with the specified destinations.

#### `transform`

```python
def transform(self, func: TransformFunction[StateT, DepsT, OutputT, NewOutputT], /) -> DecisionBranchBuilder[StateT, DepsT, NewOutputT, SourceT, HandledT]
```


Apply a transformation to the branch's output.

Args:
    func: Transformation function to apply.

Returns:
    A new DecisionBranchBuilder where the provided transform is applied prior to generating the final output.

#### `map`

```python
def map(self: DecisionBranchBuilder[StateT, DepsT, Iterable[T], SourceT, HandledT] | DecisionBranchBuilder[StateT, DepsT, AsyncIterable[T], SourceT, HandledT], *, fork_id: str | None=None, downstream_join_id: str | None=None) -> DecisionBranchBuilder[StateT, DepsT, T, SourceT, HandledT]
```


Spread the branch's output.

To do this, the current output must be iterable, and any subsequent steps in the path being built for this
branch will be applied to each item of the current output in parallel.

Args:
    fork_id: Optional ID for the fork, defaults to a generated value
    downstream_join_id: Optional ID of a downstream join node which is involved when mapping empty iterables

Returns:
    A new DecisionBranchBuilder where mapping is performed prior to generating the final output.

#### `label`

```python
def label(self, label: str) -> DecisionBranchBuilder[StateT, DepsT, OutputT, SourceT, HandledT]
```


Apply a label to the branch at the current point in the path being built.

These labels are only used in generated mermaid diagrams.

Args:
    label: The label to apply.

Returns:
    A new DecisionBranchBuilder where the label has been applied at the end of the current path being built.