# `pydantic_evals.online_capability`

Online evaluation capability for pydantic-ai agents.

Provides an `OnlineEvaluation` capability that attaches evaluators to agent runs,
dispatching them asynchronously in the background after each run completes.



### `OnlineEvaluation`

```python
class OnlineEvaluation
```


Capability that runs online evaluators on agent run results.

Dispatches evaluators asynchronously in the background after each completed
agent run. Non-blocking — the agent run returns without waiting for evaluators
to finish.

!!! note
    [`OnlineEvaluation`][pydantic_evals.online_capability.OnlineEvaluation]
    wraps [`agent.run()`][pydantic_ai.agent.AbstractAgent.run],
    [`agent.run_stream()`][pydantic_ai.agent.AbstractAgent.run_stream], and
    [`agent.iter()`][pydantic_ai.agent.Agent.iter] when the run reaches a
    final result.
    For streaming runs, evaluators are dispatched only after the final
    result is available and the surrounding context manager exits.

Example:
```python
from dataclasses import dataclass

from pydantic_ai import Agent
from pydantic_evals.evaluators import Evaluator, EvaluatorContext
from pydantic_evals.online_capability import OnlineEvaluation


@dataclass
class OutputNotEmpty(Evaluator):
    def evaluate(self, ctx: EvaluatorContext) -> bool:
        return bool(ctx.output)


agent = Agent(
    'openai:gpt-5.2',
    name='assistant',
    capabilities=[OnlineEvaluation(evaluators=[OutputNotEmpty()])],
)
```

```python
evaluators: Sequence[Evaluator | OnlineEvaluator]
```

```python
config: OnlineEvalConfig | None = None
```

```python
_online_evaluators: list[OnlineEvaluator] = field(init=False, repr=False)
```

```python
_resolved_config: OnlineEvalConfig = field(init=False, repr=False)
```