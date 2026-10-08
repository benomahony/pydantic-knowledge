# `pydantic_ai.agent`















### `Agent`

```python
class Agent
```


Class for defining "agents" - a way to have a specific type of "conversation" with an LLM.

Agents are generic in the dependency type they take [`AgentDepsT`][pydantic_ai.tools.AgentDepsT]
and the output type they return, [`OutputDataT`][pydantic_ai.output.OutputDataT].

By default, if neither generic parameter is customised, agents have type `Agent[object, str]`.

Minimal usage example:

```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-5.2')
result = agent.run_sync('What is the capital of France?')
print(result.output)
#> The capital of France is Paris.
```

```python
_model: models.Model | models.KnownModelName | str | None
```

```python
_name: str | None
```

```python
_description: TemplateStr[AgentDepsT] | str | None
```

```python
end_strategy: EndStrategy
```

```python
model_settings: AgentModelSettings[AgentDepsT] | None
```

```python
_output_type: OutputSpec[OutputDataT]
```

```python
_instrument: InstrumentationSettings | bool | None
```

```python
_instrument_default: ClassVar[InstrumentationSettings | bool] = False
```

```python
_metadata: AgentMetadata[AgentDepsT] | None = dataclasses.field(repr=False)
```

```python
_deps_type: type[AgentDepsT] = dataclasses.field(repr=False)
```

```python
_output_schema: _output.OutputSchema[OutputDataT] = dataclasses.field(repr=False)
```

```python
_output_validators: list[_output.OutputValidator[AgentDepsT, OutputDataT]] = dataclasses.field(repr=False)
```

```python
_instructions: list[_instructions.SourcedInstruction[AgentDepsT]] = dataclasses.field(repr=False)
```

```python
_system_prompts: tuple[str, ...] = dataclasses.field(repr=False)
```

```python
_system_prompt_functions: list[_system_prompt.SystemPromptRunner[AgentDepsT]] = dataclasses.field(repr=False)
```

```python
_system_prompt_dynamic_functions: dict[str, _system_prompt.SystemPromptRunner[AgentDepsT]] = dataclasses.field(repr=False)
```

```python
_function_toolset: FunctionToolset[AgentDepsT] = dataclasses.field(repr=False)
```

```python
_output_toolset: OutputToolset[AgentDepsT] | None = dataclasses.field(repr=False)
```

```python
_user_toolsets: list[AbstractToolset[AgentDepsT]] = dataclasses.field(repr=False)
```

```python
_max_output_retries: int = dataclasses.field(repr=False)
```

```python
_max_tool_retries: int = dataclasses.field(repr=False)
```

```python
_tool_timeout: float | None = dataclasses.field(repr=False)
```

```python
_validation_context: Any | Callable[[RunContext[AgentDepsT]], Any] = dataclasses.field(repr=False)
```

```python
_event_stream_handler: EventStreamHandler[AgentDepsT] | None = dataclasses.field(repr=False)
```

```python
_concurrency_limiter: _concurrency.AbstractConcurrencyLimiter | None = dataclasses.field(repr=False)
```

```python
_entered_count: int = dataclasses.field(repr=False)
```

```python
_exit_stack: AsyncExitStack | None = dataclasses.field(repr=False)
```



#### `from_spec`

```python
def from_spec(cls, spec: dict[str, Any] | AgentSpec, *, deps_type: type[Any]=type(None), custom_capability_types: Sequence[type[AbstractCapability[Any]]]=(), model: models.Model | models.KnownModelName | str | None=None, output_type: OutputSpec[Any]=str, instructions: AgentInstructions[Any]=None, system_prompt: str | Sequence[str]=(), name: str | None=None, description: TemplateStr[Any] | str | None=None, model_settings: ModelSettings | None=None, retries: int | AgentRetries | None=None, validation_context: Any=None, tools: Sequence[Tool[Any] | ToolFuncEither[Any, ...]]=(), toolsets: Sequence[AgentToolset[Any]] | None=None, defer_model_check: bool=False, end_strategy: EndStrategy | None=None, metadata: AgentMetadata[Any] | None=None, tool_timeout: float | None=None, max_concurrency: _concurrency.AnyConcurrencyLimit=None, capabilities: Sequence[AgentCapability[Any]] | None=None) -> Agent[Any, Any]
```


Construct an Agent from a spec dict or `AgentSpec`.

This allows defining agents declaratively in YAML/JSON/dict form.
Keyword arguments supplement the spec: scalar spec fields (like `name`,
`retries`) are used as defaults that explicit arguments override, while
`capabilities` from both sources are merged.

