# `pydantic_ai.models.snowflake`

## Setup

For details on how to set up authentication with this model, see [model configuration for Snowflake Cortex](../../models/snowflake.md).

Snowflake Cortex model implementation using Snowflake's OpenAI-compatible Chat Completions API.

### `SnowflakeReasoning`

```python
class SnowflakeReasoning
```


Configuration for reasoning tokens in Snowflake Cortex requests to Claude models.

See <https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-rest-api> for details.

```python
effort: Literal['high', 'medium', 'low']
```

```python
max_tokens: int
```

### `SnowflakeModelSettings`

```python
class SnowflakeModelSettings
```


Settings used for a Snowflake Cortex model request.

ALL FIELDS MUST BE `snowflake_` PREFIXED SO YOU CAN MERGE THEM WITH OTHER MODELS.

```python
snowflake_reasoning: SnowflakeReasoning
```



### `SnowflakeModel`

```python
class SnowflakeModel
```


A model that uses Snowflake Cortex's OpenAI-compatible Chat Completions API.

Snowflake Cortex serves Claude, GPT, Llama, Mistral, DeepSeek, and Snowflake's own models,
with all inference running inside the customer's Snowflake account.

Apart from `__init__`, all methods are private or match those of the base class.





### `SnowflakeStreamedResponse`

```python
class SnowflakeStreamedResponse
```


Implementation of `StreamedResponse` for Snowflake Cortex models.

