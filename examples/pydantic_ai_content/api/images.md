# `pydantic_ai.images`

### `infer_image_generation_model`

```python
def infer_image_generation_model(model: ImageGenerationModel | KnownImageGenerationModelName | str, *, provider_factory: Callable[[str], Provider[Any]]=infer_provider) -> ImageGenerationModel
```


Infer the image generation model from the name.

### `ImageGenerator`

```python
class ImageGenerator
```


High-level interface for generating images.

The `ImageGenerator` class provides a convenient way to generate images from a prompt, and to edit
or transform reference images, using dedicated image models. It handles model inference, settings
management, and optional OpenTelemetry instrumentation.

Example:
```python
from pydantic_ai import ImageGenerator

generator = ImageGenerator('openai:gpt-image-2')


async def main():
    result = await generator.generate('A watercolor map of a floating city.')
    print(result.image.media_type)
    #> image/png
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


Set the default instrumentation options for all image generators where `instrument` is not explicitly set.

This is useful for enabling instrumentation globally without modifying each generator individually.

Args:
    instrument: Instrumentation settings to use as the default. Set to `True` for default settings,
        `False` to disable, or pass an
        [`InstrumentationSettings`][pydantic_ai.models.instrumented.InstrumentationSettings]
        instance to customize.

#### `model`

```python
def model(self) -> ImageGenerationModel | KnownImageGenerationModelName | str
```


The image generation model used by this generator.

#### `override`

```python
def override(self, *, model: ImageGenerationModel | KnownImageGenerationModelName | str | _utils.Unset=_utils.UNSET) -> Generator[None]
```


Context manager to temporarily override the image generation model.

Useful for testing or dynamically switching models.

Args:
    model: The image generation model to use within this context.

Example:
```python
from pydantic_ai import ImageGenerator

generator = ImageGenerator('openai:gpt-image-2')


async def main():
    # Temporarily use a different model
    with generator.override(model='google:gemini-3.1-flash-image'):
        result = await generator.generate('A watercolor map of a floating city.')
        print(result.model_name)
        #> gemini-3.1-flash-image
```

#### `generate`

```python
async def generate(self, prompt: str, *, images: Sequence[ImageGenerationInput] | None=None, settings: ImageGenerationSettings | None=None) -> ImageGenerationResult
```


Generate images from a prompt and optional reference images.

Args:
    prompt: The text prompt describing the image to generate.
    images: Optional reference images to edit or transform. Passing reference images sends the
        request to the provider's image-editing path, preserving the order of the images. Each
        item can be a [`BinaryImage`][pydantic_ai.messages.BinaryImage],
        [`ImageUrl`][pydantic_ai.messages.ImageUrl], or
        [`UploadedFile`][pydantic_ai.messages.UploadedFile]; see the
        [Image Generation guide](../image-generation.md#editing-images) for the reference-input
        types each provider accepts.
    settings: Optional settings to override the generator's default settings for this call.

Returns:
    An [`ImageGenerationResult`][pydantic_ai.images.ImageGenerationResult] containing the
    generated images and metadata about the operation.

Raises:
    ContentFilterError: If the provider blocked the request, or every generated image, for
        content moderation.
    UserError: If the prompt is empty, a setting is invalid, or the model cannot produce the
        requested dimensions.

#### `generate_sync`

```python
def generate_sync(self, prompt: str, *, images: Sequence[ImageGenerationInput] | None=None, settings: ImageGenerationSettings | None=None) -> ImageGenerationResult
```


Synchronous version of [`generate()`][pydantic_ai.images.ImageGenerator.generate].

Args:
    prompt: The text prompt describing the image to generate.
    images: Optional reference images to edit or transform.
    settings: Optional settings to override the generator's default settings for this call.

Returns:
    An [`ImageGenerationResult`][pydantic_ai.images.ImageGenerationResult] containing the
    generated images and metadata about the operation.

Raises:
    ContentFilterError: If the provider blocked the request, or every generated image, for
        content moderation.
    UserError: If the prompt is empty, a setting is invalid, or the model cannot produce the
        requested dimensions.

### `ImageGenerationModel`

```python
class ImageGenerationModel
```


Abstract base class for image generation models.

```python
_settings: ImageGenerationSettings | None = None
```



#### `settings`

```python
def settings(self) -> ImageGenerationSettings | None
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


The name of the image generation model.

#### `system`

```python
def system(self) -> str
```


The image generation model provider/system identifier.

#### `generate`

```python
async def generate(self, prompt: str, *, images: Sequence[ImageGenerationInput] | None=None, settings: ImageGenerationSettings | None=None) -> ImageGenerationResult
```


Generate images for the given prompt.

The result always holds at least one image. An implementation with no image to return raises
[`ContentFilterError`][pydantic_ai.exceptions.ContentFilterError] when the provider blocked the output, and
[`UnexpectedModelBehavior`][pydantic_ai.exceptions.UnexpectedModelBehavior] otherwise, rather than returning an
empty result.



#### `prepare_generate`

```python
def prepare_generate(self, prompt: str, *, images: Sequence[ImageGenerationInput] | None=None, settings: ImageGenerationSettings | None=None) -> tuple[str, list[ImageGenerationInput], ImageGenerationSettings]
```


