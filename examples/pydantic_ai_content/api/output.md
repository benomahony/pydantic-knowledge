# `pydantic_ai.output`



### `ToolOutput`

```python
class ToolOutput
```


Marker class to use a tool for output and optionally customize the tool.

Example:
```python {title="tool_output.py"}
from pydantic import BaseModel

from pydantic_ai import Agent, ToolOutput


class Fruit(BaseModel):
    name: str
    color: str


class Vehicle(BaseModel):
    name: str
    wheels: int


agent = Agent(
    'openai:gpt-5.2',
    output_type=[
        ToolOutput(Fruit, name='return_fruit'),
        ToolOutput(Vehicle, name='return_vehicle'),
    ],
)
result = agent.run_sync('What is a banana?')
print(repr(result.output))
#> Fruit(name='banana', color='yellow')
```

```python
output: OutputTypeOrFunction[OutputDataT]
```

```python
name: str | None
```

```python
description: str | None
```

```python
max_retries: int | None
```

```python
strict: bool | None
```

```python
sequential: bool
```

### `NativeOutput`

```python
class NativeOutput
```


Marker class to use the model's native structured outputs functionality for outputs and optionally customize the name and description.

Example:
```python {title="native_output.py" requires="tool_output.py"}
from pydantic_ai import Agent, NativeOutput

from tool_output import Fruit, Vehicle

agent = Agent(
    'openai:gpt-5.2',
    output_type=NativeOutput(
        [Fruit, Vehicle],
        name='Fruit or vehicle',
        description='Return a fruit or vehicle.'
    ),
)
result = agent.run_sync('What is a Ford Explorer?')
print(repr(result.output))
#> Vehicle(name='Ford Explorer', wheels=4)
```

```python
outputs: OutputTypeOrFunction[OutputDataT] | Sequence[OutputTypeOrFunction[OutputDataT]]
```

```python
name: str | None
```

```python
description: str | None
```

```python
strict: bool | None
```

```python
template: str | Literal[False] | None
```

### `PromptedOutput`

```python
class PromptedOutput
```


Marker class to use a prompt to tell the model what to output and optionally customize the prompt.

Example:
```python {title="prompted_output.py" requires="tool_output.py"}
from pydantic import BaseModel

from pydantic_ai import Agent, PromptedOutput

from tool_output import Vehicle


class Device(BaseModel):
    name: str
    kind: str


agent = Agent(
    'openai:gpt-5.2',
    output_type=PromptedOutput(
        [Vehicle, Device],
        name='Vehicle or device',
        description='Return a vehicle or device.'
    ),
)
result = agent.run_sync('What is a MacBook?')
print(repr(result.output))
#> Device(name='MacBook', kind='laptop')

agent = Agent(
    'openai:gpt-5.2',
    output_type=PromptedOutput(
        [Vehicle, Device],
        template='Gimme some JSON: {schema}'
    ),
)
result = agent.run_sync('What is a Ford Explorer?')
print(repr(result.output))
#> Vehicle(name='Ford Explorer', wheels=4)
```

```python
outputs: OutputTypeOrFunction[OutputDataT] | Sequence[OutputTypeOrFunction[OutputDataT]]
```

```python
name: str | None
```

```python
description: str | None
```

```python
template: str | Literal[False] | None
```

### `OutputObjectDefinition`

```python
class OutputObjectDefinition
```


Definition of an output object used for structured output generation.

```python
json_schema: ObjectJsonSchema
```

```python
name: str | None = None
```

```python
description: str | None = None
```

```python
strict: bool | None = None
```

### `OutputContext`

```python
class OutputContext
```


Context about the output being processed, passed to output hooks.

```python
mode: OutputMode
```

```python
output_type: type[Any] | None
```

```python
object_def: OutputObjectDefinition | None
```

```python
has_function: bool
```

```python
function_name: str | None = None
```

```python
tool_call: ToolCallPart | None = None
```

```python
tool_def: ToolDefinition | None = None
```

```python
allows_text: bool = False
```

```python
allows_image: bool = False
```

```python
allows_deferred_tools: bool = False
```

### `TextOutput`

```python
class TextOutput
```


Marker class to use text output for an output function taking a string argument.

Example:
```python
from pydantic_ai import Agent, TextOutput


def split_into_words(text: str) -> list[str]:
    return text.split()


agent = Agent(
    'openai:gpt-5.2',
    output_type=TextOutput(split_into_words),
)
result = agent.run_sync('Who was Albert Einstein?')
print(result.output)
#> ['Albert', 'Einstein', 'was', 'a', 'German-born', 'theoretical', 'physicist.']
```

!!! note
    When streaming, [`stream_text()`][pydantic_ai.result.StreamedRunResult.stream_text] does not apply the
    wrapped function. Use [`stream_output()`][pydantic_ai.result.StreamedRunResult.stream_output] to stream
    the value it produces.

