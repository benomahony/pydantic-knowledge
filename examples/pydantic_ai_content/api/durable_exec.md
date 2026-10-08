# `pydantic_ai.durable_exec`

### `PydanticAIPlugin`

```python
class PydanticAIPlugin
```


Temporal client and worker plugin for Pydantic AI.

### `AgentPlugin`

```python
class AgentPlugin
```


Temporal worker plugin for a specific Pydantic AI agent.

Accepts either a regular `Agent` carrying a
[`TemporalDurability`][pydantic_ai.durable_exec.temporal.TemporalDurability]
capability (whose chain is walked to find the bound capability), or the
deprecated [`TemporalAgent`][pydantic_ai.durable_exec.temporal.TemporalAgent]
wrapper, and registers the agent's activities on the worker.