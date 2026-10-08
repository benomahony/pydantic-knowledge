# `pydantic_ai.models.decision`

## Setup

For how an agent's output type and tools become a decision model's questions, and how to implement one, see [Decision models](../../models/decision.md).

### `NoulCriteria`

```python
class NoulCriteria
```


Descriptions of the two outcomes of a yes/no question.

```python
true: JsonValue = None
```

```python
false: JsonValue = None
```

### `NoulQuestion`

```python
class NoulQuestion
```


A yes/no question whose answer is the probability of yes.

```python
instructions: JsonValue = None
```

```python
criteria: NoulCriteria | None = None
```

```python
type: Literal['noul'] = 'noul'
```

### `ChoiceQuestion`

```python
class ChoiceQuestion
```


A question that selects one named option.

```python
criteria: dict[str, JsonValue]
```

```python
instructions: JsonValue = None
```

```python
type: Literal['choice'] = 'choice'
```

### `ScoreQuestion`

```python
class ScoreQuestion
```


A question that scores the state against ordered levels.

```python
criteria: list[JsonValue]
```

```python
instructions: JsonValue = None
```

```python
type: Literal['score'] = 'score'
```

### `NoulAnswer`

```python
class NoulAnswer
```


The probability of yes for a yes/no question.

```python
noul: float
```

```python
type: Literal['noul'] = 'noul'
```

### `ChoiceAnswer`

```python
class ChoiceAnswer
```


The selected option and its probability distribution.

```python
choice: str
```

```python
confidence: float
```

```python
probabilities: dict[str, float]
```

```python
type: Literal['choice'] = 'choice'
```

### `ScoreAnswer`

```python
class ScoreAnswer
```


A score and its probability distribution across levels.

```python
score: float
```

```python
confidence: float
```

```python
probabilities: dict[int, float]
```

```python
legend: dict[int, JsonValue] = field(default_factory=dict[int, JsonValue])
```

```python
type: Literal['score'] = 'score'
```

### `DecisionRequest`

```python
class DecisionRequest
```


A request to decide typed questions about a state.

```python
state: JsonValue
```

```python
questions: dict[str, DecisionQuestion]
```

### `DecisionResponse`

```python
class DecisionResponse
```


The answers to a [`DecisionRequest`][pydantic_ai.models.decision.DecisionRequest], and what produced them.

```python
answers: dict[str, DecisionAnswer]
```

```python
model_name: str
```

```python
usage: RequestUsage = field(default_factory=RequestUsage)
```

```python
provider_response_id: str | None = None
```



### `DecisionModelSettings`

```python
class DecisionModelSettings
```


Settings used for a decision model request.

```python
decision_boolean_threshold: float
```

```python
decision_route_threshold: float
```

### `DecisionHandOff`

```python
class DecisionHandOff
```


A decision model handed the step off instead of answering it: the base of the hand-offs it raises.

A [`ModelAPIError`][pydantic_ai.exceptions.ModelAPIError], so a
[`FallbackModel`][pydantic_ai.models.fallback.FallbackModel] with a language model behind the decision model
hands that model the whole step by default, tools and all, and only the steps the decision model hands off cost
a language model call. Pass `fallback_on=DecisionHandOff` to hand off only these, and let an error from the
decision model's backend fail the run rather than go to the language model.

```python
route: str
```

```python
probability: float
```

### `UnfillableRoute`

```python
class UnfillableRoute
```


A decision model picked a route whose fields or arguments it cannot fill.

A tool with an argument the model cannot express, such as a free-form `str`, or an output type with such a
field. See [`DecisionHandOff`][pydantic_ai.models.decision.DecisionHandOff] for how a
[`FallbackModel`][pydantic_ai.models.fallback.FallbackModel] takes the step.

#### `tool_name`

```python
def tool_name(self) -> str
```


Deprecated alias for [`route`][pydantic_ai.models.decision.DecisionHandOff.route].

For a tool, the tool's name. For an output type, the name the route question offered it under, as `Reply`,
rather than the name of the output tool Pydantic AI made for it.

### `UnsureRoute`

```python
class UnsureRoute
```


A decision model picked a route less likely than `decision_route_threshold`.

Raised before any request to fill the route. See
[`DecisionHandOff`][pydantic_ai.models.decision.DecisionHandOff] for how a
[`FallbackModel`][pydantic_ai.models.fallback.FallbackModel] takes the step.

```python
probabilities: dict[str, float]
```

```python
threshold: float
```



### `DecisionModel`

```python
class DecisionModel
```


Base class for decision models: models that answer typed questions about a text rather than write text.

