# `pydantic_ai.ui.vercel_ai`

Vercel AI protocol adapter for Pydantic AI agents.

This module provides classes for integrating Pydantic AI agents with the Vercel AI protocol,
enabling streaming event-based communication for interactive AI applications.

Converted to Python from:
https://github.com/vercel/ai/blob/ai%405.0.34/packages/ai/src/ui/ui-messages.tsVercel AI request types (UI messages).

Converted to Python from:
https://github.com/vercel/ai/blob/ai%406.0.57/packages/ai/src/ui/ui-messages.ts

Tool approval types (`ToolApprovalRequested`, `ToolApprovalResponded`) require AI SDK v6 or later.

### `BaseUIPart`

```python
class BaseUIPart
```


Abstract base class for all UI parts.

### `TextUIPart`

```python
class TextUIPart
```


A text part of a message.

```python
type: Literal['text'] = 'text'
```

```python
text: str
```

```python
state: Literal['streaming', 'done'] | None = None
```

```python
provider_metadata: ProviderMetadata | None = None
```

### `ReasoningUIPart`

```python
class ReasoningUIPart
```


A reasoning part of a message.

```python
type: Literal['reasoning'] = 'reasoning'
```

```python
id: str | None = Field(default=None, exclude_if=lambda value: value is None)
```

```python
text: str
```

```python
state: Literal['streaming', 'done'] | None = None
```

```python
provider_metadata: ProviderMetadata | None = None
```

### `SourceUrlUIPart`

```python
class SourceUrlUIPart
```


A source part of a message.

```python
type: Literal['source-url'] = 'source-url'
```

```python
source_id: str
```

```python
url: str
```

```python
title: str | None = None
```

```python
provider_metadata: ProviderMetadata | None = None
```

### `SourceDocumentUIPart`

```python
class SourceDocumentUIPart
```


A document source part of a message.

```python
type: Literal['source-document'] = 'source-document'
```

```python
source_id: str
```

```python
media_type: str
```

```python
title: str
```

```python
filename: str | None = None
```

```python
provider_metadata: ProviderMetadata | None = None
```

### `FileUIPart`

```python
class FileUIPart
```


A file part of a message.

```python
type: Literal['file'] = 'file'
```

```python
media_type: str
```

```python
filename: str | None = None
```

```python
url: str
```

```python
provider_metadata: ProviderMetadata | None = None
```

### `StepStartUIPart`

```python
class StepStartUIPart
```


A step boundary part of a message.

```python
type: Literal['step-start'] = 'step-start'
```

### `DataUIPart`

```python
class DataUIPart
```


Data part with dynamic type based on data name.

```python
type: Annotated[str, Field(pattern='^data-')]
```

```python
id: str | None = None
```

```python
data: Any
```

### `ToolApprovalRequested`

```python
class ToolApprovalRequested
```


Tool approval in requested state (awaiting user response).

```python
id: str
```

### `ToolApprovalResponded`

```python
class ToolApprovalResponded
```


Tool approval in responded state (user has approved or denied).

```python
id: str
```

```python
approved: StrictBool
```

```python
reason: str | None = None
```

### `ToolInputStreamingPart`

```python
class ToolInputStreamingPart
```


Tool part in input-streaming state.

```python
type: Annotated[str, Field(pattern='^tool-')]
```

```python
tool_call_id: str
```

```python
title: str | None = None
```

```python
state: Literal['input-streaming'] = 'input-streaming'
```

```python
input: Any | None = None
```

```python
provider_executed: bool | None = None
```

```python
call_provider_metadata: ProviderMetadata | None = None
```

```python
approval: ToolApproval | None = None
```

### `ToolInputAvailablePart`

```python
class ToolInputAvailablePart
```


Tool part in input-available state.

```python
type: Annotated[str, Field(pattern='^tool-')]
```

```python
tool_call_id: str
```

```python
title: str | None = None
```

```python
state: Literal['input-available'] = 'input-available'
```

```python
input: Any | None = None
```

```python
provider_executed: bool | None = None
```

```python
call_provider_metadata: ProviderMetadata | None = None
```

```python
approval: ToolApproval | None = None
```

### `ToolOutputAvailablePart`

```python
class ToolOutputAvailablePart
```


Tool part in output-available state.

```python
type: Annotated[str, Field(pattern='^tool-')]
```

```python
tool_call_id: str
```

```python
title: str | None = None
```

```python
state: Literal['output-available'] = 'output-available'
```

```python
input: Any | None = None
```

```python
output: Any | None = None
```

```python
provider_executed: bool | None = None
```

```python
call_provider_metadata: ProviderMetadata | None = None
```

```python
preliminary: bool | None = None
```

```python
approval: ToolApproval | None = None
```

### `ToolOutputErrorPart`

```python
class ToolOutputErrorPart
```


Tool part in output-error state.

