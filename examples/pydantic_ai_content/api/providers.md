# `pydantic_ai.providers`

## `Provider`

```python
class Provider
```


Abstract class for a provider.

The provider is in charge of providing an authenticated client to the API.

Each provider only supports a specific interface. An interface can be supported by multiple providers.

For example, the `OpenAIChatModel` interface can be supported by the `OpenAIProvider` and the `DeepSeekProvider`.

When used as an async context manager, providers that create their own HTTP client will close it on exit.
This is handled automatically when using [`Agent`][pydantic_ai.agent.Agent] as a context manager.

```python
_client: InterfaceClient
```

```python
_own_http_client: AsyncHTTPClient | None = None
```

```python
_http_client_factory: Callable[[], AsyncHTTPClient] | None = None
```

```python
_entered_count: int = 0
```

```python
_model_id_namespace: str | None = None
```

### `name`

```python
def name(self) -> str
```


The provider name.

The returned value flows into [`ModelMessage.provider_name`][pydantic_ai.messages.ModelMessage]
on every part. Thinking-tag detection and native-tool detection check this value when
the model class loads history, so silently renaming a concrete `name` value breaks
replay of any message history captured against the old name.

### `model_id_namespace`

```python
def model_id_namespace(self) -> str
```


The namespace used to fully qualify model IDs routed through this provider.

### `base_url`

```python
def base_url(self) -> str
```


The base URL for the provider API.

### `client`

```python
def client(self) -> InterfaceClient
```


The client for the provider.

### `model_profile`

```python
def model_profile(model_name: str) -> ModelProfile | None
```


The model profile for the named model, if available.

### `realtime_model_profile`

```python
def realtime_model_profile(model_name: str) -> RealtimeModelProfile | None
```


The realtime model profile for the named model, if available.

## `infer_provider`

```python
def infer_provider(provider: str) -> Provider[Any]
```


Infer the provider from the provider name.## `infer_provider_class`

```python
def infer_provider_class(provider: str) -> type[Provider[Any]]
```


Infers the provider class from the provider name.## `gateway_provider`

```python
def gateway_provider(upstream_provider: Literal['openai', 'openai-chat', 'openai-responses', 'chat', 'responses'], /, *, route: str | None=None, api_key: str | None=None, base_url: str | None=None, http_client: AsyncHTTPClient | None=None) -> Provider[AsyncOpenAI]
```
## `AnthropicProvider`

```python
class AnthropicProvider
```


Provider for Anthropic API.

### `BaseGoogleProvider`

```python
class BaseGoogleProvider
```


Common base for the Gemini API and Google Cloud providers.

Abstract — instantiate [`GoogleProvider`][pydantic_ai.providers.google.GoogleProvider] for the
Gemini API or [`GoogleCloudProvider`][pydantic_ai.providers.google_cloud.GoogleCloudProvider] for
Google Cloud. Subclasses share `base_url`, `client`, `_set_http_client`, and model-profile
lookup; each subclass owns its own `Client` construction.



### `GoogleProvider`

```python
class GoogleProvider
```


Provider for the Gemini API (formerly Google AI Studio / Google GLA).

### `GoogleCloudProvider`

```python
class GoogleCloudProvider
```


Provider for Google Cloud (formerly known as Vertex AI).

### `OpenAIProvider`

```python
class OpenAIProvider
```


Provider for OpenAI API.