Prepare the prompt, reference images, and settings for image generation.### `GeneratedImage`

```python
class GeneratedImage
```


One generated image with normalized content and provider metadata.

```python
content: BinaryImage
```

```python
_: KW_ONLY
```

```python
revised_prompt: str | None = None
```

```python
output_format: str | None = None
```

```python
provider_details: dict[str, Any] | None = None
```

### `ImageGenerationResult`

```python
class ImageGenerationResult
```


The result of an image generation operation.

```python
images: Sequence[GeneratedImage]
```

```python
_: KW_ONLY
```

```python
prompt: str
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

```python
provider_url: str | None = None
```

#### `image`

```python
def image(self) -> BinaryImage
```


The first generated image. Use `images` when the request asked for more than one.

A result always holds at least one image: the
[`ImageGenerationModel.generate`][pydantic_ai.images.ImageGenerationModel.generate] contract
requires an implementation with nothing to return to raise instead of returning an empty result.

#### `cost`

```python
def cost(self) -> genai_types.PriceCalculation
```


Calculate the cost of the image generation request.

Uses [`genai-prices`](https://github.com/pydantic/genai-prices) for pricing data.

Models priced per token are covered, such as the GPT Image and Gemini image families. The
Grok Imagine family raises `LookupError`: it has no entry in the pricing data, and there is
no unit that counts generated images to price it with.

Returns:
    A price calculation object with `total_price`, `input_price`, and other cost details.

Raises:
    LookupError: If pricing data is not available for this model/provider.### `ImageGenerationSettings`

```python
class ImageGenerationSettings
```


Normalized settings for configuring image generation models.

This type contains only settings with the same semantics across every direct
image provider. Provider-specific settings classes extend it with prefixed
options for controls that are not portable.

```python
dimensions: ImageDimensions
```

```python
aspect_ratio: ImageGenerationAspectRatio
```

```python
extra_headers: dict[str, str]
```

```python
extra_body: object
```

### `merge_image_generation_settings`

```python
def merge_image_generation_settings(base: ImageGenerationSettings | None, overrides: ImageGenerationSettings | None) -> ImageGenerationSettings | None
```


Merge two sets of image generation settings, with overrides taking precedence.### `OpenAIImageGenerationSettings`

```python
class OpenAIImageGenerationSettings
```


Settings used for an OpenAI image generation request.

All fields from [`ImageGenerationSettings`][pydantic_ai.images.ImageGenerationSettings]
are supported, plus OpenAI-specific settings prefixed with `openai_`.

```python
openai_n: int
```

```python
openai_output_format: OpenAIImageOutputFormat
```

```python
openai_size: str
```

```python
openai_quality: Literal['low', 'medium', 'high', 'auto']
```

```python
openai_background: Literal['transparent', 'opaque', 'auto']
```

```python
openai_input_fidelity: Literal['high', 'low']
```

```python
openai_moderation: Literal['auto', 'low']
```

```python
openai_output_compression: int
```

```python
openai_user: str
```

### `OpenAIImageGenerationModel`

```python
class OpenAIImageGenerationModel
```


OpenAI image generation model implementation.

This model works with OpenAI's Images API and the GPT Image model family, such as `gpt-image-2`,
`gpt-image-1.5`, `gpt-image-1`, and `gpt-image-1-mini`.

The `dall-e-2` and `dall-e-3` models are not supported and raise a
[`UserError`][pydantic_ai.exceptions.UserError] on construction, even though they are part of the
OpenAI SDK's `ImageModel` type: they diverge from the GPT Image request and response contract in
size, quality, image count, and response format. Unrecognized model names are passed through to
OpenAI, so newly released GPT Image models work without a Pydantic AI release.

Example:
```python
from pydantic_ai.images.openai import OpenAIImageGenerationModel
from pydantic_ai.providers.openai import OpenAIProvider

# Using OpenAI directly
model = OpenAIImageGenerationModel('gpt-image-2')

# Using a custom base URL or client configuration
model = OpenAIImageGenerationModel(
    'gpt-image-2',
    provider=OpenAIProvider(base_url='https://my-provider.com/v1'),
)
```

```python
_model_name: OpenAIImageGenerationModelName = field(repr=False)
```

```python
_provider: Provider[AsyncOpenAI] = field(repr=False)
```



#### `model_name`

```python
def model_name(self) -> OpenAIImageGenerationModelName
```


The image generation model name.

#### `system`

```python
def system(self) -> str
```


The image generation model provider.

### `GoogleImageGenerationSettings`

```python
class GoogleImageGenerationSettings
```


Settings used for a Google image generation request.

All fields from [`ImageGenerationSettings`][pydantic_ai.images.ImageGenerationSettings]
are supported, plus Google-specific settings prefixed with `google_`.

```python
google_image_config: ImageConfigDict
```

### `GoogleImageGenerationModel`

```python
class GoogleImageGenerationModel
```


Google Gemini image generation model implementation.

This model works with the Gemini image models, such as `gemini-3.1-flash-image` and
`gemini-3-pro-image`, through the Gemini Developer API (Google AI Studio) or Google Cloud
(Vertex AI). It asks Gemini for an image-only response, as
[`ImageGenerator`][pydantic_ai.images.ImageGenerator] returns generated images rather than
Gemini's optional conversational text.

Example:
```python
from pydantic_ai.images.google import GoogleImageGenerationModel
from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai.providers.google_cloud import GoogleCloudProvider