A decision model is sent a *state*, the text or JSON value to judge, and a set of named questions of three
kinds: a yes/no ([`NoulQuestion`][pydantic_ai.models.decision.NoulQuestion]), a pick-one
([`ChoiceQuestion`][pydantic_ai.models.decision.ChoiceQuestion]), and a score against an ordered rubric
([`ScoreQuestion`][pydantic_ai.models.decision.ScoreQuestion]). It answers each one with a probability or a
distribution. That exchange is the Decisions protocol, and this class maps an agent run onto it, so that an
agent whose job is to decide something runs on a decision model like on any other model:

- Each field of the `output_type` is one question, and its type picks the kind: a `bool` is a yes/no, a
  `Literal` or `Enum` of strings is a pick-one, and whole numbers from 0 with a description per level are a
  rubric. A `list` or `dict` of options is one yes/no per option, and a nested model is its fields. A field of
  any other type is a [`UserError`][pydantic_ai.exceptions.UserError] before a request is sent, unless there
  is another route to take, as below.
- The field's description is the question, the output type's docstring its goal, and the agent's
  `instructions` framing shared by every question; a nested field's question also carries what it sits in.
  The latest user prompt is the text to judge, the message history before it goes along beside it, and once a
  tool has returned or a retry was sent, what was done since goes along apart from both.
- With tools attached, or a union of output types, one more pick-one asks which route the text calls for, and
  the likeliest is taken. The fields of every route the model can fill are asked beside it, each on the premise
  of its route, and only the taken route's answers are read; past a size cutoff, a picked route with fields is
  filled in a second request instead. A route whose fields the model cannot express, a single output type's
  included, is raised as [`UnfillableRoute`][pydantic_ai.models.decision.UnfillableRoute], for a
  [`FallbackModel`][pydantic_ai.models.fallback.FallbackModel] to hand to a language model. A pick below
  `decision_route_threshold`, when set, is raised as [`UnsureRoute`][pydantic_ai.models.decision.UnsureRoute]
  the same way.
- Each field's confidence, the full distribution of each pick-one and rubric, and the route pick are reported
  in [`ModelResponse.provider_details`][pydantic_ai.messages.ModelResponse.provider_details].

The answers arrive in one piece, so a streamed run gets the whole answer as one event.

To support a backend, subclass this, implement [`decide`][pydantic_ai.models.decision.DecisionModel.decide]
along with `model_name`, `system` and `base_url`, and set `max_choice_options` and `max_score_levels` to the
backend's limits, or have its provider set them per model in a
[`DecisionModelProfile`][pydantic_ai.profiles.decision.DecisionModelProfile]. See [Decision models](https://pydantic.dev/docs/ai/models/decision/) for the full rules
and an example.

```python
max_choice_options: ClassVar[int | None] = None
```

```python
max_score_levels: ClassVar[int | None] = None
```

#### `profile`

```python
def profile(self) -> ModelProfile
```


The model profile: text output off and inline system prompts on, whatever the provider or `profile=` says.

A decision model answers questions and has no way to write text, so this is a fact about the class
rather than a default to override: with text output left on, an `output_type` like `[Ticket, str]`
would pass the shared request preparation and have its `str` branch silently never taken.

It also judges a system prompt rather than asking it, so a system prompt partway through the conversation
stays a `system` entry: without inline system prompts, the shared request preparation would fold it into
the user text, where it would be judged as the request.

#### `decide`

```python
async def decide(self, request: DecisionRequest, model_settings: DecisionModelSettings) -> DecisionResponse
```


Send one request to the backend and return its answers.

This is called once per request the model makes: once per step, or twice when a route is picked in one
request and, past the size cutoff for asking every route's fields up front, filled in a second. Every
question in `request.questions` needs an answer of the matching kind under the same name.

Raise [`ModelHTTPError`][pydantic_ai.exceptions.ModelHTTPError] or
[`ModelAPIError`][pydantic_ai.exceptions.ModelAPIError] when the backend fails, so a
[`FallbackModel`][pydantic_ai.models.fallback.FallbackModel] can take over;
[`UnexpectedModelBehavior`][pydantic_ai.exceptions.UnexpectedModelBehavior] when it returns something that
cannot be read; and [`UserError`][pydantic_ai.exceptions.UserError] when the request cannot be sent as
given. Forward `timeout`, `extra_headers` and `extra_body` from `model_settings` where the backend
supports them.











### `DecisionStreamedResponse`

```python
class DecisionStreamedResponse
```


A decision model's whole answer as one event, so that a streamed run works on a model that cannot stream.

```python
_response: ModelResponse
```

#### `close_stream`

```python
async def close_stream(self) -> None
```


No live stream to close: the whole answer was in hand before the first event.















































































































