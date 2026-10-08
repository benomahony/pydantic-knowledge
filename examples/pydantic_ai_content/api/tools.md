# `pydantic_ai.tools`



### `matches_tool_selector`

```python
async def matches_tool_selector(selector: ToolSelector[AgentDepsT], ctx: RunContext[AgentDepsT], tool_def: ToolDefinition) -> bool
```


Check whether a tool definition matches a [`ToolSelector`][pydantic_ai.tools.ToolSelector].

Args:
    selector: The selector to check against.
    ctx: The current run context.
    tool_def: The tool definition to test.

Returns:
    `True` if the tool matches the selector.

### `Tool`

```python
class Tool
```


A tool function for an agent.

```python
function: ToolFuncEither[ToolAgentDepsT]
```

```python
takes_ctx: bool
```

```python
max_retries: int | None
```

```python
name: str
```

```python
description: str | None
```

```python
prepare: ToolPrepareFunc[ToolAgentDepsT] | None
```

```python
args_validator: ArgsValidatorFunc[ToolAgentDepsT, ...] | None
```

```python
docstring_format: DocstringFormat
```

```python
require_parameter_descriptions: bool
```

```python
strict: bool | None
```

```python
sequential: bool
```

```python
requires_approval: bool
```

```python
metadata: dict[str, Any] | None
```

```python
timeout: float | None
```

```python
defer_loading: bool
```

```python
include_return_schema: bool | None
```

```python
function_schema: _function_schema.FunctionSchema
```



#### `from_schema`

```python
def from_schema(cls, function: Callable[..., Any], name: str, description: str | None, json_schema: JsonSchemaValue, takes_ctx: bool=False, sequential: bool=False, args_validator: ArgsValidatorFunc[Any, ...] | None=None) -> Self
```


Creates a Pydantic tool from a function and a JSON schema.

Args:
    function: The function to call.
        This will be called with keywords only. Schema validation of
        the arguments is skipped, but a custom `args_validator` will
        still run if provided.
    name: The unique name of the tool that clearly communicates its purpose
    description: Used to tell the model how/when/why to use the tool.
        You can provide few-shot examples as a part of the description.
    json_schema: The schema for the function arguments
    takes_ctx: An optional boolean parameter indicating whether the function
        accepts the context object as an argument.
    sequential: Whether this tool acts as a barrier that runs alone, not overlapping with other tool calls.
        See [`ToolDefinition`][pydantic_ai.tools.ToolDefinition] for more info. Defaults to False.
    args_validator: custom method to validate tool arguments after schema validation has passed,
        before execution. The validator receives the already-validated and type-converted parameters,
        with `RunContext` as the first argument.
        Raise [`ModelRetry`][pydantic_ai.exceptions.ModelRetry] to ask the model to correct the
        arguments and try again, or [`ToolFailed`][pydantic_ai.exceptions.ToolFailed] to report a
        terminal failure the model should adapt to instead of retrying. Return `None` on success.
        See [`ArgsValidatorFunc`][pydantic_ai.tools.ArgsValidatorFunc].

Returns:
    A Pydantic tool that calls the function

#### `prepare_tool_def`

```python
async def prepare_tool_def(self, ctx: RunContext[ToolAgentDepsT]) -> ToolDefinition | None
```


Get the tool definition.

By default, this method creates a tool definition, then either returns it, or calls `self.prepare`
if it's set.

Returns:
    return a `ToolDefinition` or `None` if the tools should not be registered for this run.

### `ToolDefinition`

```python
class ToolDefinition
```


Definition of a tool passed to a model.

This is used for both function tools and output tools.

```python
name: str
```

```python
parameters_json_schema: ObjectJsonSchema = field(default_factory=lambda: {'type': 'object', 'properties': {}})
```

```python
description: str | None = None
```

```python
outer_typed_dict_key: str | None = None
```

```python
strict: bool | None = None
```

```python
sequential: bool = False
```

```python
kind: ToolKind = field(default='function')
```

```python
metadata: dict[str, Any] | None = None
```

```python
timeout: float | None = None
```

```python
defer_loading: bool = False
```

```python
unless_native: Annotated[str | None, Field(validation_alias=AliasChoices('unless_native', 'prefer_native', 'prefer_builtin'))] = None
```

```python
with_native: str | None = None
```

```python
tool_kind: ToolPartKind | None = None
```

```python
return_schema: ObjectJsonSchema | None = None
```

```python
include_return_schema: bool | None = None
```

