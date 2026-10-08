# `pydantic_ai.embeddings`

### `infer_embedding_model`

```python
def infer_embedding_model(model: EmbeddingModel | KnownEmbeddingModelName | str, *, provider_factory: Callable[[str], Provider[Any]]=infer_provider) -> EmbeddingModel
```


Infer the model from the name.

### `Embedder`

```python
class Embedder
```


High-level interface for generating text embeddings.

The `Embedder` class provides a convenient way to generate vector embeddings from text
using various embedding model providers. It handles model inference, settings management,
and optional OpenTelemetry instrumentation.

Example:
```python
from pydantic_ai import Embedder

embedder = Embedder('openai:text-embedding-3-small')


async def main():
    result = await embedder.embed_query('What is machine learning?')
    print(result.embeddings[0][:5])  # First 5 dimensions
    #> [1.0, 1.0, 1.0, 1.0, 1.0]
```

```python
instrument: InstrumentationSettings | bool | None
```

```python
_instrument_default: ClassVar[InstrumentationSettings | bool] = False
```



#### `instrument_all`

```python
def instrument_all(instrument: InstrumentationSettings | bool=True) -> None
```


Set the default instrumentation options for all embedders where `instrument` is not explicitly set.

This is useful for enabling instrumentation globally without modifying each embedder individually.

Args:
    instrument: Instrumentation settings to use as the default. Set to `True` for default settings,
        `False` to disable, or pass an
        [`InstrumentationSettings`][pydantic_ai.models.instrumented.InstrumentationSettings]
        instance to customize.

#### `model`

```python
def model(self) -> EmbeddingModel | KnownEmbeddingModelName | str
```


The embedding model used by this embedder.

#### `override`

```python
def override(self, *, model: EmbeddingModel | KnownEmbeddingModelName | str | _utils.Unset=_utils.UNSET) -> Generator[None]
```


Context manager to temporarily override the embedding model.

Useful for testing or dynamically switching models.

Args:
    model: The embedding model to use within this context.

Example:
```python
from pydantic_ai import Embedder

embedder = Embedder('openai:text-embedding-3-small')


async def main():
    # Temporarily use a different model
    with embedder.override(model='openai:text-embedding-3-large'):
        result = await embedder.embed_query('test')
        print(len(result.embeddings[0]))  # 3072 dimensions for large model
        #> 3072
```

#### `embed_query`

```python
async def embed_query(self, query: str | Sequence[str], *, settings: EmbeddingSettings | None=None) -> EmbeddingResult
```


Embed one or more query texts.

Use this method when embedding search queries that will be compared against document embeddings.
Some models optimize embeddings differently based on whether the input is a query or document.

Args:
    query: A single query string or sequence of query strings to embed.
    settings: Optional settings to override the embedder's default settings for this call.

Returns:
    An [`EmbeddingResult`][pydantic_ai.embeddings.EmbeddingResult] containing the embeddings
    and metadata about the operation.

#### `embed_documents`

```python
async def embed_documents(self, documents: str | Sequence[str], *, settings: EmbeddingSettings | None=None) -> EmbeddingResult
```


Embed one or more document texts.

Use this method when embedding documents that will be stored and later searched against.
Some models optimize embeddings differently based on whether the input is a query or document.

Args:
    documents: A single document string or sequence of document strings to embed.
    settings: Optional settings to override the embedder's default settings for this call.

Returns:
    An [`EmbeddingResult`][pydantic_ai.embeddings.EmbeddingResult] containing the embeddings
    and metadata about the operation.

#### `embed`

```python
async def embed(self, inputs: str | Sequence[str], *, input_type: EmbedInputType, settings: EmbeddingSettings | None=None) -> EmbeddingResult
```


Embed text inputs with explicit input type specification.

This is the low-level embedding method. For most use cases, prefer
[`embed_query()`][pydantic_ai.embeddings.Embedder.embed_query] or
[`embed_documents()`][pydantic_ai.embeddings.Embedder.embed_documents].

Args:
    inputs: A single string or sequence of strings to embed.
    input_type: The type of input, either `'query'` or `'document'`.
    settings: Optional settings to override the embedder's default settings for this call.

