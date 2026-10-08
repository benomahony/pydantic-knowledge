# `pydantic_ai.models.bedrock_mantle`

## Setup

For details on how to set up authentication with these models, see [model configuration for Bedrock Mantle](../../models/bedrock.md#bedrock-mantle).

### `BedrockMantleResponsesModel`

```python
class BedrockMantleResponsesModel
```


An OpenAI Responses model served by Amazon Bedrock Mantle.

Serves GPT-5.4+ (on the `/openai/v1` endpoint) and GPT-OSS (on the `/v1` endpoint); the endpoint is
chosen from the model profile.

```python
_mantle_client: AsyncOpenAI = field(repr=False)
```



### `BedrockMantleChatModel`

```python
class BedrockMantleChatModel
```


An OpenAI Chat Completions model served by Amazon Bedrock Mantle (GPT-OSS Safeguard).

The response-scoped tool-call-ID normalization added for #6536 is Responses-only: Mantle's Chat
Completions API returns globally-unique `chatcmpl-tool-*` IDs across separate responses (verified
live), unlike the `/openai/v1/responses` endpoint's per-response `call_0` counter, so the Chat path
needs no normalization.

```python
_mantle_client: AsyncOpenAI = field(repr=False)
```

