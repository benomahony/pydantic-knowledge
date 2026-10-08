# `pydantic_evals.generation`

Utilities for generating example datasets for pydantic_evals.

This module provides functions for generating sample datasets for testing and examples,
using LLMs to create realistic test data with proper structure.

### `generate_dataset`

```python
async def generate_dataset(*, dataset_type: type[Dataset[InputsT, OutputT, MetadataT]], path: Path | str | None=None, custom_evaluator_types: Sequence[type[Evaluator[InputsT, OutputT, MetadataT]]]=(), model: models.Model | models.KnownModelName='openai:gpt-5.2', n_examples: int=3, extra_instructions: str | None=None) -> Dataset[InputsT, OutputT, MetadataT]
```


Use an LLM to generate a dataset of test cases, each consisting of input, expected output, and metadata.

This function creates a properly structured dataset with the specified input, output, and metadata types.
It uses an LLM to attempt to generate realistic test cases that conform to the types' schemas.

Args:
    path: Optional path to save the generated dataset. If provided, the dataset will be saved to this location.
    dataset_type: The type of dataset to generate, with the desired input, output, and metadata types.
    custom_evaluator_types: Optional sequence of custom evaluator classes to include in the schema.
    model: The Pydantic AI model to use for generation. Defaults to 'openai:gpt-5.2'.
    n_examples: Number of examples to generate. Defaults to 3.
    extra_instructions: Optional additional instructions to provide to the LLM.

Returns:
    A properly structured Dataset object with generated test cases.

Raises:
    ValidationError: If the LLM's response cannot be parsed as a valid dataset.