Returns:
    An [`EmbeddingResult`][pydantic_ai.embeddings.EmbeddingResult] containing the embeddings
    and metadata about the operation.

#### `max_input_tokens`

```python
async def max_input_tokens(self) -> int | None
```


Get the maximum number of tokens the model can accept as input.

Returns:
    The maximum token count, or `None` if the limit is unknown for this model.

#### `count_tokens`

```python
async def count_tokens(self, text: str) -> int
```


Count the number of tokens in the given text.

Args:
    text: The text to tokenize and count.

Returns:
    The number of tokens in the text.

Raises:
    NotImplementedError: If the model doesn't support token counting.
    UserError: If the model or tokenizer is not supported.

#### `embed_query_sync`

```python
def embed_query_sync(self, query: str | Sequence[str], *, settings: EmbeddingSettings | None=None) -> EmbeddingResult
```


Synchronous version of [`embed_query()`][pydantic_ai.embeddings.Embedder.embed_query].

#### `embed_documents_sync`

```python
def embed_documents_sync(self, documents: str | Sequence[str], *, settings: EmbeddingSettings | None=None) -> EmbeddingResult
```


Synchronous version of [`embed_documents()`][pydantic_ai.embeddings.Embedder.embed_documents].

#### `embed_sync`

```python
def embed_sync(self, inputs: str | Sequence[str], *, input_type: EmbedInputType, settings: EmbeddingSettings | None=None) -> EmbeddingResult
```


Synchronous version of [`embed()`][pydantic_ai.embeddings.Embedder.embed].

#### `max_input_tokens_sync`

```python
def max_input_tokens_sync(self) -> int | None
```


Synchronous version of [`max_input_tokens()`][pydantic_ai.embeddings.Embedder.max_input_tokens].

#### `count_tokens_sync`

```python
def count_tokens_sync(self, text: str) -> int
```


Synchronous version of [`count_tokens()`][pydantic_ai.embeddings.Embedder.count_tokens].

### `EmbeddingModel`

```python
class EmbeddingModel
```


Abstract base class for embedding models.

Implement this class to create a custom embedding model. For most use cases,
use one of the built-in implementations:

- [`OpenAIEmbeddingModel`][pydantic_ai.embeddings.openai.OpenAIEmbeddingModel]
- [`CohereEmbeddingModel`][pydantic_ai.embeddings.cohere.CohereEmbeddingModel]
- [`GoogleEmbeddingModel`][pydantic_ai.embeddings.google.GoogleEmbeddingModel]
- [`BedrockEmbeddingModel`][pydantic_ai.embeddings.bedrock.BedrockEmbeddingModel]
- [`SentenceTransformerEmbeddingModel`][pydantic_ai.embeddings.sentence_transformers.SentenceTransformerEmbeddingModel]

```python
_settings: EmbeddingSettings | None = None
```



#### `settings`

```python
def settings(self) -> EmbeddingSettings | None
```


Get the default settings for this model.

#### `base_url`

```python
def base_url(self) -> str | None
```


The base URL for the provider API, if available.

#### `model_name`

```python
def model_name(self) -> str
```


The name of the embedding model.

#### `system`

```python
def system(self) -> str
```


The embedding model provider/system identifier (e.g., 'openai', 'cohere').

#### `embed`

```python
async def embed(self, inputs: str | Sequence[str], *, input_type: EmbedInputType, settings: EmbeddingSettings | None=None) -> EmbeddingResult
```


Generate embeddings for the given inputs.

Args:
    inputs: A single string or sequence of strings to embed.
    input_type: Whether the inputs are queries or documents.
    settings: Optional settings to override the model's defaults.

Returns:
    An [`EmbeddingResult`][pydantic_ai.embeddings.EmbeddingResult] containing
    the embeddings and metadata.

#### `prepare_embed`

```python
def prepare_embed(self, inputs: str | Sequence[str], settings: EmbeddingSettings | None=None) -> tuple[list[str], EmbeddingSettings]
```


Prepare the inputs and settings for embedding.

This method normalizes inputs to a list and merges settings.
Subclasses should call this at the start of their `embed()` implementation.

Args:
    inputs: A single string or sequence of strings.
    settings: Optional settings to merge with defaults.