```python
type: Annotated[str, Field(pattern='^tool-')]
```

```python
tool_call_id: str
```

```python
title: str | None = None
```

```python
state: Literal['output-error'] = 'output-error'
```

```python
input: Any | None = None
```

```python
raw_input: Any | None = None
```

```python
error_text: str
```

```python
provider_executed: bool | None = None
```

```python
call_provider_metadata: ProviderMetadata | None = None
```

```python
approval: ToolApproval | None = None
```

### `ToolApprovalRequestedPart`

```python
class ToolApprovalRequestedPart
```


Tool part in approval-requested state (awaiting user decision).

```python
type: Annotated[str, Field(pattern='^tool-')]
```

```python
tool_call_id: str
```

```python
title: str | None = None
```

```python
state: Literal['approval-requested'] = 'approval-requested'
```

```python
input: Any | None = None
```

```python
provider_executed: bool | None = None
```

```python
call_provider_metadata: ProviderMetadata | None = None
```

```python
approval: ToolApproval | None = None
```

### `ToolApprovalRespondedPart`

```python
class ToolApprovalRespondedPart
```


Tool part in approval-responded state (user approved/denied, execution pending).

```python
type: Annotated[str, Field(pattern='^tool-')]
```

```python
tool_call_id: str
```

```python
title: str | None = None
```

```python
state: Literal['approval-responded'] = 'approval-responded'
```

```python
input: Any | None = None
```

```python
provider_executed: bool | None = None
```

```python
call_provider_metadata: ProviderMetadata | None = None
```

```python
approval: ToolApproval | None = None
```

### `ToolOutputDeniedPart`

```python
class ToolOutputDeniedPart
```


Tool part in output-denied state (tool was denied, terminal state).

```python
type: Annotated[str, Field(pattern='^tool-')]
```

```python
tool_call_id: str
```

```python
title: str | None = None
```

```python
state: Literal['output-denied'] = 'output-denied'
```

```python
input: Any | None = None
```

```python
provider_executed: bool | None = None
```

```python
call_provider_metadata: ProviderMetadata | None = None
```

```python
approval: ToolApproval | None = None
```

### `DynamicToolInputStreamingPart`

```python
class DynamicToolInputStreamingPart
```


Dynamic tool part in input-streaming state.

```python
type: Literal['dynamic-tool'] = 'dynamic-tool'
```

```python
tool_name: str
```

```python
tool_call_id: str
```

```python
title: str | None = None
```

```python
state: Literal['input-streaming'] = 'input-streaming'
```

```python
input: Any | None = None
```

```python
provider_executed: bool | None = None
```

```python
call_provider_metadata: ProviderMetadata | None = None
```

```python
approval: ToolApproval | None = None
```

### `DynamicToolInputAvailablePart`

```python
class DynamicToolInputAvailablePart
```


Dynamic tool part in input-available state.

```python
type: Literal['dynamic-tool'] = 'dynamic-tool'
```

```python
tool_name: str
```

```python
tool_call_id: str
```

```python
title: str | None = None
```

```python
state: Literal['input-available'] = 'input-available'
```

```python
input: Any
```

```python
provider_executed: bool | None = None
```

```python
call_provider_metadata: ProviderMetadata | None = None
```

```python
approval: ToolApproval | None = None
```

### `DynamicToolOutputAvailablePart`

```python
class DynamicToolOutputAvailablePart
```


Dynamic tool part in output-available state.

```python
type: Literal['dynamic-tool'] = 'dynamic-tool'
```

```python
tool_name: str
```

```python
tool_call_id: str
```

```python
title: str | None = None
```

```python
state: Literal['output-available'] = 'output-available'
```

```python
input: Any
```

```python
output: Any
```

```python
provider_executed: bool | None = None
```

```python
call_provider_metadata: ProviderMetadata | None = None
```

```python
preliminary: bool | None = None
```

```python
approval: ToolApproval | None = None
```

### `DynamicToolOutputErrorPart`

```python
class DynamicToolOutputErrorPart
```


Dynamic tool part in output-error state.

```python
type: Literal['dynamic-tool'] = 'dynamic-tool'
```

```python
tool_name: str
```

```python
tool_call_id: str
```

```python
title: str | None = None
```

```python
state: Literal['output-error'] = 'output-error'
```

```python
input: Any
```

```python
error_text: str
```

```python
provider_executed: bool | None = None
```

```python
call_provider_metadata: ProviderMetadata | None = None
```

```python
approval: ToolApproval | None = None
```

### `DynamicToolApprovalRequestedPart`

```python
class DynamicToolApprovalRequestedPart
```


Dynamic tool part in approval-requested state (awaiting user decision).

```python
type: Literal['dynamic-tool'] = 'dynamic-tool'
```

```python
tool_name: str
```

```python
tool_call_id: str
```

