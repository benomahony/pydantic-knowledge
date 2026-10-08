# `pydantic_ai.profiles`

### `ModelProfile`

```python
class ModelProfile
```


Describes how requests to and responses from specific models or families of models need to be constructed and processed to get the best results, independent of the model and provider classes used.

All fields are optional; absent keys mean "use the documented default" (defaults are documented per field below and applied at access sites).

Subclasses (`OpenAIModelProfile`, `AnthropicModelProfile`, ...) add provider-specific keys; cross-class merging via dict-spread is supported.

```python
supports_tools: bool
```

```python
supports_text_output: bool
```

```python
supports_tool_return_schema: bool
```

```python
supports_json_schema_output: bool
```

```python
supports_json_object_output: bool
```

```python
supports_image_output: bool
```

```python
supports_audio_input: bool
```

```python
supports_inline_system_prompts: bool
```

```python
default_structured_output_mode: StructuredOutputMode
```

```python
prompted_output_template: str
```

```python
native_output_requires_schema_in_instructions: bool
```

```python
json_schema_transformer: type[JsonSchemaTransformer] | None
```

```python
default_cache_retention: timedelta | None
```

```python
supports_thinking: bool
```

```python
thinking_always_enabled: bool
```

```python
thinking_enabled_by_default: bool
```

```python
supports_forced_tool_choice: bool
```

```python
supports_forced_tool_choice_with_thinking: bool
```

```python
forced_tool_choice_disables_thinking: bool
```

```python
thinking_tags: tuple[str, str]
```

```python
ignore_streamed_leading_whitespace: bool
```

```python
supported_native_tools: frozenset[type[AbstractNativeTool]]
```

```python
context_window: int | None
```

```python
tool_deferral_mode: ToolDeferralMode | None
```

```python
tool_addition_mode: ToolAdditionMode | None
```

```python
tool_additions: ToolAdditionMode | None
```

```python
deferred_tools_require_tool_search: bool
```



### `merge_profile`

```python
def merge_profile(base: ModelProfile | None, *overrides: ModelProfile | None) -> ModelProfile
```


Merge profiles via dict-spread. Later arguments override earlier ones; `None` is treated as empty.

This is the canonical way to layer profiles in providers and tests; replaces the old `ModelProfile.update()` method.
Deprecated key spellings are translated per input before spreading, so a legacy key in an
override still overrides the base.

### `prompt_cache_outlook`

```python
def prompt_cache_outlook(messages: Sequence[ModelMessage], *, profile: ModelProfile | None=None, retention: timedelta | None=None, now: datetime | None=None) -> PromptCacheOutlook
```


Predict whether the provider's prompt cache is still warm for the next request on this history.

This is a pure function of the message history and an expectation boundary — it holds no state and makes no
requests, so a history processor, capability, or plain application code can call it with just a
message history to decide whether the next turn is a cheap moment for history-mutating maintenance
(compaction, pruning, repair). When the outlook is `'cold'` the next request pays a full prefix
re-write anyway, so the marginal cache cost of mutating history right now is ~zero.

