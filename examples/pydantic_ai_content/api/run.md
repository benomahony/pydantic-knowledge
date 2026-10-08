# `pydantic_ai.run`





### `AgentRun`

```python
class AgentRun
```


A stateful, async-iterable run of an [`Agent`][pydantic_ai.agent.Agent].

You generally obtain an `AgentRun` instance by calling `async with my_agent.iter(...) as agent_run:`.

Once you have an instance, you can use it to iterate through the run's nodes as they execute. When an
[`End`][pydantic_graph.basenode.End] is reached, the run finishes and [`result`][pydantic_ai.agent.AgentRun.result]
becomes available.

Example:
```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-5.2')

async def main():
    nodes = []
    # Iterate through the run, recording each node along the way:
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

You can also manually drive the iteration using the [`next`][pydantic_ai.agent.AgentRun.next] method for
more granular control.

```python
_graph_run: GraphRun[_agent_graph.GraphAgentState, _agent_graph.GraphAgentDeps[AgentDepsT, Any], FinalResult[OutputDataT]]
```

```python
_result_override: AgentRunResult[OutputDataT] | None = dataclasses.field(default=None, repr=False, init=False)
```

```python
_node_error: BaseException | None = dataclasses.field(default=None, repr=False, init=False)
```

```python
_last_yielded_node: _agent_graph.AgentNode[AgentDepsT, OutputDataT] | End[FinalResult[OutputDataT]] | None = dataclasses.field(default=None, repr=False, init=False)
```

#### `ctx`

```python
def ctx(self) -> GraphRunContext[_agent_graph.GraphAgentState, _agent_graph.GraphAgentDeps[AgentDepsT, Any]]
```


The current context of the agent run.

#### `next_node`

```python
def next_node(self) -> _agent_graph.AgentNode[AgentDepsT, OutputDataT] | End[FinalResult[OutputDataT]]
```


The next node that will be run in the agent graph.

This is the next node that will be used during async iteration, or if a node is not passed to `self.next(...)`.

#### `result`

```python
def result(self) -> AgentRunResult[OutputDataT] | None
```


The final result of the run if it has ended, otherwise `None`.

Once the run returns an [`End`][pydantic_graph.basenode.End] node, `result` is populated
with an [`AgentRunResult`][pydantic_ai.agent.AgentRunResult].

#### `all_messages`

```python
def all_messages(self) -> list[_messages.ModelMessage]
```


Return all messages for the run so far.

Messages from older runs are included.

#### `all_messages_json`

```python
def all_messages_json(self, *, output_tool_return_content: str | None=None) -> bytes
```


Return all messages from [`all_messages`][pydantic_ai.agent.AgentRun.all_messages] as JSON bytes.

Returns:
    JSON bytes representing the messages.

#### `new_messages`

```python
def new_messages(self) -> list[_messages.ModelMessage]
```


Return the messages produced during this run so far.

Messages provided via `message_history` and messages from older runs are excluded.

#### `new_messages_json`

```python
def new_messages_json(self) -> bytes
```


Return new messages from [`new_messages`][pydantic_ai.agent.AgentRun.new_messages] as JSON bytes.

Returns:
    JSON bytes representing the new messages.

















#### `next`

```python
async def next(self, node: _agent_graph.AgentNode[AgentDepsT, OutputDataT]) -> _agent_graph.AgentNode[AgentDepsT, OutputDataT] | End[FinalResult[OutputDataT]]
```


Manually drive the agent run by passing in the node you want to run next.

This lets you inspect or mutate the node before continuing execution, or skip certain nodes
under dynamic conditions. The agent run should be stopped when you return an [`End`][pydantic_graph.basenode.End]
node.

Example:
```python
from pydantic_ai import Agent
from pydantic_graph import End

agent = Agent('openai:gpt-5.2')

async def main():
    async with agent.iter('What is the capital of France?') as agent_run:
        next_node = agent_run.next_node  # start with the first node
        nodes = [next_node]
        while not isinstance(next_node, End):
            next_node = await agent_run.next(next_node)
            nodes.append(next_node)
        # Once `next_node` is an End, we've finished:
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
        print('Final result:', agent_run.result.output)
        #> Final result: The capital of France is Paris.