Args:
    spec: The agent specification, either a dict or an `AgentSpec` instance.
    deps_type: The type of the dependencies for the agent. When provided,
        template strings in capabilities (e.g. `"Hello {{name}}"`) are
        compiled and validated against this type.
    custom_capability_types: Additional capability classes to make available
        beyond the built-in defaults.
    model: Override the model from the spec.
    output_type: The type of the output data, defaults to `str`.
    instructions: Instructions for the agent.
    system_prompt: Static system prompts.
    name: The agent name, overrides spec `name` if provided.
    description: The agent description, overrides spec `description` if provided.
    model_settings: Model request settings.
    retries: Retry budgets for tools and output validation. Pass an `int` to set the same budget
        for both, or an [`AgentRetries`][pydantic_ai.AgentRetries] dict to set them individually.
        Overrides spec `retries` if provided.
    validation_context: Pydantic validation context for tool arguments and outputs.
    tools: Tools to register with the agent.
    toolsets: Toolsets to register with the agent.
    defer_model_check: Defer model evaluation until first run.
    end_strategy: Strategy for tool calls alongside a final result, overrides spec `end_strategy` if provided.
    metadata: Metadata to store with each run, overrides spec `metadata` if provided.
    tool_timeout: Default timeout for tool execution, overrides spec `tool_timeout` if provided.

    max_concurrency: Limit on concurrent agent runs.
    capabilities: Additional capabilities merged with those from the spec.

Returns:
    A new Agent instance.

#### `from_file`

```python
def from_file(cls, path: Path | str, *, fmt: Literal['yaml', 'json'] | None=None, deps_type: type[Any]=type(None), custom_capability_types: Sequence[type[AbstractCapability[Any]]]=(), model: models.Model | models.KnownModelName | str | None=None, output_type: OutputSpec[Any]=str, instructions: AgentInstructions[Any]=None, system_prompt: str | Sequence[str]=(), name: str | None=None, description: TemplateStr[Any] | str | None=None, model_settings: ModelSettings | None=None, retries: int | AgentRetries | None=None, validation_context: Any=None, tools: Sequence[Tool[Any] | ToolFuncEither[Any, ...]]=(), toolsets: Sequence[AgentToolset[Any]] | None=None, defer_model_check: bool=False, end_strategy: EndStrategy | None=None, metadata: AgentMetadata[Any] | None=None, tool_timeout: float | None=None, max_concurrency: _concurrency.AnyConcurrencyLimit=None, capabilities: Sequence[AgentCapability[Any]] | None=None) -> Agent[Any, Any]
```


Construct an Agent from a YAML or JSON spec file.

This is a convenience method equivalent to
`Agent.from_spec(AgentSpec.from_file(path), ...)`.

The file format is inferred from the extension (`.yaml`/`.yml` or `.json`)
unless overridden with the `fmt` argument.

All other arguments are forwarded to [`from_spec`][pydantic_ai.agent.Agent.from_spec].

#### `instrument_all`

```python
def instrument_all(instrument: InstrumentationSettings | bool=True) -> None
```


Set the instrumentation options for all agents that don't explicitly add an `Instrumentation` capability.

#### `instrument`

```python
def instrument(self) -> InstrumentationSettings | bool | None
```


Instrumentation settings applied to this agent.

#### `model`

```python
def model(self) -> models.Model | models.KnownModelName | str | None
```


The default model configured for this agent.

#### `model`

```python
def model(self, value: models.Model | models.KnownModelName | str | None) -> None
```


Set the default model configured for this agent.

We allow `str` here since the actual list of allowed models changes frequently.

#### `name`

```python
def name(self) -> str | None
```


The name of the agent, used for logging.

If `None`, we try to infer the agent name from the call frame when the agent is first run.

#### `name`

```python
def name(self, value: str | None) -> None
```


Set the name of the agent, used for logging.

#### `description`

```python
def description(self) -> str | None
```


A human-readable description of the agent.

If the description is a TemplateStr, returns the raw template source.
The rendered description is available at runtime via OTel span attributes.

#### `description`

```python
def description(self, value: TemplateStr[AgentDepsT] | str | None) -> None
```


Set the description of the agent.

#### `render_description`

```python
def render_description(self, deps: AgentDepsT=None) -> str | None
```


Return the agent description, rendering any TemplateStr with the given deps.

#### `deps_type`

```python
def deps_type(self) -> type
```


The type of dependencies used by the agent.

#### `output_type`

```python
def output_type(self) -> OutputSpec[OutputDataT]
```


The type of data output by agent runs, used to validate the data returned by the model, defaults to `str`.

#### `event_stream_handler`

```python
def event_stream_handler(self) -> EventStreamHandler[AgentDepsT] | None
```


Optional handler for events from the model's streaming response and the agent's execution of tools.

#### `validation_context`

```python
def validation_context(self) -> Any | Callable[[RunContext[AgentDepsT]], Any]
```


The Pydantic validation context used to validate tool arguments and outputs.

Set this when validators need values from [`ValidationInfo.context`][pydantic.ValidationInfo.context].
A callable can build the context from the current [`RunContext`][pydantic_ai.tools.RunContext].

#### `iter`