Returns:
    A tuple of (normalized inputs list, merged settings).

#### `max_input_tokens`

```python
async def max_input_tokens(self) -> int | None
```


Get the maximum number of tokens that can be input to the model.

Returns:
    The maximum token count, or `None` if unknown.

#### `count_tokens`

```python
async def count_tokens(self, text: str) -> int
```


Count the number of tokens in the given text.

Args:
    text: The text to tokenize and count.

Returns:
    The number of tokens.

Raises:
    NotImplementedError: If the model doesn't support token counting.
    UserError: If the model or tokenizer is not supported.### `EmbeddingResult`

```python
class EmbeddingResult
```


The result of an embedding operation.

This class contains the generated embeddings along with metadata about
the operation, including the original inputs, model information, usage
statistics, and timing.

Example:
```python
from pydantic_ai import Embedder

embedder = Embedder('openai:text-embedding-3-small')


async def main():
    result = await embedder.embed_query('What is AI?')

    # Access embeddings by index
    print(len(result.embeddings[0]))
    #> 1536

    # Access embeddings by original input text
    print(result['What is AI?'] == result.embeddings[0])
    #> True

    # Check usage
    print(f'Tokens used: {result.usage.input_tokens}')
    #> Tokens used: 3
```

```python
embeddings: Sequence[Sequence[float]]
```

```python
_: KW_ONLY
```

```python
inputs: Sequence[str]
```

```python
input_type: EmbedInputType
```

```python
model_name: str
```

```python
provider_name: str
```

```python
timestamp: datetime = field(default_factory=_now_utc)
```

```python
usage: RequestUsage = field(default_factory=RequestUsage)
```

```python
provider_details: dict[str, Any] | None = None
```

```python
provider_response_id: str | None = None
```



#### `cost`

```python
def cost(self) -> genai_types.PriceCalculation
```


Calculate the cost of the embedding request.