```python
output_function: TextOutputFunc[OutputDataT]
```

### `StructuredDict`

```python
def StructuredDict(json_schema: JsonSchemaValue, name: str | None=None, description: str | None=None) -> type[JsonSchemaValue]
```


Returns a `dict[str, Any]` subclass with a JSON schema attached that will be used for structured output.

Args:
    json_schema: A JSON schema of type `object` defining the structure of the dictionary content.
    name: Optional name of the structured output. If not provided, the `title` field of the JSON schema will be used if it's present.
    description: Optional description of the structured output. If not provided, the `description` field of the JSON schema will be used if it's present.

Example:
```python {title="structured_dict.py"}
from pydantic_ai import Agent, StructuredDict

schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'age': {'type': 'integer'}
    },
    'required': ['name', 'age']
}

agent = Agent('openai:gpt-5.2', output_type=StructuredDict(schema))
result = agent.run_sync('Create a person')
print(result.output)
#> {'name': 'John Doe', 'age': 30}
```

### `Choice`

```python
class Choice
```


One choice in a [`Choices`][pydantic_ai.output.Choices] set: what it means, and what it stands for.

Building a set from descriptions alone yields the key the model picked, so `Choice` is only reached for
when a choice stands for something other than its key:

```python {title="choice.py"}
from pydantic_ai import Agent, Choice, Choices

Card = Choices(
    {
        'visa': Choice('Any card starting with a 4.', value=4),
        'amex': Choice('Any card starting with a 3.', value=3),
    }
)

agent = Agent('openai:gpt-5.2', output_type=Card)
result = agent.run_sync('4111 1111 1111 1111')
print(result.output)
#> 4
```

```python
description: str | None
```

```python
value: T_co
```





### `Choices`

```python
def Choices(choices: Sequence[str] | Mapping[str, str | Choice[Any]], *, name: str | None=None, description: str | None=None) -> type[Any]
```


Returns a type the model can only fill with one of `choices`, each described where it is built.

Use it when the set is only known once the run is under way -- the actions available on the screen in front
of an agent, the records a search returned. For a set you know when you write the code, use a `Literal` or
an `Enum` (with [`UseEnumMemberDocstrings`][pydantic_ai.UseEnumMemberDocstrings] to describe its
members), which give you exhaustiveness checking that a run-time set cannot.

Like [`StructuredDict`][pydantic_ai.output.StructuredDict] it returns a type, so it works as an
`output_type`, as a field of a Pydantic model, and as a tool parameter.

Args:
    choices: The choices, as a sequence of keys, a mapping from key to its description, or a mapping from
        key to a [`Choice`][pydantic_ai.output.Choice] carrying both a description and what the key stands
        for.
    name: Name of the output tool or structured output. Defaults to `'Choices'`.
    description: What the model is being asked to pick, e.g. `'Which action to take next.'`.

Example:
```python {title="choices.py"}
from pydantic_ai import Agent, Choices

Intent = Choices(
    {
        'refund': 'The customer wants their money back.',
        'replace': 'The customer wants a working unit instead.',
        'escalate': 'Nobody on this tier can resolve it.',
    },
    name='customer_intent',
    description='What the customer is asking for.',
)

agent = Agent('openai:gpt-5.2', output_type=Intent)
result = agent.run_sync('The blender arrived smashed. Just send me another one.')
print(result.output)
#> replace
```

### `BoolCriteria`

```python
class BoolCriteria
```


What a yes and what a no would each mean, for a `bool` field or parameter to carry in `Annotated`.

A `bool` field's description says what is being asked; these two say what either answer amounts to,
which is what a set of options gets from [`Choices()`][pydantic_ai.output.Choices] and an `Enum` gets
from [`UseEnumMemberDocstrings`][pydantic_ai.UseEnumMemberDocstrings]. Both descriptions reach the model
in the schema, as a description on each of the two constants a boolean can be.

It is a marker rather than a type, so the field stays a plain `bool` to every type checker, and the
value you get back is a plain `True` or `False`:

```python {title="bool_criteria.py"}
from typing import Annotated

from pydantic import BaseModel, Field

from pydantic_ai import Agent, BoolCriteria


class Settled(BaseModel):
    refunded: Annotated[
        bool,
        BoolCriteria(true='Money was returned to the customer.', false='No refund was issued.'),
    ] = Field(description='Was a refund issued?')


agent = Agent('openai:gpt-5.2', output_type=Settled)
result = agent.run_sync('We have sent the 40 pounds back to your card.')
print(result.output.refunded)
#> True
```

On [TypeSafe's Jev](../models/typesafe.md), which asks a yes/no as its own primitive, the two land in
that question's `criteria` as `true` and `false`, sent verbatim.

```python
true: str
```

```python
false: str
```