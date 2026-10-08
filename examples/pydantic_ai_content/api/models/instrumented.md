# pydantic_ai.models.instrumented

### `instrument_model`

```python
def instrument_model(model: Model, instrument: InstrumentationSettings | bool) -> Model
```


Wrap `model` in an `InstrumentedModel` so OTel/Logfire spans are emitted around requests.

### `InstrumentationSettings`

```python
class InstrumentationSettings
```


Options for instrumenting models and agents with OpenTelemetry.

Used in:

- [`Instrumentation`][pydantic_ai.capabilities.Instrumentation] capability
- [`Agent.instrument`][pydantic_ai.agent.Agent.instrument] / [`Agent.instrument_all()`][pydantic_ai.agent.Agent.instrument_all]
- [`InstrumentedModel`][pydantic_ai.models.instrumented.InstrumentedModel]

See the [Debugging and Monitoring guide](https://pydantic.dev/docs/ai/integrations/logfire/) for more info.

```python
tracer: Tracer = field(repr=False)
```

```python
include_binary_content: bool = True
```

```python
include_content: bool = True
```

```python
include_model_request_parameters: bool = True
```

```python
version: Literal[2, 3, 4, 5, 6] = DEFAULT_INSTRUMENTATION_VERSION
```

```python
use_aggregated_usage_attribute_names: bool = True
```





#### `aggregated_usage_attributes`

```python
def aggregated_usage_attributes(self, usage: UsageBase) -> dict[str, int]
```


Cumulative-usage OpenTelemetry attributes for a run/session span.

Remaps `gen_ai.usage.*` to `gen_ai.aggregated_usage.*` when `use_aggregated_usage_attribute_names`
is set, so a backend that sums span attributes doesn't double-count the run's cumulative usage
against the per-request `chat` spans' `gen_ai.usage.*`. Shared by the classic agent-run span (the
`Instrumentation` capability) and the realtime session span so the two can't drift.

### `InstrumentedModel`

```python
class InstrumentedModel
```


Model which wraps another model so that requests are instrumented with OpenTelemetry.

See the [Debugging and Monitoring guide](https://pydantic.dev/docs/ai/integrations/logfire/) for more info.

```python
instrumentation_settings: InstrumentationSettings
```