```python
title: str | None = None
```

```python
state: Literal['approval-requested'] = 'approval-requested'
```

```python
input: Any
```

```python
provider_executed: bool | None = None
```

```python
call_provider_metadata: ProviderMetadata | None = None
```

```python
approval: ToolApproval | None = None
```

### `DynamicToolApprovalRespondedPart`

```python
class DynamicToolApprovalRespondedPart
```


Dynamic tool part in approval-responded state (user approved/denied, execution pending).

```python
type: Literal['dynamic-tool'] = 'dynamic-tool'
```

```python
tool_name: str
```

```python
tool_call_id: str
```

```python
title: str | None = None
```

```python
state: Literal['approval-responded'] = 'approval-responded'
```

```python
input: Any
```

```python
provider_executed: bool | None = None
```

```python
call_provider_metadata: ProviderMetadata | None = None
```

```python
approval: ToolApproval | None = None
```

### `DynamicToolOutputDeniedPart`

```python
class DynamicToolOutputDeniedPart
```


Dynamic tool part in output-denied state (tool was denied, terminal state).

```python
type: Literal['dynamic-tool'] = 'dynamic-tool'
```

```python
tool_name: str
```

```python
tool_call_id: str
```

```python
title: str | None = None
```

```python
state: Literal['output-denied'] = 'output-denied'
```

```python
input: Any
```

```python
provider_executed: bool | None = None
```

```python
call_provider_metadata: ProviderMetadata | None = None
```

```python
approval: ToolApproval | None = None
```

### `UIMessage`

```python
class UIMessage
```


A message as displayed in the UI by Vercel AI Elements.

```python
id: str
```

```python
role: Literal['system', 'user', 'assistant']
```

```python
metadata: Any | None = None
```

```python
parts: list[UIMessagePart]
```

### `SubmitMessage`

```python
class SubmitMessage
```


Submit message request.

```python
trigger: Literal['submit-message'] = 'submit-message'
```

```python
id: str
```

```python
messages: list[UIMessage]
```

### `RegenerateMessage`

```python
class RegenerateMessage
```


Ask the agent to regenerate a message.

```python
trigger: Literal['regenerate-message']
```

```python
id: str
```

```python
messages: list[UIMessage]
```

```python
message_id: str | None = None
```Vercel AI response types (SSE chunks).

Converted to Python from:
https://github.com/vercel/ai/blob/ai%406.0.57/packages/ai/src/ui-message-stream/ui-message-chunks.ts

Tool approval types (`ToolApprovalRequestChunk`, `ToolOutputDeniedChunk`) require AI SDK UI v6 or later.

### `BaseChunk`

```python
class BaseChunk
```


Abstract base class for response SSE events.

### `TextStartChunk`

```python
class TextStartChunk
```


Text start chunk.

```python
type: Literal['text-start'] = 'text-start'
```

```python
id: str
```

```python
provider_metadata: ProviderMetadata | None = None
```

### `TextDeltaChunk`

```python
class TextDeltaChunk
```


Text delta chunk.

```python
type: Literal['text-delta'] = 'text-delta'
```

```python
delta: str
```

```python
id: str
```

```python
provider_metadata: ProviderMetadata | None = None
```

### `TextEndChunk`

```python
class TextEndChunk
```


Text end chunk.

```python
type: Literal['text-end'] = 'text-end'
```

```python
id: str
```

```python
provider_metadata: ProviderMetadata | None = None
```

### `ReasoningStartChunk`

```python
class ReasoningStartChunk
```


Reasoning start chunk.

```python
type: Literal['reasoning-start'] = 'reasoning-start'
```

```python
id: str
```

```python
provider_metadata: ProviderMetadata | None = None
```

### `ReasoningDeltaChunk`

```python
class ReasoningDeltaChunk
```


Reasoning delta chunk.

```python
type: Literal['reasoning-delta'] = 'reasoning-delta'
```

```python
id: str
```

```python
delta: str
```

```python
provider_metadata: ProviderMetadata | None = None
```

### `ReasoningEndChunk`

```python
class ReasoningEndChunk
```


Reasoning end chunk.

```python
type: Literal['reasoning-end'] = 'reasoning-end'
```

```python
id: str
```

```python
provider_metadata: ProviderMetadata | None = None
```

### `ErrorChunk`

```python
class ErrorChunk
```


Error chunk.

```python
type: Literal['error'] = 'error'
```

```python
error_text: str
```

### `ToolInputStartChunk`

```python
class ToolInputStartChunk
```


Tool input start chunk.

```python
type: Literal['tool-input-start'] = 'tool-input-start'
```

```python
tool_call_id: str
```

```python
tool_name: str
```

```python
provider_executed: bool | None = None
```

```python
provider_metadata: ProviderMetadata | None = None
```

```python
dynamic: bool | None = None
```