```python
async def iter(self, user_prompt: str | Sequence[_messages.UserContent] | None=None, *, output_type: OutputSpec[Any] | None=None, message_history: Sequence[_messages.ModelMessage] | None=None, deferred_tool_results: DeferredToolResults | None=None, conversation_id: str | None=None, run_id: str | None=None, model: models.Model | models.KnownModelName | str | None=None, instructions: AgentInstructions[AgentDepsT]=None, deps: AgentDepsT=None, model_settings: AgentModelSettings[AgentDepsT] | None=None, usage_limits: _usage.UsageLimits | None=None, cancellation_token: CancellationToken | None=None, usage: _usage.RunUsage | None=None, metadata: AgentMetadata[AgentDepsT] | None=None, retries: int | AgentRetries | None=None, infer_name: bool=True, toolsets: Sequence[AbstractToolset[AgentDepsT]] | None=None, capabilities: Sequence[AgentCapability[AgentDepsT]] | None=None, workspace: WorkspaceBackend | WorkspaceRef | Literal['new'] | None=None, spec: dict[str, Any] | AgentSpec | None=None) -> AsyncGenerator[AgentRun[AgentDepsT, Any]]
```


A contextmanager which can be used to iterate over the agent graph's nodes as they are executed.

This method builds an internal agent graph (using system prompts, tools and output schemas) and then returns an
`AgentRun` object. The `AgentRun` can be used to async-iterate over the nodes of the graph as they are
executed. This is the API to use if you want to consume the outputs coming from each LLM model response, or the
stream of events coming from the execution of tools.

The `AgentRun` also provides methods to access the full message history, new messages, and usage statistics,
and the final result of the run once it has completed.

For more details, see the documentation of `AgentRun`.

Example:
```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-5.2')

async def main():
    nodes = []
    async with agent.iter('What is the capital of France?') as agent_run:
        async for node in agent_run:
            nodes.append(node)
    print(nodes)
    '''
    [
        UserPromptNode(
            user_prompt='What is the capital of France?',
            instructions_functions=[],
            system_prompts=(),
            system_prompt_functions=[],
            system_prompt_dynamic_functions={},
        ),
        ModelRequestNode(
            request=ModelRequest(
                parts=[
                    UserPromptPart(
                        content='What is the capital of France?',
                        timestamp=datetime.datetime(...),
                    )
                ],
                timestamp=datetime.datetime(...),
                run_id='...',
                conversation_id='...',
            )
        ),
        CallToolsNode(
            model_response=ModelResponse(
                parts=[TextPart(content='The capital of France is Paris.')],
                usage=RequestUsage(
                    cost=Decimal('0.000196'), input_tokens=56, output_tokens=7
                ),
                model_name='gpt-5.2',
                timestamp=datetime.datetime(...),
                run_id='...',
                conversation_id='...',
            )
        ),
        End(data=FinalResult(output='The capital of France is Paris.')),
    ]
    '''
    assert agent_run.result is not None
    print(agent_run.result.output)
    #> The capital of France is Paris.
```