The prediction compares the most recent [`ModelResponse.timestamp`][pydantic_ai.messages.ModelResponse.timestamp]
in `messages` against `now`: an idle gap within the retention window is `'warm'`, a larger gap is `'cold'`.
Responses are the anchor because they mark the provider's last confirmed use of the cache — a request that
has no response after it (like the just-appended request a [history processor](../message-history.md#processing-message-history)
sees, which hasn't been sent yet) never touched the cache, so its timestamp must not reset the idle clock.

Cache points in the history extend whichever boundary applies to their largest TTL, assuming they
were honored by the provider that served the requests.

Args:
    messages: The message history the next request would be built on, oldest first.
    profile: The model profile whose [`default_cache_retention`][pydantic_ai.profiles.ModelProfile.default_cache_retention]
        is used as the expectation boundary when `retention` is `None`.
    retention: The retention requested for these requests, replacing the profile's default. With a model
        and its settings in hand, pass
        [`model.resolve_cache_retention(model_settings)`][pydantic_ai.models.Model.resolve_cache_retention]:
        it returns `None` when the settings request nothing, so the profile's default still applies.
    now: The reference time to measure idleness against. Defaults to the current UTC time; inject a
        fixed value for deterministic tests.

Returns:
    `'warm'`, `'cold'`, or `'unknown'` (see [`PromptCacheOutlook`][pydantic_ai.profiles.PromptCacheOutlook]).







### `OpenAIModelProfile`

```python
class OpenAIModelProfile
```


Profile for models used with `OpenAIChatModel`.

ALL FIELDS MUST BE `openai_` PREFIXED SO YOU CAN MERGE THEM WITH OTHER MODELS.

```python
openai_chat_thinking_field: str | None
```

```python
openai_chat_send_back_thinking_parts: Literal['auto', 'tags', 'field', False]
```

```python
openai_supports_strict_tool_definition: bool
```

```python
openai_unsupported_model_settings: Sequence[str]
```

```python
openai_supports_tool_choice_required: bool
```

```python
openai_supports_forced_tool_choice_with_thinking: bool
```

```python
openai_system_prompt_role: OpenAISystemPromptRole | None
```

```python
openai_chat_supports_multiple_system_messages: bool
```

```python
openai_chat_streaming_requires_finish_reason: bool
```

```python
openai_chat_supports_web_search: bool
```

```python
openai_chat_audio_input_encoding: Literal['base64', 'uri']
```

```python
openai_chat_supports_file_urls: bool
```

```python
openai_supports_encrypted_reasoning_content: bool
```

```python
openai_supports_reasoning: bool
```

```python
openai_reasoning_enabled_by_default: bool
```

```python
openai_supports_reasoning_effort_none: bool
```

```python
openai_supports_minimal_reasoning_effort: bool
```

```python
openai_responses_supports_reasoning_mode: bool
```

```python
openai_responses_supports_reasoning_context: bool
```

```python
openai_responses_requires_function_call_status_none: bool
```

```python
openai_responses_supports_json_schema_output: bool
```

```python
openai_responses_tool_call_ids_are_response_scoped: bool
```

```python
openai_responses_supports_interleaved_function_calls: bool
```

```python
openai_supports_phase: bool
```

```python
openai_chat_supports_document_input: bool
```

```python
openai_chat_supports_max_completion_tokens: bool
```

```python
openai_supports_prompt_cache_breakpoints: bool
```

```python
openai_responses_requires_streaming: bool
```

```python
openai_responses_requires_store_false: bool
```

```python
openai_supports_input_token_counting: bool
```

### `validate_openai_profile`

```python
def validate_openai_profile(profile: ModelProfile) -> None
```


Validate an OpenAI-compatible profile after resolution. Called from `OpenAIChatModel.__init__`.

### `openai_model_profile`

```python
def openai_model_profile(model_name: str) -> ModelProfile
```


Get the model profile for an OpenAI model.

### `is_openai_live_model`

```python
def is_openai_live_model(model_name: str) -> bool
```


Whether a model name belongs to OpenAI's GPT-Live API rather than its Realtime API.

The two are different protocols on the same provider, so the model name is what picks between
them — see [`OpenAILiveModel`][pydantic_ai.realtime.openai_live.OpenAILiveModel].

### `openai_live_model_profile`

```python
def openai_live_model_profile(model_name: str) -> RealtimeModelProfile
```


Get the realtime model profile for an OpenAI GPT-Live model.

Live is far more constrained than the Realtime API: it owns turn-taking entirely (no manual
turns, no server-side interruption or truncation), speaks rather than writes, takes an image only
for its delegated backend to respond to, and seeds from text alone. It also has no end-of-turn frame, so Pydantic AI infers the boundary.

### `openai_realtime_model_profile`

```python
def openai_realtime_model_profile(model_name: str) -> RealtimeModelProfile
```


Get the realtime model profile for an OpenAI realtime model.

### `OpenAIJsonSchemaTransformer`

```python
class OpenAIJsonSchemaTransformer
```


Recursively handle the schema to make it compatible with OpenAI strict mode.

See https://platform.openai.com/docs/guides/function-calling?api-mode=responses#strict-mode for more details,
but this basically just requires:
* `additionalProperties` must be set to false for each object in the parameters
* all fields in properties must be marked as required### `openai_codex_model_profile`

```python
def openai_codex_model_profile(model_name: str) -> ModelProfile
```


Get the model profile for OpenAI Codex subscription-auth models.

The Codex backend speaks the Responses API with a narrower dialect than the standard OpenAI
endpoint: it serves streaming responses only, requires `store=false`, rejects sampling/tuning
request fields (verified live on PR [#6433](https://github.com/pydantic/pydantic-ai/pull/6433)),
and does not expose server-side input-token counting.### `AnthropicModelProfile`

```python
class AnthropicModelProfile
```


Profile for models used with `AnthropicModel`.

ALL FIELDS MUST BE `anthropic_` PREFIXED SO YOU CAN MERGE THEM WITH OTHER MODELS.

```python
anthropic_supports_fast_speed: bool
```

```python
anthropic_supports_adaptive_thinking: bool
```

```python
anthropic_supports_effort: bool
```

```python
anthropic_supports_dynamic_filtering: bool
```

```python
anthropic_supports_xhigh_effort: bool
```

```python
anthropic_disallows_budget_thinking: bool
```

```python
anthropic_disallows_sampling_settings: bool
```

```python
anthropic_disallows_top_effort_when_thinking_disabled: bool
```

```python
anthropic_default_code_execution_tool_version: AnthropicCodeExecutionToolVersion
```

```python
anthropic_supported_code_execution_tool_versions: tuple[AnthropicCodeExecutionToolVersion, ...]
```

```python
anthropic_supports_task_budgets: bool
```

```python
anthropic_supports_forced_tool_choice: bool
```

```python
anthropic_max_output_tokens: int | None
```

```python
anthropic_rejects_max_tokens_beyond_context_window: bool
```

```python
anthropic_binds_thinking_blocks: bool
```

### `resolve_anthropic_effort`

```python
def resolve_anthropic_effort(level: ThinkingEffort, *, supports_xhigh: bool) -> AnthropicEffort
```


Resolve a unified thinking effort level to the Anthropic `output_config.effort` value.

Shared between the direct Anthropic path and any provider that translates to the
Anthropic `output_config` wire shape (e.g. Bedrock Converse for Anthropic models).
Keeps `ANTHROPIC_THINKING_EFFORT_MAP` as the single source of truth for the
base mapping, while letting the `xhigh` passthrough decision live in one place.

### `anthropic_model_profile`

```python
def anthropic_model_profile(model_name: str) -> ModelProfile | None
```


Get the model profile for an Anthropic model.



### `GoogleModelProfile`

```python
class GoogleModelProfile
```


Profile for models used with `GoogleModel`.

ALL FIELDS MUST BE `google_` PREFIXED SO YOU CAN MERGE THEM WITH OTHER MODELS.

```python
google_supports_tool_combination: bool
```

```python
google_supports_server_side_tool_invocations: bool
```

```python
google_supported_mime_types_in_tool_returns: tuple[str, ...]
```

```python
google_supports_thinking_level: bool
```

```python
google_supports_minimal_thinking_level: bool
```

```python
google_thinking_levels: frozenset[GoogleThinkingLevel]
```

```python
google_supports_strict_tool_definition: bool
```

```python
google_web_search_billed_per_prompt: bool
```

### `google_model_profile`

```python
def google_model_profile(model_name: str) -> ModelProfile | None
```


Get the model profile for a Google model.

### `google_realtime_model_profile`

```python
def google_realtime_model_profile(model_name: str) -> RealtimeModelProfile
```


Get the realtime model profile for a Gemini Live model.

### `GoogleJsonSchemaTransformer`

```python
class GoogleJsonSchemaTransformer
```


Transforms the JSON Schema from Pydantic to be suitable for Gemini.

Gemini supports [a subset of OpenAPI v3.0.3](https://ai.google.dev/gemini-api/docs/function-calling#function_declarations).

### `GoogleOpenAPISchemaTransformer`

```python
class GoogleOpenAPISchemaTransformer
```


Transforms the JSON Schema from Pydantic into the OpenAPI v3.0.3 subset Gemini's `Schema` accepts.

A function declaration carries its parameters as *either* `parametersJsonSchema` (full JSON Schema,
which [`GoogleModel`][pydantic_ai.models.google.GoogleModel] sends) *or* `parameters` (an
[OpenAPI v3.0.3 subset](https://ai.google.dev/gemini-api/docs/function-calling#function_declarations)) —
the two are mutually exclusive. The Live API only implements `parameters`, so
[`GoogleRealtimeModel`][pydantic_ai.realtime.google.GoogleRealtimeModel] needs this narrower form,
where a union is `anyOf`, an enum is a list of strings, and there are no `$ref`s to resolve.

### `meta_model_profile`

```python
def meta_model_profile(model_name: str) -> ModelProfile | None
```


Get the model profile for a Meta model.### `amazon_model_profile`

```python
def amazon_model_profile(model_name: str) -> ModelProfile | None
```


Get the model profile for an Amazon model.### `deepseek_model_profile`

```python
def deepseek_model_profile(model_name: str) -> ModelProfile | None
```


Get the model profile for a DeepSeek model.### `GrokModelProfile`

```python
class GrokModelProfile
```


Profile for Grok models (used with XaiProvider and various OpenAI-compatible providers).

ALL FIELDS MUST BE `grok_` PREFIXED SO YOU CAN MERGE THEM WITH OTHER MODELS.

```python
grok_supports_builtin_tools: bool
```

```python
grok_supports_tool_choice_required: bool
```

```python
grok_reasoning_efforts: frozenset[GrokReasoningEffort]
```

### `grok_model_profile`

```python
def grok_model_profile(model_name: str) -> ModelProfile | None
```


Get the model profile for a Grok model.

### `grok_realtime_model_profile`

```python
def grok_realtime_model_profile(model_name: str) -> RealtimeModelProfile
```


Get the realtime model profile for an xAI Grok Voice model.### `mistral_model_profile`

```python
def mistral_model_profile(model_name: str) -> ModelProfile | None
```


Get the model profile for a Mistral model.### `qwen_model_profile`

```python
def qwen_model_profile(model_name: str) -> ModelProfile | None
```


Get the model profile for a Qwen model.### `GroqModelProfile`

```python
class GroqModelProfile
```


Profile for models used with GroqModel.

ALL FIELDS MUST BE `groq_` PREFIXED SO YOU CAN MERGE THEM WITH OTHER MODELS.

```python
groq_always_has_web_search_builtin_tool: bool
```

```python
groq_supports_reasoning_disable: bool
```

```python
groq_supports_graded_reasoning_effort: bool
```

### `groq_model_profile`

```python
def groq_model_profile(model_name: str) -> ModelProfile
```


Get the model profile for a Groq model.### `ZaiModelProfile`

```python
class ZaiModelProfile
```


Profile for Z.AI (Zhipu AI) GLM models.

```python
zai_supports_reasoning_effort: bool
```

```python
zai_reasoning_effort_mapping: Mapping[str, str]
```

### `zai_model_profile`

```python
def zai_model_profile(model_name: str) -> ModelProfile | None
```


The model profile for ZAI (Zhipu AI) GLM models, matched by Z.AI's native `glm-*` ids.

Marks thinking-capable models (`glm-5`, `glm-4.7`, `glm-4.6`, `glm-4.5`) via `supports_thinking=True`.
This includes the `glm-4.6v` and `glm-4.5v` vision models, which also support thinking mode per the
Z.AI docs. GLM-5.2 and GLM-5.3 additionally accept a per-request reasoning effort level, flagged via
`zai_supports_reasoning_effort=True`. GLM-5.3 always reasons and cannot disable thinking, flagged via
`thinking_always_enabled=True`.

The provider-specific request/response shape (e.g. the `reasoning_content` field used by Z.AI's API)
is configured in `ZaiProvider.model_profile()` rather than here. Providers that serve GLM models under
a different id scheme (e.g. Cerebras's `zai-glm-*`, which doesn't match the `glm-*` prefixes above)
configure thinking support in their own `model_profile()`.### `DecisionModelProfile`

```python
class DecisionModelProfile
```


Profile for a [decision model][pydantic_ai.models.decision.DecisionModel]: what the model can be asked.

These are facts about the model behind the URL, not the class that talks to it, so they are set by the provider
for the model name, or by `profile=`. A key left out falls back to the class's
[`max_choice_options`][pydantic_ai.models.decision.DecisionModel.max_choice_options] and
[`max_score_levels`][pydantic_ai.models.decision.DecisionModel.max_score_levels].

ALL FIELDS MUST BE `decision_` PREFIXED SO YOU CAN MERGE THEM WITH OTHER MODELS.

```python
decision_max_choice_options: int | None
```

```python
decision_max_score_levels: int | None
```

### `decision_model_profile`

```python
def decision_model_profile(model_name: str) -> ModelProfile
```


Get the model profile for a [decision model][pydantic_ai.models.decision.DecisionModel].

A decision model answers typed questions about a state; it does not generate text, call tools, or read anything
but text. Tool-mode structured output is how a decision model fills an `output_type`, and it rides on
`supports_tools`, so that stays on. A system prompt anywhere in the history is part of what the model judges, so
it needs no wrapping. Every other capability flag is off, and what no flag covers, such as a file in a prompt,
the model refuses itself.