### `ToolInputDeltaChunk`

```python
class ToolInputDeltaChunk
```


Tool input delta chunk.

```python
type: Literal['tool-input-delta'] = 'tool-input-delta'
```

```python
tool_call_id: str
```

```python
input_text_delta: str
```

### `ToolOutputAvailableChunk`

```python
class ToolOutputAvailableChunk
```


Tool output available chunk.

```python
type: Literal['tool-output-available'] = 'tool-output-available'
```

```python
tool_call_id: str
```

```python
output: Any
```

```python
provider_executed: bool | None = None
```

```python
dynamic: bool | None = None
```

```python
preliminary: bool | None = None
```

### `ToolInputAvailableChunk`

```python
class ToolInputAvailableChunk
```


Tool input available chunk.

```python
type: Literal['tool-input-available'] = 'tool-input-available'
```

```python
tool_call_id: str
```

```python
tool_name: str
```

```python
input: Any
```

```python
provider_executed: bool | None = None
```

```python
provider_metadata: ProviderMetadata | None = None
```

```python
dynamic: bool | None = None
```

### `ToolInputErrorChunk`

```python
class ToolInputErrorChunk
```


Tool input error chunk.

Requires AI SDK UI v6 or later.

```python
type: Literal['tool-input-error'] = 'tool-input-error'
```

```python
tool_call_id: str
```

```python
tool_name: str
```

```python
input: Any
```

```python
provider_executed: bool | None = None
```

```python
provider_metadata: ProviderMetadata | None = None
```

```python
dynamic: bool | None = None
```

```python
error_text: str
```

### `ToolOutputErrorChunk`

```python
class ToolOutputErrorChunk
```


Tool output error chunk.

```python
type: Literal['tool-output-error'] = 'tool-output-error'
```

```python
tool_call_id: str
```

```python
error_text: str
```

```python
provider_executed: bool | None = None
```

```python
dynamic: bool | None = None
```

### `ToolApprovalRequestChunk`

```python
class ToolApprovalRequestChunk
```


Tool approval request chunk for human-in-the-loop approval.

Requires AI SDK UI v6 or later.

```python
type: Literal['tool-approval-request'] = 'tool-approval-request'
```

```python
approval_id: str
```

```python
tool_call_id: str
```

### `ToolOutputDeniedChunk`

```python
class ToolOutputDeniedChunk
```


Tool output denied chunk when user denies tool execution.

Requires AI SDK UI v6 or later.

```python
type: Literal['tool-output-denied'] = 'tool-output-denied'
```

```python
tool_call_id: str
```

### `SourceUrlChunk`

```python
class SourceUrlChunk
```


Source URL chunk.

```python
type: Literal['source-url'] = 'source-url'
```

```python
source_id: str
```

```python
url: str
```

```python
title: str | None = None
```

```python
provider_metadata: ProviderMetadata | None = None
```

### `SourceDocumentChunk`

```python
class SourceDocumentChunk
```


Source document chunk.

```python
type: Literal['source-document'] = 'source-document'
```

```python
source_id: str
```

```python
media_type: str
```

```python
title: str
```

```python
filename: str | None = None
```

```python
provider_metadata: ProviderMetadata | None = None
```

### `FileChunk`

```python
class FileChunk
```


File chunk.

```python
type: Literal['file'] = 'file'
```

```python
url: str
```

```python
media_type: str
```

### `DataChunk`

```python
class DataChunk
```


Data chunk with dynamic type.

```python
type: Annotated[str, Field(pattern='^data-')]
```

```python
id: str | None = None
```

```python
data: Any
```

```python
transient: bool | None = None
```

### `StartStepChunk`

```python
class StartStepChunk
```


Start step chunk.

```python
type: Literal['start-step'] = 'start-step'
```

### `FinishStepChunk`

```python
class FinishStepChunk
```


Finish step chunk.

```python
type: Literal['finish-step'] = 'finish-step'
```

### `StartChunk`

```python
class StartChunk
```


Start chunk.

```python
type: Literal['start'] = 'start'
```

```python
message_id: str | None = None
```

```python
message_metadata: Any | None = None
```

### `FinishChunk`

```python
class FinishChunk
```


Finish chunk.

```python
type: Literal['finish'] = 'finish'
```

```python
finish_reason: FinishReason = None
```

```python
message_metadata: Any | None = None
```

### `AbortChunk`

```python
class AbortChunk
```


Abort chunk.

```python
type: Literal['abort'] = 'abort'
```

```python
reason: str | None = None
```

### `MessageMetadataChunk`

```python
class MessageMetadataChunk
```


Message metadata chunk.

```python
type: Literal['message-metadata'] = 'message-metadata'
```

```python
message_metadata: Any
```

### `DoneChunk`

```python
class DoneChunk
```


Done chunk.

```python
type: Literal['done'] = 'done'
```