```

Args:
    node: The node to run next in the graph.

Returns:
    The next node returned by the graph logic, or an [`End`][pydantic_graph.basenode.End] node if
    the run has completed.



#### `usage`

```python
def usage(self) -> _usage.RunUsage
```


Get usage statistics for the run so far, including token usage, model requests, and so on.

#### `metadata`

```python
def metadata(self) -> dict[str, Any] | None
```


Metadata associated with this agent run, if configured.

#### `run_id`

```python
def run_id(self) -> str
```


The unique identifier for the agent run.

#### `conversation_id`

```python
def conversation_id(self) -> str
```


The unique identifier for the conversation this run belongs to.

#### `pending_messages`

```python
def pending_messages(self) -> list[PendingMessage]
```


Internal: live view of the queue mutated by `enqueue` and drained by the internal `PendingMessageDrainCapability`.

Exposed for inspection / debugging; use [`enqueue`][pydantic_ai.run.AgentRun.enqueue] to add messages.

#### `emit`

```python
async def emit(self, event: CustomEventT, /) -> CustomEventT
```


Emit a [`CustomEvent`][pydantic_ai.messages.CustomEvent] into this run's event stream.

Lets code driving [`Agent.iter`][pydantic_ai.agent.AbstractAgent.iter] inject application-defined
events (e.g. from an external harness or event bus) into the stream, alongside events emitted from
tools via [`RunContext.emit`][pydantic_ai.tools.RunContext.emit].
The event surfaces on the next pull from the run's node stream.

Designed to be called from the same event loop driving `agent.iter()`. If you're forwarding events
from a different thread, submit the coroutine to the agent's loop
(e.g. `asyncio.run_coroutine_threadsafe(agent_run.emit(event), loop)`).

Args:
    event: The [`CustomEvent`][pydantic_ai.messages.CustomEvent] to emit.

Returns:
    The event as emitted.

Raises:
    UserError: If the run has already ended (no stream remains to deliver the event), or if
        passed a [`CapabilityEvent`][pydantic_ai.messages.CapabilityEvent]: those belong
        to capabilities, and code driving the run is application code.

#### `enqueue`

```python
def enqueue(self, *content: EnqueueContent, priority: PendingMessagePriority='asap') -> str | None
```


Enqueue content to be injected into the conversation.

Safe to call directly from synchronous or asynchronous code, including
a callback running in another thread.

Args:
    *content: One or more [`EnqueueContent`][pydantic_ai.run.EnqueueContent] items.
        Adjacent [`UserContent`][pydantic_ai.messages.UserContent] (a `str` or multi-modal
        content like an [`ImageUrl`][pydantic_ai.messages.ImageUrl]) is gathered into one
        [`UserPromptPart`][pydantic_ai.messages.UserPromptPart], and each
        [`ModelRequestPart`][pydantic_ai.messages.ModelRequestPart] (e.g. a
        [`SystemPromptPart`][pydantic_ai.messages.SystemPromptPart]) is coalesced with adjacent
        part-style items into one [`ModelRequest`][pydantic_ai.messages.ModelRequest]; a complete
        [`ModelRequest`][pydantic_ai.messages.ModelRequest] or
        [`ModelResponse`][pydantic_ai.messages.ModelResponse] is kept as its own message. The
        assembled sequence must end in a request. Calling with no positional args is a no-op.
    priority: When to deliver:
        `'asap'` (default) — at the earliest opportunity (next model request,
            or a redirect if the agent would otherwise end).
        `'when_idle'` — only when the agent would otherwise end, after `'asap'` messages.

Returns:
    The `enqueue_id` of the queued message, echoed on the
    [`EnqueuedMessagesEvent`][pydantic_ai.messages.EnqueuedMessagesEvent] emitted when it's
    delivered, or `None` when there was nothing to enqueue (an empty call).

Raises:
    UserError: If the run has ended, since there'd be nowhere to deliver the message.

#### `cancel`

```python
def cancel(self) -> None
```


Cancel the whole agent run.

The run stops what it is doing — the in-flight model request is torn down, in-flight tool
tasks are cancelled and drained, a suspended server-side job is best-effort cancelled — and
the code driving the run sees `asyncio.CancelledError`. When the `agent.iter()` context
exits, this becomes [`RunCancelled`][pydantic_ai.exceptions.RunCancelled] (including for
`agent.run()`, which wraps `iter()`). Everything that completed before the cancellation took
effect is preserved in message history.
[`RunCancelled.all_messages()`][pydantic_ai.exceptions.RunCancelled.all_messages] returns a
complete snapshot that can be passed to a new run as `message_history` to resume the
conversation.

Cancellation is terminal: capability hooks (`wrap_run`, `wrap_node_run`, `on_run_error`)
may observe it and clean up, but cannot recover the run into a successful result.

Unlike [`StreamedRunResult.cancel()`][pydantic_ai.result.StreamedRunResult.cancel], which
only stops the current model response and lets the run continue, this ends the run itself.

Safe to call from another task or thread (e.g. a TUI's key handler while the run is
awaited elsewhere). Idempotent; a no-op once the run has finished — where "finished" means
the `agent.iter()`/`agent.run()` context has exited. A `cancel()` issued inside the context
after the run has already produced its result (e.g. after iterating to `End`) is still
honored and surfaces as `RunCancelled` on exit, so that a hook running at context exit (like
`after_run`) can still cancel the run; only after the context has exited is `cancel()` a true
no-op. Externally cancelling the task running the agent (`asyncio.Task.cancel()`) remains
supported and keeps raising `asyncio.CancelledError` instead; when both happen, the external
cancellation wins.

### `AgentRunResult`

```python
class AgentRunResult
```


The final result of an agent run.

```python
output: OutputDataT
```

```python
_output_tool_name: str | None = dataclasses.field(repr=False, compare=False, default=None)
```

```python
_state: _agent_graph.GraphAgentState = dataclasses.field(repr=False, compare=False, default_factory=_agent_graph.GraphAgentState)
```

```python
_new_message_index: int = dataclasses.field(repr=False, compare=False, default=0)
```

```python
_traceparent_value: str | None = dataclasses.field(repr=False, compare=False, default=None)
```

#### `workspace`

```python
def workspace(self) -> Workspace
```


The [`Workspace`][pydantic_ai.workspaces.Workspace] the run used, still usable after it.

Pass it as `workspace=` to continue in it. A result not produced by a run has a placeholder.





#### `all_messages`

```python
def all_messages(self, *, output_tool_return_content: str | None=None) -> list[_messages.ModelMessage]
```


Return the history of _messages.

Args:
    output_tool_return_content: The return content of the tool call to set in the last message.
        This provides a convenient way to modify the content of the output tool call if you want to continue
        the conversation and want to set the response to the output tool call. If `None`, the last message will
        not be modified.

Returns:
    List of messages.

#### `all_messages_json`

```python
def all_messages_json(self, *, output_tool_return_content: str | None=None) -> bytes
```


Return all messages from [`all_messages`][pydantic_ai.agent.AgentRunResult.all_messages] as JSON bytes.

Args:
    output_tool_return_content: The return content of the tool call to set in the last message.
        This provides a convenient way to modify the content of the output tool call if you want to continue
        the conversation and want to set the response to the output tool call. If `None`, the last message will
        not be modified.

Returns:
    JSON bytes representing the messages.

#### `new_messages`

```python
def new_messages(self, *, output_tool_return_content: str | None=None) -> list[_messages.ModelMessage]
```


Return the messages produced during this run.

Messages provided via `message_history` and messages from older runs are excluded.

Args:
    output_tool_return_content: The return content of the tool call to set in the last message.
        This provides a convenient way to modify the content of the output tool call if you want to continue
        the conversation and want to set the response to the output tool call. If `None`, the last message will
        not be modified.

Returns:
    List of new messages.

#### `new_messages_json`

```python
def new_messages_json(self, *, output_tool_return_content: str | None=None) -> bytes
```


Return new messages from [`new_messages`][pydantic_ai.agent.AgentRunResult.new_messages] as JSON bytes.

Args:
    output_tool_return_content: The return content of the tool call to set in the last message.
        This provides a convenient way to modify the content of the output tool call if you want to continue
        the conversation and want to set the response to the output tool call. If `None`, the last message will
        not be modified.

Returns:
    JSON bytes representing the new messages.

#### `response`

```python
def response(self) -> _messages.ModelResponse
```


Return the last response from the message history.

#### `usage`

```python
def usage(self) -> _usage.RunUsage
```


Return the usage of the whole run.

#### `timestamp`

```python
def timestamp(self) -> datetime
```


Return the timestamp of last response.

#### `metadata`

```python
def metadata(self) -> dict[str, Any] | None
```


Metadata associated with this agent run, if configured.

#### `run_id`

```python
def run_id(self) -> str
```


The unique identifier for the agent run.

#### `conversation_id`

```python
def conversation_id(self) -> str
```


The unique identifier for the conversation this run belongs to.

### `AgentRunResultEvent`

```python
class AgentRunResultEvent
```


An event indicating the agent run ended and containing the final result of the agent run.

```python
result: AgentRunResult[OutputDataT]
```

```python
_: dataclasses.KW_ONLY
```

```python
event_kind: Literal['agent_run_result'] = 'agent_run_result'
``````python
EnqueueContent: TypeAlias = 'UserContent | ModelRequestPart | ModelMessage'
```## `PendingMessage`

```python
class PendingMessage
```


One or more [`ModelMessage`][pydantic_ai.messages.ModelMessage]s queued for injection into the agent conversation.

Enqueued via [`RunContext.enqueue`][pydantic_ai.tools.RunContext.enqueue] or
[`AgentRun.enqueue`][pydantic_ai.run.AgentRun.enqueue] and automatically drained
at the appropriate time during the agent run by the internal `PendingMessageDrainCapability`.

```python
messages: list[ModelMessage]
```

```python
priority: PendingMessagePriority = 'asap'
```

```python
enqueue_id: str = field(default_factory=lambda: str(uuid7()))
```

### `from_content`

```python
def from_content(cls, *content: EnqueueContent, priority: PendingMessagePriority='asap') -> PendingMessage | None
```


Build a `PendingMessage` from `enqueue` arguments, or `None` when there's nothing to send.

Returns `None` for an empty call (enqueueing nothing is a no-op rather than an error).

Raises:
    UserError: If the assembled messages don't end in a
        [`ModelRequest`][pydantic_ai.messages.ModelRequest] — e.g. a lone `ModelResponse` —
        since the agent needs a request to respond to.```python
PendingMessagePriority: TypeAlias = Literal['asap', 'when_idle']
```