# Using the Gemini API (requires GOOGLE_API_KEY env var)
model = GoogleImageGenerationModel('gemini-3.1-flash-image')

# Or with explicit provider configuration
model = GoogleImageGenerationModel(
    'gemini-3.1-flash-image',
    provider=GoogleProvider(api_key='your-api-key'),
)

# Using Google Cloud (Vertex AI)
model = GoogleImageGenerationModel(
    'gemini-3.1-flash-image',
    provider=GoogleCloudProvider(project='my-project', location='global'),
)
```

```python
_model_name: GoogleImageGenerationModelName = field(repr=False)
```

```python
_provider: Provider[Client] = field(repr=False)
```



#### `model_name`

```python
def model_name(self) -> GoogleImageGenerationModelName
```


The image generation model name.

#### `system`

```python
def system(self) -> str
```


The image generation model provider.





### `XaiImageGenerationSettings`

```python
class XaiImageGenerationSettings
```


Settings used for an xAI image generation request.

All fields from [`ImageGenerationSettings`][pydantic_ai.images.ImageGenerationSettings]
are supported, plus xAI-specific settings prefixed with `xai_`.

```python
xai_n: int
```

```python
xai_user: str
```

```python
xai_aspect_ratio: XaiImageAspectRatio
```

```python
xai_resolution: ImageResolution
```



### `XaiImageGenerationModel`

```python
class XaiImageGenerationModel
```


xAI image generation model implementation.

This model works with the Grok Imagine models, such as `grok-imagine-image` and
`grok-imagine-image-quality`, through the official xAI SDK, which connects over gRPC.

xAI moderates silently: a flagged image in a batch comes back empty rather than as an error, so the
clean images are returned and the flagged positions are reported through
`provider_details['moderated_image_indices']`. A
[`ContentFilterError`][pydantic_ai.exceptions.ContentFilterError] is raised only when every image
was flagged. See the [xAI model page](../models/xai.md#image-generation) for details.

Example:
```python
from pydantic_ai.images.xai import XaiImageGenerationModel
from pydantic_ai.providers.xai import XaiProvider

# Using xAI directly (requires XAI_API_KEY env var)
model = XaiImageGenerationModel('grok-imagine-image')

# Or with explicit provider configuration
model = XaiImageGenerationModel(
    'grok-imagine-image',
    provider=XaiProvider(api_key='your-api-key'),
)
```

```python
_model_name: XaiImageGenerationModelName = field(repr=False)
```

```python
_provider: Provider[AsyncClient] = field(repr=False)
```



#### `model_name`

```python
def model_name(self) -> XaiImageGenerationModelName
```


The image generation model name.

#### `system`

```python
def system(self) -> str
```


The image generation model provider.

### `TestImageGenerationModel`

```python
class TestImageGenerationModel
```


A deterministic image generation model for testing.

This model returns a single 1x1 PNG without making any API calls, and records the reference images
and settings used in the last call via the `last_images` and `last_settings` attributes.

Example:
```python
from pydantic_ai import ImageGenerator
from pydantic_ai.images import TestImageGenerationModel

test_model = TestImageGenerationModel()
generator = ImageGenerator('openai:gpt-image-2')


async def main():
    with generator.override(model=test_model):
        await generator.generate('A test image', settings={'aspect_ratio': '16:9'})
        print(test_model.last_settings)
        #> {'aspect_ratio': '16:9'}
        print(test_model.last_images)
        #> []
```

```python
_model_name: str
```

```python
_provider_name: str
```

```python
last_images: list[ImageGenerationInput]
```

```python
last_settings: ImageGenerationSettings | None = None
```



#### `model_name`

```python
def model_name(self) -> str
```


The image generation model name.

#### `system`

```python
def system(self) -> str
```


The image generation model provider.### `WrapperImageGenerationModel`

```python
class WrapperImageGenerationModel
```


Base class for image generation models that wrap another model.

Use this as a base class to create custom image generation model wrappers
that modify behavior (e.g., caching, logging, rate limiting) while
delegating to an underlying model.

By default, all methods are passed through to the wrapped model.
Override specific methods to customize behavior.

```python
wrapped: ImageGenerationModel
```



#### `settings`

```python
def settings(self) -> ImageGenerationSettings | None
```


Get the settings from the wrapped image generation model.### `instrument_image_generation_model`

```python
def instrument_image_generation_model(model: ImageGenerationModel, instrument: InstrumentationSettings | bool) -> ImageGenerationModel
```


Instrument an image generation model with OpenTelemetry/logfire.

### `InstrumentedImageGenerationModel`

```python
class InstrumentedImageGenerationModel
```


Image generation model which wraps another model for OpenTelemetry instrumentation.

```python
instrumentation_settings: InstrumentationSettings
```