Changing `base_url` does not change the OpenAI model profile selection. For another service,
use its dedicated provider when available. For a custom gateway, subclass this provider and
override `model_profile`, or configure the model's `profile` explicitly.
See [OpenAI-compatible models](https://pydantic.dev/docs/ai/models/openai/#openai-compatible-models).

OpenAI Codex subscription-auth provider: OAuth flow primitives, credential refresh, wire dialect.

Core owns the protocol primitives (PKCE context, authorization URL, code exchange, refresh) and,
because the pinned redirect URI makes every login a localhost callback, the one-shot callback
catcher (`exchange_code_from_callback()`); browser opening and persistent credential storage
belong to applications and harnesses.

The authorization-code + PKCE redirect flow is the only login flow the public Codex client
supports: its registration pins the redirect URI to `http://localhost:1455/auth/callback`
(exact-match, probed live 2026-08-25), and the auth service serves no device-authorization
endpoint. `exchange_code_from_callback()` serves this exact redirect URI and exchanges the
authorization code.



### `CredentialsRefreshError`

```python
class CredentialsRefreshError
```


Refreshing Codex credentials against the token endpoint failed.

When the underlying error is `invalid_grant`, the stored grant is no longer usable and a fresh
authorization is required (locally: rerun `codex login`; in an app: rerun your connect flow).

### `CredentialsPersistenceError`

```python
class CredentialsPersistenceError
```


Rotated credentials were updated in memory but the persistence callback raised.

The in-memory credentials are current and were handed to the callback before it failed; the
error surfaces so callers do not mistake a failed save for durability.

### `OpenAICodexCredentials`

```python
class OpenAICodexCredentials
```


Codex subscription credentials.

The tokens are excluded from `repr` so a logged or traceback-embedded instance does not leak them.

```python
_: KW_ONLY
```

```python
access_token: str = field(repr=False)
```

```python
refresh_token: str = field(repr=False)
```

```python
account_id: str
```

#### `from_codex_cli_auth`

```python
def from_codex_cli_auth(cls, data: Mapping[str, Any]) -> Self
```


Parse the Codex CLI `~/.codex/auth.json` shape (`{'tokens': {...}}`).























### `OpenAICodexCredentialSource`

```python
class OpenAICodexCredentialSource
```


Application-owned storage for the credentials, so refreshed tokens outlive the process.

The provider owns the credential lifecycle (expiry checks, refresh, single-flight) and calls
this only to read and write the stored set: `load()` on first use, and `save()` after tokens
are refreshed.

Refresh tokens are single-use, so before refreshing, the provider re-reads storage with
`load()` and adopts newer credentials if another process using the same store already
refreshed them. That is best-effort, not mutual exclusion: two processes can still race
between `load()` and `save()`.

Conformance is structural, but implementations are encouraged to subclass the protocol
explicitly so type checkers verify the method signatures.

#### `load`

```python
async def load(self) -> OpenAICodexCredentials
```


Return the currently stored credentials.

#### `save`

```python
async def save(self, credentials: OpenAICodexCredentials) -> None
```


Durably replace the stored credentials with a freshly rotated set.



### `OpenAICodexOAuthFlow`

```python
class OpenAICodexOAuthFlow
```


Pure authorization-code + PKCE context for the OpenAI Codex public client.

This is the only login flow the public client supports (no device flow; redirect URI pinned to
`localhost:1455`, probed exact-match). Construction does no I/O: build the context anywhere,
send the user to `authorization_url()`, then let `exchange_code_from_callback()` receive the
redirect on localhost and exchange its code. The browser and credential storage stay
caller-owned.



#### `authorization_url`

```python
def authorization_url(self, *, scope: str | None=None, extra_params: Mapping[str, str] | None=None) -> str
```


The URL to send the user to. Note the public client pins redirects to localhost.

Args:
    scope: The OAuth scopes to request; `None` means the standard Codex login scopes.
    extra_params: Additional query parameters, merged over the defaults (so they can also
        override them), except `client_id` and `redirect_uri`: `exchange_code()` always
        posts the public client id and the flow's `redirect_uri`, so overriding either
        here would make the authorization code unusable. The production Codex login's
        `id_token_add_organizations=true` and `codex_cli_simplified_flow=true` are sent by
        default: without the former, the `id_token` can omit the account id for multi-org
        accounts (live-verified 2026-08-25).

#### `exchange_code`

```python
async def exchange_code(self, code: str) -> OpenAICodexCredentials
```


Exchange an authorization code for credentials (call this in your callback handler).



### `OpenAICodexProvider`

```python
class OpenAICodexProvider
```


Provider for OpenAI Codex subscription authentication.

Wraps the standard `OpenAIProvider` machinery pointed at the Codex backend, injecting Codex
OAuth credentials instead of API keys. One provider instance carries one set of credentials
(there is no process-global cache). The instance binds its refresh lock to the first event
loop that awaits a request, so do not reuse it across loops.

```python {test="skip" lint="skip"}
provider = OpenAICodexProvider(credential_source=YourCredentialStore())
agent = Agent('openai-codex:gpt-5.6-luna', provider=provider)
```

#### `credentials`

```python
def credentials(self) -> OpenAICodexCredentials
```


The credentials currently held in memory, rotated in place by refreshes.













### `XaiProvider`

```python
class XaiProvider
```


Provider for xAI API (native xAI SDK).

#### `api_key`

```python
def api_key(self) -> str | None
```


The resolved API key, or `None` when the provider was built from a pre-configured `xai_client`.

The gRPC `AsyncClient` doesn't expose its key, so this returns the one resolved from the `api_key`
argument or `XAI_API_KEY`. Used by transports that authenticate outside the SDK, e.g.
[`XaiRealtimeModel`][pydantic_ai.realtime.xai.XaiRealtimeModel]'s WebSocket `Authorization` header.

#### `api_host`

```python
def api_host(self) -> str | None
```


The custom `api_host` this provider was configured with, or `None`.

Read by [`XaiRealtimeModel`][pydantic_ai.realtime.xai.XaiRealtimeModel] to reject a custom host
it can't yet honor: the realtime WebSocket derives its URL from `base_url`, not the gRPC channel
target that `api_host` sets.

### `DeepSeekProvider`

```python
class DeepSeekProvider
```


Provider for DeepSeek API.### `BedrockJsonSchemaTransformer`

```python
class BedrockJsonSchemaTransformer
```


Transforms schemas to the subset supported by Bedrock structured outputs.

The transformer is applied to Bedrock tool and output schemas during request
customization. Strict-mode rewrites are applied when:
- `NativeOutput` is used as the `output_type` of the Agent. `BedrockConverseModel`
  forces native output schemas to `strict=True` before request customization.
- `strict=True` is set explicitly on a Tool.

Like `AnthropicJsonSchemaTransformer`, Bedrock does not infer strict tool mode
from `strict=None`. Strict tool definitions are opt-in: callers must set
`strict=True` explicitly. This avoids silently changing large toolsets into
strict toolsets, which can exceed Anthropic/Bedrock's 20 strict-tools-per-request
limit, and avoids applying potentially lossy strict-mode schema rewrites unless
requested.

When `strict=True`, `additionalProperties: false` is injected on objects and keys
Bedrock rejects are removed from the schema and re-emitted into the field's
`description` so the model still has the hint.

### `BedrockModelProfile`

```python
class BedrockModelProfile
```


Profile for models used with BedrockModel.

ALL FIELDS MUST BE `bedrock_` PREFIXED SO YOU CAN MERGE THEM WITH OTHER MODELS.

```python
bedrock_supports_tool_choice: bool
```

```python
bedrock_tool_result_format: Literal['text', 'json']
```

```python
bedrock_send_back_thinking_parts: bool
```

```python
bedrock_supports_prompt_caching: bool
```

```python
bedrock_supports_tool_caching: bool
```

```python
bedrock_supported_media_kinds_in_tool_returns: frozenset[Literal['image', 'document', 'video']]
```

```python
bedrock_tool_result_colocatable_content: frozenset[Literal['text', 'image', 'document', 'video']]
```

```python
bedrock_supports_leading_assistant_message: bool
```

```python
bedrock_supports_tool_result_status: bool
```

```python
bedrock_supports_strict_tool_definition: bool
```

```python
bedrock_thinking_variant: Literal['anthropic', 'openai', 'qwen'] | None
```

```python
bedrock_supports_adaptive_thinking: bool
```

```python
bedrock_supports_effort: bool
```

```python
bedrock_top_k_variant: Literal['anthropic', 'nova'] | None
```

```python
bedrock_disallows_sampling_settings: bool
```

```python
bedrock_supported_on_converse: bool
```

### `bedrock_anthropic_model_profile`

```python
def bedrock_anthropic_model_profile(model_name: str) -> ModelProfile | None
```


Get the model profile for an Anthropic model used via Bedrock.

### `bedrock_amazon_model_profile`

```python
def bedrock_amazon_model_profile(model_name: str) -> ModelProfile | None
```


Get the model profile for an Amazon model used via Bedrock.

### `bedrock_deepseek_model_profile`

```python
def bedrock_deepseek_model_profile(model_name: str) -> ModelProfile | None
```


Get the model profile for a DeepSeek model used via Bedrock.

### `bedrock_meta_model_profile`

```python
def bedrock_meta_model_profile(model_name: str) -> ModelProfile | None
```


Get the model profile for a Meta Llama model used via Bedrock.

### `bedrock_mistral_model_profile`

```python
def bedrock_mistral_model_profile(model_name: str) -> ModelProfile | None
```


Get the model profile for a Mistral model used via Bedrock.

### `bedrock_qwen_model_profile`

```python
def bedrock_qwen_model_profile(model_name: str) -> ModelProfile | None
```


Get the model profile for a Qwen model used via Bedrock.

### `bedrock_google_model_profile`

```python
def bedrock_google_model_profile(model_name: str) -> ModelProfile | None
```


Get the model profile for a Google model used via Bedrock.

### `bedrock_zai_model_profile`

```python
def bedrock_zai_model_profile(model_name: str) -> ModelProfile | None
```


Get the model profile for a Z.AI (Zhipu) GLM model used via Bedrock.

### `bedrock_moonshotai_model_profile`

```python
def bedrock_moonshotai_model_profile(model_name: str) -> ModelProfile | None
```


Get the model profile for a Moonshot AI Kimi model used via Bedrock.

Registered for both the `moonshot.` and `moonshotai.` Bedrock provider prefixes.

### `bedrock_writer_model_profile`

```python
def bedrock_writer_model_profile(model_name: str) -> ModelProfile | None
```


Get the model profile for a Writer Palmyra model used via Bedrock.

### `bedrock_minimax_model_profile`

```python
def bedrock_minimax_model_profile(model_name: str) -> ModelProfile | None
```


Get the model profile for a MiniMax model used via Bedrock.

### `bedrock_nvidia_model_profile`

```python
def bedrock_nvidia_model_profile(model_name: str) -> ModelProfile | None
```


Get the model profile for an NVIDIA model used via Bedrock.

### `bedrock_openai_model_profile`

```python
def bedrock_openai_model_profile(model_name: str) -> ModelProfile | None
```


Get the model profile for an OpenAI model used via Bedrock Converse.

### `BedrockProvider`

```python
class BedrockProvider
```


Provider for AWS Bedrock.

#### `client`

```python
def client(self) -> BaseClient
```


The boto3 client used to make requests to the Bedrock API.

#### `client`

```python
def client(self, client: BaseClient) -> None
```


Replace the underlying boto3 client.

Useful for rotating short-lived credentials (e.g. temporary STS credentials) in a long-running service:
construct a fresh `bedrock-runtime` client and assign it here, and every [`BedrockConverseModel`]
[pydantic_ai.models.bedrock.BedrockConverseModel] using this provider will pick it up.

### `BedrockMantleModelProfile`

```python
class BedrockMantleModelProfile
```


Profile for OpenAI models served through Amazon Bedrock Mantle.

```python
bedrock_mantle_interface: BedrockMantleInterface
```

### `bedrock_mantle_model_profile`

```python
def bedrock_mantle_model_profile(model_name: str) -> ModelProfile
```


Resolve the profile for an OpenAI model served through Bedrock Mantle.



### `BedrockMantleProvider`

```python
class BedrockMantleProvider
```


Provider for the Amazon Bedrock Mantle OpenAI-compatible API.



### `groq_moonshotai_model_profile`

```python
def groq_moonshotai_model_profile(model_name: str) -> ModelProfile | None
```


Get the model profile for an MoonshotAI model used with the Groq provider.

### `meta_groq_model_profile`

```python
def meta_groq_model_profile(model_name: str) -> ModelProfile | None
```


Get the model profile for a Meta model used with the Groq provider.

### `GroqProvider`

```python
class GroqProvider
```


Provider for Groq API.

### `AzureProvider`

```python
class AzureProvider
```


Provider for Azure OpenAI API.

See <https://azure.microsoft.com/en-us/products/ai-foundry> for more information.

#### `azure_endpoint`

```python
def azure_endpoint(self) -> str
```


The Azure resource endpoint used to derive service-specific URLs.

#### `api_key`

```python
def api_key(self) -> str
```


The Azure resource key, for transports that authenticate with one.

Raises [`UserError`][pydantic_ai.exceptions.UserError] when the provider has no key, i.e. it
was built from a Microsoft Entra ID client (`azure_ad_token` / `azure_ad_token_provider`).

#### `voice_live_endpoint`

```python
def voice_live_endpoint(self) -> str
```


The Azure AI Voice Live endpoint (`AZURE_VOICELIVE_ENDPOINT`, else the Azure OpenAI endpoint).

#### `voice_live_api_key`

```python
def voice_live_api_key(self) -> str
```


The Azure AI Voice Live key (`AZURE_VOICELIVE_API_KEY`, else the Azure OpenAI key).

#### `voice_live_api_version`

```python
def voice_live_api_version(self) -> str
```


The Azure AI Voice Live API version (`AZURE_VOICELIVE_API_VERSION`, else a supported default).

#### `for_realtime`

```python
def for_realtime(cls, *, azure_endpoint: str | None=None, api_version: str | None=None, api_key: str | None=None, entra_authenticated: bool=False, http_client: _OpenAIHTTPClient | None=None) -> Self
```


Create an Azure provider for the GA realtime API.

The realtime transport always uses Azure's `/openai/v1` protocol and does not send an
`api_version`. When neither `api_version` nor `OPENAI_API_VERSION` is set, a bare resource
endpoint is therefore normalized to its `/openai/v1` form before constructing the provider.
Explicit arguments otherwise follow the same environment fallbacks and validation as the
standard constructor.

Args:
    azure_endpoint: The Azure resource endpoint. Falls back to `AZURE_OPENAI_ENDPOINT`.
    api_version: The API version for endpoints that require one. Falls back to
        `OPENAI_API_VERSION`.
    api_key: The Azure resource key. Falls back to `AZURE_OPENAI_API_KEY`.
    entra_authenticated: Set when every request is authenticated with a Microsoft Entra ID
        credential instead of the resource key (see
        [`AzureRealtimeModel(credential=...)`][pydantic_ai.realtime.azure.AzureRealtimeModel]).
        The key is then neither required nor sent, and `api_key` raises its usual explanatory
        error if anything asks — the same state a provider built from an Entra-authenticated
        `openai_client` lands in.
    http_client: An existing `httpx2.AsyncClient` or legacy `httpx.AsyncClient` used to construct the provider client.





### `CohereProvider`

```python
class CohereProvider
```


Provider for Cohere API.

## `VoyageAIProvider`

```python
class VoyageAIProvider
```


Provider for VoyageAI API.

## `SentenceTransformersProvider`

```python
class SentenceTransformersProvider
```


Provider for Sentence Transformers API.

### `name`

```python
def name(self) -> str
```


The provider name.

### `base_url`

```python
def base_url(self) -> str
```


The base URL for the provider API.

### `client`

```python
def client(self) -> Any
```


The client for the provider.## `CerebrasProvider`

```python
class CerebrasProvider
```


Provider for Cerebras API.

## `MistralProvider`

```python
class MistralProvider
```


Provider for Mistral API.

## `FireworksProvider`

```python
class FireworksProvider
```


Provider for Fireworks AI API.## `TogetherProvider`

```python
class TogetherProvider
```


Provider for Together AI API.## `HerokuProvider`

```python
class HerokuProvider
```


Provider for Heroku API.## `GitHubProvider`

```python
class GitHubProvider
```


Provider for the retired GitHub Models API.

GitHub Models was [retired on 2026-07-30](https://docs.github.com/en/github-models); the inference API is no
longer available, so this provider is deprecated and will be removed in v3.

## `GitHubCopilotProvider`

```python
class GitHubCopilotProvider
```


Provider for [GitHub Copilot](https://docs.github.com/en/copilot).

Routes requests through Copilot's OpenAI-compatible Chat Completions API at
`https://api.githubcopilot.com/chat/completions`. Copilot serves Anthropic, OpenAI, Google, xAI and
MoonshotAI models under a subscription, but only the ids whose catalog entry lists `/chat/completions`
under `supported_endpoints` are reachable here; xAI's Grok ids, for one, are served on the Responses
API alone. Which ids you can reach also depends on your plan; list yours with
`GET https://api.githubcopilot.com/models`.

This is not [`GitHubProvider`][pydantic_ai.providers.github.GitHubProvider], which served the
retired GitHub Models API.

## `GitHubCopilotOAuthFlow`

```python
class GitHubCopilotOAuthFlow
```


One GitHub.com device-login flow for a caller-supplied OAuth application.

Construction does no I/O. Call `start`, display the returned challenge, then call
`wait_for_authorization`. No browser is opened and no credentials are persisted.
Use one instance per login attempt; do not call its methods concurrently.



### `start`

```python
async def start(self) -> GitHubCopilotDeviceAuthorization
```


Request a new device code. Replaces any previous challenge on this instance.

The local expiry deadline uses `expires_in` from receipt of the response.
Raises `UserError` for an HTTP failure, rejected client, or malformed response.
Transport errors propagate unchanged.

### `wait_for_authorization`

```python
async def wait_for_authorization(self) -> GitHubCopilotCredentials
```


Poll until approval, rejection, or expiry; cancellation propagates to the caller.

Waits at least GitHub's interval before each request, including the first, and increases
it on `slow_down`. The challenge's original deadline also bounds in-flight requests.
A challenge can be consumed once: call `start` again after success, failure, or cancellation.
Raises `UserError` for expiry, denial, an HTTP failure, or a malformed response.## `GitHubCopilotDeviceAuthorization`

```python
class GitHubCopilotDeviceAuthorization
```


A GitHub device authorization challenge. Display `user_code` at `verification_uri`.

`device_code` is used only by the token exchange and is excluded from `repr`.
`expires_in` and `interval` are seconds, as returned by GitHub.

```python
device_code: Annotated[str, Field(min_length=1)] = field(repr=False)
```

```python
user_code: Annotated[str, Field(min_length=1)]
```

```python
verification_uri: Literal['https://github.com/login/device']
```

```python
expires_in: Annotated[int, Field(strict=True, gt=0)]
```

```python
interval: Annotated[int, Field(strict=True, gt=0)] = 5
```## `GitHubCopilotCredentials`

```python
class GitHubCopilotCredentials
```


GitHub OAuth credentials, with tokens excluded from `repr`.

Pass `access_token` to `GitHubCopilotProvider(api_key=...)`. GitHub authorization does not
establish Copilot entitlement: the inference API checks the account's subscription and policy.
Expiry durations, when present, are seconds from issuance. Applications own persistence and
renewal; the provider does not refresh a token passed through `api_key`.

```python
access_token: Annotated[str, Field(min_length=1)] = field(repr=False)
```

```python
token_type: Literal['bearer']
```

```python
scope: str
```

```python
refresh_token: Annotated[str | None, Field(min_length=1)] = field(default=None, repr=False)
```

```python
expires_in: Annotated[int | None, Field(strict=True, gt=0)] = None
```

```python
refresh_token_expires_in: Annotated[int | None, Field(strict=True, gt=0)] = None
```## `OpenRouterProvider`

```python
class OpenRouterProvider
```


Provider for OpenRouter API.

## `VercelProvider`

```python
class VercelProvider
```


Provider for Vercel AI Gateway API.## `HuggingFaceProvider`

```python
class HuggingFaceProvider
```


Provider for Hugging Face.

## `MoonshotAIProvider`

```python
class MoonshotAIProvider
```


Provider for MoonshotAI platform (Kimi models).## `OllamaProvider`

```python
class OllamaProvider
```


Provider for local or remote Ollama API.

## `LiteLLMProvider`

```python
class LiteLLMProvider
```


Provider for LiteLLM API.

## `VLLMProvider`

```python
class VLLMProvider
```


Provider for local or remote vLLM API.

## `NebiusProvider`

```python
class NebiusProvider
```


Provider for Nebius AI Studio API.## `OVHcloudProvider`

```python
class OVHcloudProvider
```


Provider for OVHcloud AI Endpoints.## `CrusoeProvider`

```python
class CrusoeProvider
```


Provider for Crusoe Serverless Inference API.

## `AlibabaProvider`

```python
class AlibabaProvider
```


Provider for Alibaba Cloud Model Studio (DashScope) OpenAI-compatible API.## `SambaNovaProvider`

```python
class SambaNovaProvider
```


Provider for SambaNova AI models.

SambaNova uses an OpenAI-compatible API.

### `name`

```python
def name(self) -> str
```


Return the provider name.

### `base_url`

```python
def base_url(self) -> str
```


Return the base URL.

### `client`

```python
def client(self) -> AsyncOpenAI
```


Return the AsyncOpenAI client.

### `model_profile`

```python
def model_profile(model_name: str) -> ModelProfile | None
```


Get model profile for SambaNova models.

SambaNova serves models from multiple families including Meta Llama,
DeepSeek, Qwen, and Mistral. Model profiles are matched based on
model name prefixes.

## `SnowflakeProvider`

```python
class SnowflakeProvider
```


Provider for [Snowflake Cortex](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-rest-api).

Routes requests through Snowflake's OpenAI-compatible Chat Completions API at
`https://<account>.snowflakecomputing.com/api/v2/cortex/v1/chat/completions`, which serves
Claude, GPT, Llama, Mistral, DeepSeek, and Snowflake's own models. All inference runs inside
the customer's Snowflake account, so data never leaves the Snowflake security perimeter.

## `TypeSafeProvider`

```python
class TypeSafeProvider
```


Provider for the [TypeSafe](https://typesafe.ai) API, which serves the Jev models.

## `SystemOneProvider`

```python
class SystemOneProvider
```


Provider for the `POST /v1/systemone` decisions API, at a URL of your choosing.

[`SystemOneModel`][pydantic_ai.models.system_one.SystemOneModel] speaks the API; this provider says where it is
and how to authenticate. Decision models such as [Contrastive Language Models](https://huggingface.co/Contrastive-LM/CLM-v0.1-8B) and
[Laya](https://huggingface.co/convaiinnovations/laya) are available over this API, and
[Ollama](https://ollama.com) runs decision models locally over it at `http://localhost:11434`.

### `api_key`

```python
def api_key(self) -> str | None
```


The key sent as a bearer token, if the API needs one.

## `ZaiProvider`

```python
class ZaiProvider
```


Provider for Z.AI (Zhipu AI) API.

Z.AI provides GLM models with support for thinking/reasoning mode
and preserved thinking across turns.