Uses [`genai-prices`](https://github.com/pydantic/genai-prices) for pricing data.

Returns:
    A price calculation object with `total_price`, `input_price`, and other cost details.

Raises:
    LookupError: If pricing data is not available for this model/provider.### `EmbeddingSettings`

```python
class EmbeddingSettings
```


Common settings for configuring embedding models.

These settings apply across multiple embedding model providers.
Not all settings are supported by all models - check the specific
model's documentation for details.

Provider-specific settings classes (e.g.,
[`OpenAIEmbeddingSettings`][pydantic_ai.embeddings.openai.OpenAIEmbeddingSettings],
[`CohereEmbeddingSettings`][pydantic_ai.embeddings.cohere.CohereEmbeddingSettings])
extend this with additional provider-prefixed options.

```python
dimensions: int
```

```python
truncate: bool
```

```python
extra_headers: dict[str, str]
```

```python
extra_body: object
```

### `merge_embedding_settings`

```python
def merge_embedding_settings(base: EmbeddingSettings | None, overrides: EmbeddingSettings | None) -> EmbeddingSettings | None
```


Merge two sets of embedding settings, with overrides taking precedence.

Args:
    base: Base settings (typically from the embedder or model).
    overrides: Settings that should override the base (typically per-call settings).

Returns:
    Merged settings, or `None` if both inputs are `None`.### `OpenAIEmbeddingSettings`

```python
class OpenAIEmbeddingSettings
```


Settings used for an OpenAI embedding model request.

All fields from [`EmbeddingSettings`][pydantic_ai.embeddings.EmbeddingSettings] are supported.

### `OpenAIEmbeddingModel`

```python
class OpenAIEmbeddingModel
```


OpenAI embedding model implementation.

This model works with OpenAI's embeddings API and any
[OpenAI-compatible providers](../models/openai.md#openai-compatible-models).

Example:
```python
from pydantic_ai.embeddings.openai import OpenAIEmbeddingModel
from pydantic_ai.providers.openai import OpenAIProvider

# Using OpenAI directly
model = OpenAIEmbeddingModel('text-embedding-3-small')

# Using an OpenAI-compatible provider
model = OpenAIEmbeddingModel(
    'text-embedding-3-small',
    provider=OpenAIProvider(base_url='https://my-provider.com/v1'),
)
```

```python
_model_name: OpenAIEmbeddingModelName = field(repr=False)
```

```python
_provider: Provider[AsyncOpenAI] = field(repr=False)
```



#### `model_name`

```python
def model_name(self) -> OpenAIEmbeddingModelName
```


The embedding model name.

#### `system`

```python
def system(self) -> str
```


The embedding model provider.### `CohereEmbeddingSettings`

```python
class CohereEmbeddingSettings
```


Settings used for a Cohere embedding model request.

All fields from [`EmbeddingSettings`][pydantic_ai.embeddings.EmbeddingSettings] are supported,
plus Cohere-specific settings prefixed with `cohere_`.

```python
cohere_max_tokens: int
```

```python
cohere_input_type: CohereEmbedInputType
```

```python
cohere_truncate: V2EmbedRequestTruncate
```

### `CohereEmbeddingModel`

```python
class CohereEmbeddingModel
```


Cohere embedding model implementation.

This model works with Cohere's embeddings API, which offers
multilingual support and various model sizes.

Example:
```python
from pydantic_ai.embeddings.cohere import CohereEmbeddingModel

model = CohereEmbeddingModel('embed-v4.0')
```

```python
_model_name: CohereEmbeddingModelName = field(repr=False)
```

```python
_provider: Provider[AsyncClientV2] = field(repr=False)
```



#### `base_url`

```python
def base_url(self) -> str
```


The base URL for the provider API, if available.

#### `model_name`

```python
def model_name(self) -> CohereEmbeddingModelName
```


The embedding model name.

#### `system`

```python
def system(self) -> str
```


The embedding model provider.### `GoogleEmbeddingSettings`

```python
class GoogleEmbeddingSettings
```


Settings used for a Google embedding model request.

All fields from [`EmbeddingSettings`][pydantic_ai.embeddings.EmbeddingSettings] are supported,
plus Google-specific settings prefixed with `google_`.

```python
google_task: GoogleEmbeddingTask
```

```python
google_task_type: str
```

```python
google_title: str
```

### `GoogleEmbeddingModel`

```python
class GoogleEmbeddingModel
```


Google embedding model implementation.

This model works with Google's embeddings API via the `google-genai` SDK,
supporting both the Gemini API (Google AI Studio) and Google Cloud (formerly known as Vertex AI).

Example:
```python
from pydantic_ai.embeddings.google import GoogleEmbeddingModel
from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai.providers.google_cloud import GoogleCloudProvider

# Using the Gemini API (requires GOOGLE_API_KEY env var)
model = GoogleEmbeddingModel('gemini-embedding-001', provider=GoogleProvider())

# Using Google Cloud
model = GoogleEmbeddingModel(
    'gemini-embedding-001',
    provider=GoogleCloudProvider(project='my-project', location='us-central1'),
)
```

```python
_model_name: GoogleEmbeddingModelName = field(repr=False)
```

```python
_provider: Provider[Client] = field(repr=False)
```



#### `model_name`

```python
def model_name(self) -> GoogleEmbeddingModelName
```


The embedding model name.

#### `system`

```python
def system(self) -> str
```


The embedding model provider.

### `BedrockEmbeddingSettings`

```python
class BedrockEmbeddingSettings
```


Settings used for a Bedrock embedding model request.

All fields from [`EmbeddingSettings`][pydantic_ai.embeddings.EmbeddingSettings] are supported,
plus Bedrock-specific settings prefixed with `bedrock_`.

All settings are optional - if not specified, model defaults are used.

**Note on `dimensions` parameter support:**

- **Titan v1** (`amazon.titan-embed-text-v1`): Not supported (fixed: 1536)
- **Titan v2** (`amazon.titan-embed-text-v2:0`): Supported (default: 1024, accepts 256/384/1024)
- **Cohere v3** (`cohere.embed-english-v3`, `cohere.embed-multilingual-v3`): Not supported (fixed: 1024)
- **Cohere v4** (`cohere.embed-v4:0`): Supported (default: 1536, accepts 256/512/1024/1536)
- **Nova** (`amazon.nova-2-multimodal-embeddings-v1:0`): Supported (default: 3072, accepts 256/384/1024/3072)

Unsupported settings are silently ignored.

**Note on `truncate` parameter support:**

- **Titan models** (`amazon.titan-embed-text-v1`, `amazon.titan-embed-text-v2:0`): Not supported
- **Cohere models** (all versions): Supported (default: `False`, maps to `'END'` when `True`)
- **Nova** (`amazon.nova-2-multimodal-embeddings-v1:0`): Supported (default: `False`, maps to `'END'` when `True`)

For fine-grained truncation control, use model-specific settings: `bedrock_cohere_truncate` or `bedrock_nova_truncate`.

Example:
    ```python
    from pydantic_ai.embeddings.bedrock import BedrockEmbeddingSettings

    # Use model defaults
    settings = BedrockEmbeddingSettings()

    # Customize specific settings for Titan v2:0
    settings = BedrockEmbeddingSettings(
        dimensions=512,
        bedrock_titan_normalize=True,
    )

    # Customize specific settings for Cohere v4
    settings = BedrockEmbeddingSettings(
        dimensions=512,
        bedrock_cohere_max_tokens=1000,
    )
    ```

```python
bedrock_titan_normalize: bool
```

```python
bedrock_cohere_max_tokens: int
```

```python
bedrock_cohere_input_type: Literal['search_document', 'search_query', 'classification', 'clustering']
```

```python
bedrock_cohere_truncate: Literal['NONE', 'START', 'END']
```

```python
bedrock_nova_truncate: Literal['NONE', 'START', 'END']
```

```python
bedrock_nova_embedding_purpose: Literal['GENERIC_INDEX', 'GENERIC_RETRIEVAL', 'TEXT_RETRIEVAL', 'CLASSIFICATION', 'CLUSTERING']
```

```python
bedrock_inference_profile: str
```

```python
bedrock_max_concurrency: int
```













### `BedrockEmbeddingModel`

```python
class BedrockEmbeddingModel
```


Bedrock embedding model implementation.

This model works with AWS Bedrock's embedding models including
Amazon Titan Embeddings and Cohere Embed models.

Example:
```python
from pydantic_ai.embeddings.bedrock import BedrockEmbeddingModel
from pydantic_ai.providers.bedrock import BedrockProvider

# Using default AWS credentials
model = BedrockEmbeddingModel('amazon.titan-embed-text-v2:0')

# Using explicit credentials
model = BedrockEmbeddingModel(
    'cohere.embed-english-v3',
    provider=BedrockProvider(
        region_name='us-east-1',
        aws_access_key_id='...',
        aws_secret_access_key='...',
    ),
)
```

```python
_model_name: BedrockEmbeddingModelName = field(repr=False)
```

```python
_provider: Provider[BaseClient] = field(repr=False)
```

```python
_handler: _BedrockEmbeddingHandler = field(repr=False)
```



#### `base_url`

```python
def base_url(self) -> str
```


The base URL for the provider API.

#### `model_name`

```python
def model_name(self) -> BedrockEmbeddingModelName
```


The embedding model name.

#### `system`

```python
def system(self) -> str
```


The embedding model provider.







#### `max_input_tokens`

```python
async def max_input_tokens(self) -> int | None
```


Get the maximum number of tokens that can be input to the model.### `VoyageAIEmbeddingSettings`

```python
class VoyageAIEmbeddingSettings
```


Settings used for a VoyageAI embedding model request.

All fields from [`EmbeddingSettings`][pydantic_ai.embeddings.EmbeddingSettings] are supported,
plus VoyageAI-specific settings prefixed with `voyageai_`.

```python
voyageai_input_type: VoyageAIEmbedInputType
```

### `VoyageAIEmbeddingModel`

```python
class VoyageAIEmbeddingModel
```


VoyageAI embedding model implementation.

VoyageAI provides state-of-the-art embedding models optimized for
retrieval, with specialized models for code, finance, and legal domains.

Example:
```python {max_py="3.13"}
from pydantic_ai.embeddings.voyageai import VoyageAIEmbeddingModel

model = VoyageAIEmbeddingModel('voyage-3.5')
```

```python
_model_name: VoyageAIEmbeddingModelName = field(repr=False)
```

```python
_provider: Provider[AsyncClient] = field(repr=False)
```



#### `base_url`

```python
def base_url(self) -> str
```


The base URL for the provider API.

#### `model_name`

```python
def model_name(self) -> VoyageAIEmbeddingModelName
```


The embedding model name.

#### `system`

```python
def system(self) -> str
```


The embedding model provider.### `SentenceTransformersEmbeddingSettings`

```python
class SentenceTransformersEmbeddingSettings
```


Settings used for a Sentence-Transformers embedding model request.

All fields from [`EmbeddingSettings`][pydantic_ai.embeddings.EmbeddingSettings] are supported,
plus Sentence-Transformers-specific settings prefixed with `sentence_transformers_`.

```python
sentence_transformers_device: str
```

```python
sentence_transformers_normalize_embeddings: bool
```

```python
sentence_transformers_batch_size: int
```

### `SentenceTransformerEmbeddingModel`

```python
class SentenceTransformerEmbeddingModel
```


Local embedding model using the `sentence-transformers` library.

This model runs embeddings locally on your machine, which is useful for:

- Privacy-sensitive applications where data shouldn't leave your infrastructure
- Reducing API costs for high-volume embedding workloads
- Offline or air-gapped environments

Models are downloaded from Hugging Face on first use.
See the [Sentence-Transformers documentation](https://www.sbert.net/docs/sentence_transformer/pretrained_models.html)
for available models.

Example:
```python {max_py="3.13"}
from sentence_transformers import SentenceTransformer

from pydantic_ai.embeddings.sentence_transformers import (
    SentenceTransformerEmbeddingModel,
)

# Using a model name (downloads from Hugging Face)
model = SentenceTransformerEmbeddingModel('sentence-transformers/all-MiniLM-L6-v2')

# Using an existing SentenceTransformer instance
st_model = SentenceTransformer('Qwen/Qwen3-Embedding-0.6B')
model = SentenceTransformerEmbeddingModel(st_model)
```

```python
_model_name: str = field(repr=False)
```

```python
_model: SentenceTransformer | None = field(repr=False, default=None)
```



#### `base_url`

```python
def base_url(self) -> str | None
```


No base URL — runs locally.

#### `model_name`

```python
def model_name(self) -> str
```


The embedding model name.

#### `system`

```python
def system(self) -> str
```


The embedding model provider/system identifier.

### `TestEmbeddingModel`

```python
class TestEmbeddingModel
```


A mock embedding model for testing.

This model returns deterministic embeddings (all 1.0 values) and tracks
the settings used in the last call via the `last_settings` attribute.

Example:
```python
from pydantic_ai import Embedder
from pydantic_ai.embeddings import TestEmbeddingModel

test_model = TestEmbeddingModel()
embedder = Embedder('openai:text-embedding-3-small')


async def main():
    with embedder.override(model=test_model):
        await embedder.embed_query('test')
        assert test_model.last_settings is not None
```

```python
_model_name: str
```

```python
_provider_name: str
```

```python
_dimensions: int
```

```python
last_settings: EmbeddingSettings | None = None
```



#### `model_name`

```python
def model_name(self) -> str
```


The embedding model name.

#### `system`

```python
def system(self) -> str
```


The embedding model provider.### `WrapperEmbeddingModel`

```python
class WrapperEmbeddingModel
```


Base class for embedding models that wrap another model.

Use this as a base class to create custom embedding model wrappers
that modify behavior (e.g., caching, logging, rate limiting) while
delegating to an underlying model.

By default, all methods are passed through to the wrapped model.
Override specific methods to customize behavior.

```python
wrapped: EmbeddingModel
```



#### `settings`

```python
def settings(self) -> EmbeddingSettings | None
```


Get the settings from the wrapped embedding model.### `instrument_embedding_model`

```python
def instrument_embedding_model(model: EmbeddingModel, instrument: InstrumentationSettings | bool) -> EmbeddingModel
```


Instrument an embedding model with OpenTelemetry/logfire.

### `InstrumentedEmbeddingModel`

```python
class InstrumentedEmbeddingModel
```


Embedding model which wraps another model so that requests are instrumented with OpenTelemetry.

See the [Debugging and Monitoring guide](https://pydantic.dev/docs/ai/integrations/logfire/) for more info.

```python
instrumentation_settings: InstrumentationSettings
```