```python
toolset_id: str | None = None
```

```python
capability_id: str | None = None
```

#### `function_signature`

```python
def function_signature(self) -> FunctionSignature
```


The function signature shape for this tool.

Lazily computed from `parameters_json_schema` and `return_schema` on first access.
Name and description are not stored on the signature — pass them at render time
via `sig.render(body, name=td.name, description=td.description)`.

#### `render_signature`

```python
def render_signature(self, body: str, **kwargs: Any) -> str
```


Render the function signature with this tool's name and description.

Convenience wrapper around `self.function_signature.render()` that
supplies `name` and `description` from this tool definition.

#### `defer`

```python
def defer(self) -> bool
```


Whether calls to this tool will be deferred.

See the [tools documentation](../deferred-tools.md#deferred-tools) for more info.## `UseEnumMemberDocstrings`

```python
class UseEnumMemberDocstrings
```


Mix into an `Enum` to describe each of its members by the docstring written under it.

This is the enum counterpart to `model_config = ConfigDict(use_attribute_docstrings=True)` on a Pydantic
model, which is how a model's fields get their docstrings as descriptions. With it, the enum is described
to the model as `anyOf` of `const`s carrying those docstrings as descriptions, rather than as a bare list
of values, so the model can tell similar options apart. Without it the docstrings are ignored and the
schema is unchanged.

The two are expressed differently because an `Enum` has no `model_config` to carry a flag, and cannot carry
a plain class attribute either — annotated or not, any assigned value becomes a member. A base class is the
only marker left, so mix it in ahead of `str`, `int` or `Enum`:
`class Urgency(UseEnumMemberDocstrings, str, Enum)`. It changes nothing else about the enum: its members,
their values, and their `str`/`int` behaviour are exactly what they would be without it.

See [enum options](../tools.md#enum-options) for an example.```python
ParallelExecutionMode = Literal['parallel', 'sequential', 'parallel_ordered_events']
```## `ToolManager`

```python
class ToolManager
```


Manages tools for an agent run step. It caches the agent run's toolset's tool definitions and handles calling tools and retries.

```python
toolset: AbstractToolset[AgentDepsT]
```

```python
root_capability: AbstractCapability[AgentDepsT] | None = None
```

```python
ctx: RunContext[AgentDepsT] | None = None
```

```python
tools: dict[str, ToolsetTool[AgentDepsT]] | None = None
```

```python
failed_tools: set[str] = field(default_factory=set[str])
```

```python
succeeded_tools: set[str] = field(default_factory=set[str])
```

```python
availability_refused: set[str] = field(default_factory=set[str])
```

```python
default_max_retries: int = 1
```

```python
resolved_capability_ids: frozenset[str] | None = None
```

### `parallel_execution_mode`

```python
def parallel_execution_mode(cls, mode: ParallelExecutionMode='parallel') -> Generator[None]
```


Set the parallel execution mode during the context.

Args:
    mode: The execution mode for tool calls:
        - 'parallel': Run tool calls in parallel, yielding events as they complete (default).
        - 'sequential': Run tool calls one at a time in order.
        - 'parallel_ordered_events': Run tool calls in parallel, but events are emitted in order, after all calls complete.

### `for_run_step`

```python
async def for_run_step(self, ctx: RunContext[AgentDepsT]) -> ToolManager[AgentDepsT]
```


Build a new tool manager for the next run step, carrying over the retries from the current run step.

Re-resolves within a step as well, when capability availability moved since the cached tools
were resolved (see `resolved_capability_ids`), so a capability that became active mid-step
still gets its `prepare_tools` say over its own tools.

### `tool_defs`

```python
def tool_defs(self) -> list[ToolDefinition]
```


The tool definitions for the tools in this tool manager.

### `get_parallel_execution_mode`

```python
def get_parallel_execution_mode(self) -> ParallelExecutionMode
```


Get the run-scoped parallel execution mode set via [`parallel_execution_mode`][pydantic_ai.tool_manager.ToolManager.parallel_execution_mode].

Per-tool `sequential=True` barriers are applied separately during execution and don't
affect this run-scoped mode: a single barrier tool no longer forces the whole batch
serial (the v1 behavior). Use `parallel_execution_mode('sequential')` to opt the entire
run into serial execution.

### `is_sequential`

```python
def is_sequential(self, call: ToolCallPart) -> bool
```


Whether a tool call must run as a barrier (`sequential=True`), executing alone.

Tools emitted before a barrier complete first; the barrier runs by itself; tools emitted
after it start only once it finishes. Other tools parallelize around it.

### `get_tool_def`

```python
def get_tool_def(self, name: str) -> ToolDefinition | None
```


Get the tool definition for a given tool name, or `None` if the tool is unknown.























### `validate_tool_call`

```python
async def validate_tool_call(self, call: ToolCallPart, *, approved: bool=False, metadata: Any=None, wrap_validation_errors: bool=True) -> ValidatedToolCall[AgentDepsT]
```


Validate tool arguments without executing the tool.

This method validates arguments BEFORE the tool is executed, allowing the caller to:
1. Emit `FunctionToolCallEvent` / `OutputToolCallEvent` with accurate `args_valid` status
2. Handle validation failures differently from execution failures
3. Decide whether to execute or defer based on validation result

A tool call can be deferred during validation by raising
[`ApprovalRequired`][pydantic_ai.exceptions.ApprovalRequired] or
[`CallDeferred`][pydantic_ai.exceptions.CallDeferred] — but only once its arguments are known
to be valid, which the caller is shown. That means the tool's `args_validator`,
`after_tool_validate`, or `wrap_tool_validate` after its handler has returned; the same
exception raised before validation has run raises a `UserError` naming the alternatives.

A permitted deferral is control flow rather than a validation failure: the returned
`ValidatedToolCall` has `args_valid=True` and carries the exception on
[`deferral`][pydantic_ai.tool_manager.ValidatedToolCall.deferral], which `execute_tool_call`
raises in place of running the tool, so callers handle deferrals in one place.

Args:
    call: The tool call part to validate.
    approved: Whether the tool call has been approved.
    metadata: Additional metadata from DeferredToolResults.metadata.
    wrap_validation_errors: If True (default), wrap `ValidationError` / `ModelRetry`
        as `ToolRetryError` on the returned `ValidatedToolCall.validation_error`,
        count the call against the retry budget, and add it to `failed_tools`.
        `ToolFailed` is wrapped as `ToolFailedError` without consuming the retry
        budget. If False, propagate the raw exception and leave retry-budget state
        untouched — useful for nested callers (e.g. sandboxed tool dispatch) where
        validation failures shouldn't consume the agent's retry budget and the raw
        exception is what the caller wants to surface.

Returns:
    ValidatedToolCall with validation results, ready for execution via execute_tool_call().

### `execute_tool_call`

```python
async def execute_tool_call(self, validated: ValidatedToolCall[AgentDepsT], *, wrap_validation_errors: bool=True) -> Any
```


Execute a validated tool call via capability hooks.

The Instrumentation capability (if present) creates trace spans via its
wrap_tool_execute hook.

Args:
    validated: The validation result from validate_tool_call().
    wrap_validation_errors: If True (default), `ModelRetry` raised by the tool
        body or by execute-stage capability hooks (`before_tool_execute`,
        `after_tool_execute`, `wrap_tool_execute`) is wrapped as `ToolRetryError`
        after counting against the retry budget. If False, the raw
        `ModelRetry` / `ValidationError` propagates and retry-budget state is
        left untouched.

Returns:
    The tool result if validation passed and execution succeeded.

Raises:
    ToolRetryError: If validation failed with a retry prompt or the tool raised
        `ModelRetry`. Only when `wrap_validation_errors=True`.
    ToolFailedError: If validation failed with `ToolFailed`, or the tool raised
        `ToolFailed`. Only when `wrap_validation_errors=True`.
    ModelRetry / ValidationError / ToolFailed: When `wrap_validation_errors=False`.
    CallDeferred / ApprovalRequired: If the tool's `args_validator` deferred the call
        (see [`ValidatedToolCall.deferral`][pydantic_ai.tool_manager.ValidatedToolCall.deferral])
        or the tool function raised one of these itself. The tool is not executed in the
        former case.
    RuntimeError: If trying to execute an external tool.

### `validate_output_tool_call`

```python
async def validate_output_tool_call(self, call: ToolCallPart, *, schema: OutputSchema[Any], allow_partial: bool=False, wrap_validation_errors: bool=True) -> ValidatedToolCall[AgentDepsT]
```


Validate output tool args through output validate hooks (skipping tool hooks).

Output tools use output hooks for validation instead of tool hooks. The Pydantic
schema validation is used as the inner handler wrapped by output validate hooks.

`schema` is the run's output schema; it's forwarded to
[`OutputContext`][pydantic_ai.output.OutputContext] so hooks can see the full shape
of what the schema accepts.

Raises:
    UnexpectedModelBehavior: If max retries exceeded.

### `execute_output_tool_call`

```python
async def execute_output_tool_call(self, validated: ValidatedToolCall[AgentDepsT], *, schema: OutputSchema[Any], wrap_validation_errors: bool=True) -> Any
```


Execute output tool through output process hooks (skipping tool hooks).

Output validators run inside process hooks (inside wrap_output_process), ensuring
the complete output pipeline is wrapped. Validators see the global output retry
context (from self.ctx), not the per-tool context, matching the text output path.

`schema` is the run's output schema; it's forwarded to
[`OutputContext`][pydantic_ai.output.OutputContext] so hooks can see the full shape
of what the schema accepts.

Raises:
    ToolRetryError: If execution or output validation fails.
    UnexpectedModelBehavior: If max retries exceeded.

### `handle_output_tool_call`

```python
async def handle_output_tool_call(self, call: ToolCallPart, *, schema: OutputSchema[Any], allow_partial: bool=False, wrap_validation_errors: bool=True) -> Any
```


Handle an output tool call using output hooks (not tool hooks).

Convenience method combining validate_output_tool_call and execute_output_tool_call.
Used by the streaming path in result.py.





### `handle_call`

```python
async def handle_call(self, call: ToolCallPart, *, approved: bool=False, metadata: Any=None, wrap_validation_errors: bool=True, on_deferred_requests: InlineDeferredRequestsHandler | None=None, on_inline_deferred: InlineDeferredResultHandler | None=None, on_validate: ToolValidationHandler | None=None) -> ToolDenied | ToolReturn[Any] | Any
```


Handle a tool call by validating the arguments, calling the tool, and handling retries.

This is a convenience method that combines validate_tool_call() and execute_tool_call().

If the tool or its `args_validator` raises
[`ApprovalRequired`][pydantic_ai.exceptions.ApprovalRequired] or
[`CallDeferred`][pydantic_ai.exceptions.CallDeferred], the capability handler
(if any) is invoked to resolve it inline; otherwise the exception propagates.

Args:
    call: The tool call part to handle.
    approved: Whether the tool call has been approved.
    metadata: Additional metadata from DeferredToolResults.metadata.
    wrap_validation_errors: If True (default), validation failures surface as
        `ToolRetryError` (after counting against the retry budget) or
        `ToolFailedError` (without consuming the retry budget). If False, the
        raw `ValidationError` / `ModelRetry` / `ToolFailed` propagates and
        retry-budget state is left untouched — useful for nested callers (e.g.
        sandboxed tool dispatch) where the call shouldn't consume the agent's
        retry budget and the raw exception is what the caller wants to surface.
    on_deferred_requests: Internal callback invoked with a deferred call's requests before the
        capability handler is asked to resolve it.
    on_inline_deferred: Internal callback invoked when a capability resolves a deferred call inline.
    on_validate: Internal callback invoked with the argument-validation outcome before execution.

Returns:
    The tool's return value on success — possibly a [`ToolReturn`][pydantic_ai.messages.ToolReturn]
    wrapper if the tool or handler supplied one.

    A [`ToolDenied`][pydantic_ai.tools.ToolDenied] instance if a
    [`HandleDeferredToolCalls`][pydantic_ai.capabilities.HandleDeferredToolCalls]
    handler denied the call. **Callers must `isinstance`-check the result**
    before treating it as a successful tool return — `ToolDenied` is *not* a
    valid tool result and the message string alone is indistinguishable from
    a real return value. Surfacing the denial (e.g. recording
    `ToolReturnPart(outcome='denied')` in message history, or raising inside
    a sandbox) is the caller's responsibility.

Raises:
    ToolRetryError: The handler requested a retry, or the (re-)executed tool
        raised `ModelRetry`. Only when `wrap_validation_errors=True`.
    ValidationError / ModelRetry: When `wrap_validation_errors=False` and the
        arguments fail validation or a hook raises `ModelRetry`.
    CallDeferred / ApprovalRequired: No handler resolved the call, or the
        approved tool re-raised a deferral.

### `resolve_deferred_tool_calls`

```python
async def resolve_deferred_tool_calls(self, requests: DeferredToolRequests) -> DeferredToolResults | None
```


Invoke the capability handler to resolve deferred tool calls.

Args:
    requests: The deferred tool requests to resolve.

Returns:
    `DeferredToolResults` with results for some or all calls, or `None` if
    no handler is available or the handler declined to handle the requests.

