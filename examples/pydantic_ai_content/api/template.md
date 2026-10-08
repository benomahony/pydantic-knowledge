# `pydantic_ai.template`

Template string support for dynamic instructions.

### `TemplateStr`

```python
class TemplateStr
```


A Handlebars template string that renders against `RunContext.deps`.

When used in type hints, strings containing `{{` are automatically
compiled as Handlebars templates during Pydantic validation.

Uses [pydantic-handlebars](https://github.com/pydantic/pydantic-handlebars)
for template compilation, schema validation, and rendering.

When used with an `Agent`, `deps_type` is inferred automatically from
the agent's validation context, so you only need to pass it when constructing
a `TemplateStr` outside of an agent (e.g. for standalone rendering).

Example:
    ```python {test="skip"}
    from dataclasses import dataclass

    from pydantic_ai import Agent, TemplateStr


    @dataclass
    class MyDeps:
        name: str

    agent = Agent(
        'openai:gpt-5',
        deps_type=MyDeps,
        instructions=TemplateStr('Hello {{name}}'),
    )
    ```

#### `render`

```python
def render(self, deps: AgentDepsT | None=None) -> str
```


Render the template against the given deps object.