Args:
    user_prompt: User input to start/continue the conversation.
    output_type: Custom output type to use for this run, `output_type` may only be used if the agent has no
        output validators since output validators would expect an argument that matches the agent's output type.
    message_history: History of the conversation so far.
    deferred_tool_results: Optional results for deferred tool calls in the message history.
    conversation_id: ID of the conversation this run belongs to. Pass `'new'` to start a fresh conversation, ignoring any `conversation_id` already on `message_history`. If omitted, falls back to the most recent `conversation_id` on `message_history` or a freshly generated UUID7.
    run_id: Optional ID for this agent run. Unlike `conversation_id`, never inherited from `message_history`. Passing an empty string, or a value that already appears on `message_history`, raises `UserError` because both break `new_messages()`; use `conversation_id` to correlate across turns or deferred-tool resume. If omitted, a fresh UUID7 is generated, except that an agent with a workspace capability, run inside a Temporal workflow, DBOS workflow or Prefect flow, gets one derived from the workflow or flow run so its workspace state survives worker recovery.
    model: Optional model to use for this run, required if `model` was not set when creating the agent.
    instructions: Optional additional instructions to use for this run.
    deps: Optional dependencies to use for this run.
    model_settings: Optional settings to use for this model's request, or a callable
        that receives [`RunContext`][pydantic_ai.tools.RunContext] and returns settings.
        Callables are called before each model request, allowing dynamic per-step settings.
    usage_limits: Optional limits on model request count or token usage.
    cancellation_token: Token used to cancel this run from another task or thread. Single-use:
        mint a fresh token per run, as a reused (already-cancelled) token prevents the run from starting.
    usage: Optional usage to start with, useful for resuming a conversation or agents used in tools.
    metadata: Optional metadata to attach to this run. Accepts a dictionary or a callable taking
        [`RunContext`][pydantic_ai.tools.RunContext]; merged with the agent's configured metadata.
    retries: Override the agent-level retry budgets for this run. Pass an `int` to override both
        the tool-retry and output budgets, or an [`AgentRetries`][pydantic_ai.AgentRetries] dict to
        override just one (e.g. `retries={'tools': 3}`). See
        [`Agent.__init__`][pydantic_ai.agent.Agent.__init__] for semantics of the two enforcement paths.
    infer_name: Whether to try to infer the agent name from the call frame if it's not set.
    toolsets: Optional additional toolsets for this run.
    capabilities: Optional additional [capabilities](https://pydantic.dev/docs/ai/capabilities/overview/) for this run, merged with the agent's configured capabilities.
    workspace: Optional [workspace](../workspace.md) for this run: a backend or `Workspace` to use as is, a `WorkspaceRef` to continue in, or `'new'` for a fresh one instead of the one in `message_history`.
    spec: Optional agent spec to apply for this run. At run time, spec values are additive.

Returns:
    The result of the run.



#### `override`

```python
def override(self, *, name: str | _utils.Unset=_utils.UNSET, deps: AgentDepsT | _utils.Unset=_utils.UNSET, model: models.Model | models.KnownModelName | str | _utils.Unset=_utils.UNSET, toolsets: Sequence[AbstractToolset[AgentDepsT]] | _utils.Unset=_utils.UNSET, tools: Sequence[Tool[AgentDepsT] | ToolFuncEither[AgentDepsT, ...]] | _utils.Unset=_utils.UNSET, native_tools: Sequence[AgentNativeTool[AgentDepsT]] | _utils.Unset=_utils.UNSET, instructions: AgentInstructions[AgentDepsT] | _utils.Unset=_utils.UNSET, metadata: AgentMetadata[AgentDepsT] | _utils.Unset=_utils.UNSET, model_settings: AgentModelSettings[AgentDepsT] | _utils.Unset=_utils.UNSET, retries: int | AgentRetries | _utils.Unset=_utils.UNSET, spec: dict[str, Any] | AgentSpec | None=None, workspace: WorkspaceBackend | Workspace | WorkspaceRef | Literal['new'] | _utils.Unset=_utils.UNSET) -> Generator[None]
```


Context manager to temporarily override agent configuration.

This is particularly useful when testing.
You can find an example of this [here](../testing.md#overriding-model-via-pytest-fixtures).

Args:
    name: The name to use instead of the name passed to the agent constructor and agent run.
    deps: The dependencies to use instead of the dependencies passed to the agent run.
    model: The model to use instead of the model passed to the agent run.
    toolsets: The toolsets to use instead of the toolsets passed to the agent constructor and agent run.
    tools: The tools to use instead of the tools registered with the agent.
    native_tools: The native tools to use instead of the agent's configured native tools.
    instructions: The instructions to use instead of the instructions registered with the agent.
        Note: this also replaces capability-contributed instructions (e.g. from
        [`get_instructions`][pydantic_ai.capabilities.AbstractCapability.get_instructions]).
    metadata: The metadata to use instead of the metadata passed to the agent constructor. When set, any
        per-run `metadata` argument is ignored.
    model_settings: The model settings to use instead of the model settings passed to the agent constructor.
        When set, any per-run `model_settings` argument is ignored.
    retries: The retry budgets to use instead of the agent-level configuration. Pass an `int` to
        override both the tool-retry and output budgets, or an [`AgentRetries`][pydantic_ai.AgentRetries]
        dict to override just one (e.g. `retries={'tools': 3}`).
        When set, any per-run `retries` argument is ignored.
    workspace: Workspace for every run in this context, in place of a per-run `workspace=` argument.
    spec: Optional agent spec providing defaults for override. Explicit params take precedence
        over spec values. When the spec includes `capabilities`, they replace (not merge with)
        the agent's existing capabilities. To add capabilities without replacing, pass `spec`
        to `run()` or `iter()` instead.

#### `instructions`

```python
def instructions(self, func: SystemPromptFunc[AgentDepsT] | None=None, /, *, name: str | None=None) -> Callable[[SystemPromptFunc[AgentDepsT]], SystemPromptFunc[AgentDepsT]] | SystemPromptFunc[AgentDepsT]
```


Decorator to register an instructions function.

Optionally takes [`RunContext`][pydantic_ai.tools.RunContext] as its only argument.
Can decorate a sync or async functions.

The decorator can be used bare (`agent.instructions`).

Overloads for every possible signature of `instructions` are included so the decorator doesn't obscure
the type of the function.

Example:
```python
from pydantic_ai import Agent, RunContext

agent = Agent('test', deps_type=str)

@agent.instructions
def simple_instructions() -> str:
    return 'foobar'

@agent.instructions
async def async_instructions(ctx: RunContext[str]) -> str:
    return f'{ctx.deps} is the best'
```

Args:
    func: The instructions function to register.
    name: An optional name for the instruction part this function produces, keyed as
        `'agent:<name>'` on [`InstructionPart.id`][pydantic_ai.messages.InstructionPart.id] so an
        application can address this part specifically, where the bare `'agent'` key addresses
        the agent's literal instructions. See [instruction parts](../agent.md#instruction-parts).

#### `system_prompt_parts`

```python
async def system_prompt_parts(self, *, deps: AgentDepsT=None, model: models.Model | models.KnownModelName | str | None=None, message_history: Sequence[_messages.ModelMessage] | None=None, prompt: str | Sequence[_messages.UserContent] | None=None, usage: _usage.RunUsage | None=None, model_settings: ModelSettings | None=None) -> list[_messages.SystemPromptPart]
```


Resolve the agent's configured system prompts into `SystemPromptPart`s.

See [`AbstractAgent.system_prompt_parts`][pydantic_ai.agent.AbstractAgent.system_prompt_parts].

#### `system_prompt`

```python
def system_prompt(self, func: SystemPromptFunc[AgentDepsT] | None=None, /, *, dynamic: bool=False) -> Callable[[SystemPromptFunc[AgentDepsT]], SystemPromptFunc[AgentDepsT]] | SystemPromptFunc[AgentDepsT]
```


Decorator to register a system prompt function.

Optionally takes [`RunContext`][pydantic_ai.tools.RunContext] as its only argument.
Can decorate a sync or async functions.

The decorator can be used either bare (`agent.system_prompt`) or as a function call
(`agent.system_prompt(...)`), see the examples below.

Overloads for every possible signature of `system_prompt` are included so the decorator doesn't obscure
the type of the function, see `tests/typed_agent.py` for tests.

Args:
    func: The function to decorate
    dynamic: If True, the system prompt will be reevaluated even when `messages_history` is provided,
        see [`SystemPromptPart.dynamic_ref`][pydantic_ai.messages.SystemPromptPart.dynamic_ref]

Example:
```python
from pydantic_ai import Agent, RunContext

agent = Agent('test', deps_type=str)

@agent.system_prompt
def simple_system_prompt() -> str:
    return 'foobar'

@agent.system_prompt(dynamic=True)
async def async_system_prompt(ctx: RunContext[str]) -> str:
    return f'{ctx.deps} is the best'
```

#### `output_validator`

```python
def output_validator(self, func: _output.OutputValidatorFunc[AgentDepsT, OutputDataT], /) -> _output.OutputValidatorFunc[AgentDepsT, OutputDataT]
```


Decorator to register an output validator function.

Optionally takes [`RunContext`][pydantic_ai.tools.RunContext] as its first argument.
Can decorate a sync or async functions.

Overloads for every possible signature of `output_validator` are included so the decorator doesn't obscure
the type of the function, see `tests/typed_agent.py` for tests.

Example:
```python
from pydantic_ai import Agent, ModelRetry, RunContext

agent = Agent('test', deps_type=str)

@agent.output_validator
def output_validator_simple(data: str) -> str:
    if 'wrong' in data:
        raise ModelRetry('wrong response')
    return data

@agent.output_validator
async def output_validator_deps(ctx: RunContext[str], data: str) -> str:
    if ctx.deps in data:
        raise ModelRetry('wrong response')
    return data

result = agent.run_sync('foobar', deps='spam')
print(result.output)
#> success (no tool calls)
```

#### `on_event`

```python
def on_event(self, func_or_event_type: OnEventHookFunc[_messages.AgentStreamEvent] | type[EventT] | None=None, *event_types: type[EventT], timeout: float | None=None) -> Any
```


Decorator to register a listener for events on this agent's run event stream.

Every event on the stream can be listened for: the framework's own model and tool events,
the application's [`CustomEvent`][pydantic_ai.messages.CustomEvent]s, and the
[`CapabilityEvent`][pydantic_ai.messages.CapabilityEvent]s published by the agent's
capabilities. Naming event classes narrows the `event` argument to their union and lets
dispatch skip the agent's listeners for anything else; a bare `@agent.on_event` sees every
[`AgentStreamEvent`][pydantic_ai.messages.AgentStreamEvent].

This is the application-level counterpart to
[`@on_event`][pydantic_ai.capabilities.on_event] on a capability, and it dispatches at the
same point. These listeners join after the agent's own capabilities, so they see the events
those emitted, and they survive an overridden root capability. Capability ordering still
applies: one asking for `position='innermost'` keeps that position and its listeners run
after these.

Dispatch happens *upstream* of
[`wrap_run_event_stream()`][pydantic_ai.capabilities.AbstractCapability.wrap_run_event_stream],
so a listener sees each event as it was emitted, not as it is finally delivered. A
capability that rewrites, replaces or drops events in its stream wrapper does so after
every listener has already run, which means a listener can see an event that no stream
consumer ever receives. To act on the delivered stream instead, wrap it yourself with
`wrap_run_event_stream` on a [`Hooks`][pydantic_ai.capabilities.Hooks] capability, or
consume [`run_stream_events()`][pydantic_ai.agent.AbstractAgent.run_stream_events].

Being application code, a listener may emit a `CustomEvent` of its own. That is how a
capability's internal event reaches a frontend: capability events are deliberately not
forwarded by the [AG-UI](../ui/ag-ui.md) and [Vercel AI](../ui/vercel-ai.md) adapters, so
you republish the part of one that is public.

For hook families other than events, pass a [`Hooks`][pydantic_ai.capabilities.Hooks]
capability to `capabilities=`, where its position among the other capabilities — which
decides where it sits in each wrap chain — is yours to choose.

Example:
```python
from dataclasses import dataclass

from pydantic_ai import Agent, CapabilityEvent, CustomEvent, RunContext

agent = Agent('test')


@dataclass(kw_only=True)
class IndexRebuiltEvent(CapabilityEvent, namespace='indexer'):
    documents: int


@dataclass(kw_only=True)
class SearchReadyEvent(CustomEvent):
    documents: int


@agent.on_event(IndexRebuiltEvent)
async def republish(ctx: RunContext, event: IndexRebuiltEvent) -> None:
    await ctx.emit(SearchReadyEvent(documents=event.documents))
```

#### `tool`

```python
def tool(self, func: ToolFuncContext[AgentDepsT, ToolParams] | None=None, /, *, name: str | None=None, description: str | None=None, retries: int | None=None, prepare: ToolPrepareFunc[AgentDepsT] | None=None, args_validator: ArgsValidatorFunc[AgentDepsT, ToolParams] | None=None, docstring_format: DocstringFormat='auto', require_parameter_descriptions: bool=False, schema_generator: type[GenerateJsonSchema]=GenerateToolJsonSchema, strict: bool | None=None, sequential: bool=False, requires_approval: bool=False, metadata: dict[str, Any] | None=None, timeout: float | None=None, defer_loading: bool=False, include_return_schema: bool | None=None) -> Any
```


Decorator to register a tool function which takes [`RunContext`][pydantic_ai.tools.RunContext] as its first argument.

Can decorate a sync or async functions.

The docstring is inspected to extract both the tool description and description of each parameter,
[learn more](../tools.md#function-tools-and-schema).

We can't add overloads for every possible signature of tool, since the return type is a recursive union
so the signature of functions decorated with `@agent.tool` is obscured.

Example:
```python
from pydantic_ai import Agent, RunContext

agent = Agent('test', deps_type=int)

@agent.tool
def foobar(ctx: RunContext[int], x: int) -> int:
    return ctx.deps + x

@agent.tool(retries=2)
async def spam(ctx: RunContext[int], y: float) -> float:
    return ctx.deps + y

result = agent.run_sync('foobar', deps=1)
print(result.output)
#> {"foobar":1,"spam":1.0}
```

Args:
    func: The tool function to register.
    name: The name of the tool, defaults to the function name.
    description: The description of the tool, defaults to the function docstring.
    retries: The number of retries to allow for this tool, defaults to the agent's default retries,
        which defaults to 1.
    prepare: custom method to prepare the tool definition for each step, return `None` to omit this
        tool from a given step. This is useful if you want to customise a tool at call time,
        or omit it completely from a step. See [`ToolPrepareFunc`][pydantic_ai.tools.ToolPrepareFunc].
    args_validator: custom method to validate tool arguments after schema validation has passed,
        before execution. The validator receives the already-validated and type-converted parameters,
        with `RunContext` as the first argument.
        Raise [`ModelRetry`][pydantic_ai.exceptions.ModelRetry] to ask the model to correct the
        arguments and try again, or [`ToolFailed`][pydantic_ai.exceptions.ToolFailed] to report a
        terminal failure the model should adapt to instead of retrying. Return `None` on success.
        See [`ArgsValidatorFunc`][pydantic_ai.tools.ArgsValidatorFunc].
    docstring_format: The format of the docstring, see [`DocstringFormat`][pydantic_ai.tools.DocstringFormat].
        Defaults to `'auto'`, such that the format is inferred from the structure of the docstring.
    require_parameter_descriptions: If True, raise an error if a parameter description is missing. Defaults to False.
    schema_generator: The JSON schema generator class to use for this tool. Defaults to `GenerateToolJsonSchema`.
    strict: Whether to enforce (vendor-specific) strict schema adherence for tool calls (supported by OpenAI, Anthropic, Google, and Bedrock).
        See [`ToolDefinition`][pydantic_ai.tools.ToolDefinition] for more info.
    sequential: Whether this tool acts as a barrier that runs alone, not overlapping with other tool calls.
        See [`ToolDefinition`][pydantic_ai.tools.ToolDefinition] for more info. Defaults to False.
    requires_approval: Whether this tool requires human-in-the-loop approval. Defaults to False.
        See the [tools documentation](../deferred-tools.md#human-in-the-loop-tool-approval) for more info.
    metadata: Optional metadata for the tool. This is not sent to the model but can be used for filtering and tool behavior customization.
    timeout: Timeout in seconds for tool execution. If the tool takes longer, a retry prompt is returned to the model.
        Overrides the agent-level `tool_timeout` if set. Defaults to None (no timeout).
    defer_loading: Whether to hide this tool until it's revealed by tool search, `load_capability`,
        or another tool's `ToolReturn.tools`. Defaults to False.
        See [Tool Search](../tools-advanced.md#tool-search) for more info.
    include_return_schema: Whether to include the return schema in the tool definition sent to the model.
        If `None`, defaults to `False` unless the [`IncludeToolReturnSchemas`][pydantic_ai.capabilities.IncludeToolReturnSchemas] capability is used.

#### `tool_plain`

```python
def tool_plain(self, func: ToolFuncPlain[ToolParams] | None=None, /, *, name: str | None=None, description: str | None=None, retries: int | None=None, prepare: ToolPrepareFunc[AgentDepsT] | None=None, args_validator: ArgsValidatorFunc[AgentDepsT, ToolParams] | None=None, docstring_format: DocstringFormat='auto', require_parameter_descriptions: bool=False, schema_generator: type[GenerateJsonSchema]=GenerateToolJsonSchema, strict: bool | None=None, sequential: bool=False, requires_approval: bool=False, metadata: dict[str, Any] | None=None, timeout: float | None=None, defer_loading: bool=False, include_return_schema: bool | None=None) -> Any
```


Decorator to register a tool function which DOES NOT take `RunContext` as an argument.

Can decorate a sync or async functions.

The docstring is inspected to extract both the tool description and description of each parameter,
[learn more](../tools.md#function-tools-and-schema).

We can't add overloads for every possible signature of tool, since the return type is a recursive union
so the signature of functions decorated with `@agent.tool` is obscured.

Example:
```python
from pydantic_ai import Agent

agent = Agent('test')

@agent.tool_plain
def foobar() -> int:
    return 123

@agent.tool_plain(retries=2)
async def spam() -> float:
    return 3.14

result = agent.run_sync('foobar')
print(result.output)
#> {"foobar":123,"spam":3.14}
```

Args:
    func: The tool function to register.
    name: The name of the tool, defaults to the function name.
    description: The description of the tool, defaults to the function docstring.
    retries: The number of retries to allow for this tool, defaults to the agent's default retries,
        which defaults to 1.
    prepare: custom method to prepare the tool definition for each step, return `None` to omit this
        tool from a given step. This is useful if you want to customise a tool at call time,
        or omit it completely from a step. See [`ToolPrepareFunc`][pydantic_ai.tools.ToolPrepareFunc].
    args_validator: custom method to validate tool arguments after schema validation has passed,
        before execution. The validator receives the already-validated and type-converted parameters,
        with [`RunContext`][pydantic_ai.tools.RunContext] as the first argument — even though the
        tool function itself does not take `RunContext` when using `tool_plain`.
        Raise [`ModelRetry`][pydantic_ai.exceptions.ModelRetry] to ask the model to correct the
        arguments and try again, or [`ToolFailed`][pydantic_ai.exceptions.ToolFailed] to report a
        terminal failure the model should adapt to instead of retrying. Return `None` on success.
        See [`ArgsValidatorFunc`][pydantic_ai.tools.ArgsValidatorFunc].
    docstring_format: The format of the docstring, see [`DocstringFormat`][pydantic_ai.tools.DocstringFormat].
        Defaults to `'auto'`, such that the format is inferred from the structure of the docstring.
    require_parameter_descriptions: If True, raise an error if a parameter description is missing. Defaults to False.
    schema_generator: The JSON schema generator class to use for this tool. Defaults to `GenerateToolJsonSchema`.
    strict: Whether to enforce (vendor-specific) strict schema adherence for tool calls (supported by OpenAI, Anthropic, Google, and Bedrock).
        See [`ToolDefinition`][pydantic_ai.tools.ToolDefinition] for more info.
    sequential: Whether this tool acts as a barrier that runs alone, not overlapping with other tool calls.
        See [`ToolDefinition`][pydantic_ai.tools.ToolDefinition] for more info. Defaults to False.
    requires_approval: Whether this tool requires human-in-the-loop approval. Defaults to False.
        See the [tools documentation](../deferred-tools.md#human-in-the-loop-tool-approval) for more info.
    metadata: Optional metadata for the tool. This is not sent to the model but can be used for filtering and tool behavior customization.
    timeout: Timeout in seconds for tool execution. If the tool takes longer, a retry prompt is returned to the model.
        Overrides the agent-level `tool_timeout` if set. Defaults to None (no timeout).
    defer_loading: Whether to hide this tool until it's revealed by tool search, `load_capability`,
        or another tool's `ToolReturn.tools`. Defaults to False.
        See [Tool Search](../tools-advanced.md#tool-search) for more info.
    include_return_schema: Whether to include the return schema in the tool definition sent to the model.
        If `None`, defaults to `False` unless the [`IncludeToolReturnSchemas`][pydantic_ai.capabilities.IncludeToolReturnSchemas] capability is used.

#### `toolset`

```python
def toolset(self, func: ToolsetFunc[AgentDepsT] | None=None, /, *, per_run_step: bool=True, id: str | None=None) -> Any
```


Decorator to register a toolset function which takes [`RunContext`][pydantic_ai.tools.RunContext] as its only argument.

Can decorate a sync or async functions.

The decorator can be used bare (`agent.toolset`).

Example:
```python
from pydantic_ai import AbstractToolset, Agent, FunctionToolset, RunContext

agent = Agent('test', deps_type=str)

@agent.toolset
async def simple_toolset(ctx: RunContext[str]) -> AbstractToolset[str]:
    return FunctionToolset()
```

Args:
    func: The toolset function to register.
    per_run_step: Whether to re-evaluate the toolset for each run step. Defaults to True.
    id: An optional unique ID for the dynamic toolset. Under durable execution, construct a
        [`DynamicToolset`][pydantic_ai.toolsets.DynamicToolset] with this ID and pass it to
        `Agent(toolsets=[...])` instead; decorator registrations cannot be used inside a
        workflow or flow because they happen after durable units are created.































#### `root_capability`

```python
def root_capability(self) -> CombinedCapability[AgentDepsT]
```


The root capability of the agent, containing all registered capabilities.

#### `toolsets`

```python
def toolsets(self) -> Sequence[AbstractToolset[AgentDepsT]]
```


All toolsets registered on the agent, including a function toolset holding tools that were registered on the agent directly.

Output tools are not included.











#### `set_mcp_sampling_model`

```python
def set_mcp_sampling_model(self, model: models.Model | models.KnownModelName | str | None=None) -> None
```


Set the sampling model on all [`MCPToolset`s][pydantic_ai.mcp.MCPToolset] registered with the agent.

If no sampling model is provided, the agent's model will be used.

#### `to_web`

```python
def to_web(self, *, models: ModelsParam=None, deps: AgentDepsT=None, model_settings: ModelSettings | None=None, instructions: str | None=None, html_source: str | Path | None=None, allowed_hosts: Sequence[str] | None=None) -> Starlette
```


Create a Starlette app that serves a web chat UI for this agent.

This method returns a pre-configured Starlette application that provides a web-based
chat interface for interacting with the agent. By default, the UI is fetched from a
CDN and cached on first use.

The returned Starlette application can be mounted into a FastAPI app or run directly
with any ASGI server (uvicorn, hypercorn, etc.).

Note that the `deps` and `model_settings` will be the same for each request.
To provide different `deps` for each request use the lower-level adapters directly.

The agent's configured native tools (registered via `capabilities=[NativeTool(...)]`
or higher-level capabilities like `WebSearch()`) are automatically exposed as
options in the UI.

Args:
    models: Additional models to make available in the UI. Can be:
        - A sequence of model names/instances (e.g., `['openai:gpt-5', 'anthropic:claude-sonnet-4-6']`)
        - A dict mapping display labels to model names/instances
          (e.g., `{'GPT 5': 'openai:gpt-5', 'Claude': 'anthropic:claude-sonnet-4-6'}`)
        The agent's model is always included. Native tool support is automatically
        determined from each model's profile.
    deps: Optional dependencies to use for all requests.
    model_settings: Optional settings to use for all model requests.
    instructions: Optional extra instructions to pass to each agent run.
    html_source: Path or URL for the chat UI HTML. Can be:
        - None (default): Fetches from CDN and caches locally
        - A Path instance: Reads from the local file
        - A URL string (http:// or https://): Fetches from the URL
        - A file path string: Reads from the local file
    allowed_hosts: Additional hostnames to answer to, e.g. `['ui.example.com']` or
        `['*.example.com']` (subdomains only, so list the apex separately if you serve it).
        IP addresses and `localhost` are always allowed; any other `Host` header is refused
        with a `421`, so that a website cannot reach the UI on your machine by pointing a
        hostname it controls at you (DNS rebinding). Pass `['*']` to answer to any host,
        only if something in front of the app already authenticates requests.

Returns:
    A configured Starlette application ready to be served (e.g., with uvicorn)

Example:
    ```python
    from pydantic_ai import Agent
    from pydantic_ai.capabilities import NativeTool
    from pydantic_ai.native_tools import WebSearchTool

    agent = Agent('openai:gpt-5', capabilities=[NativeTool(WebSearchTool())])

    # Simple usage - uses agent's model and native tools
    app = agent.to_web()

    # Or provide additional models for UI selection
    app = agent.to_web(models=['openai:gpt-5', 'anthropic:claude-sonnet-4-6'])

    # Then run with: uvicorn app:app --reload
    ```









































## `CancellationToken`

```python
class CancellationToken
```


A thread-safe handle for cancelling one or more agent runs.

A token is permanently cancelled after [`cancel`][pydantic_ai.CancellationToken.cancel] is
called. The same token may be passed to multiple concurrent runs, in which case all of them
are cancelled.

### `cancelled`

```python
def cancelled(self) -> bool
```


Whether cancellation has been requested.

### `cancel`

```python
def cancel(self) -> None
```


Cancel every live run registered with this token.

This method is idempotent and may be called from any thread.