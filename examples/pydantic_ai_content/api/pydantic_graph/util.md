# `pydantic_graph.util`

Utility types and functions for type manipulation and introspection.

This module provides helper classes and functions for working with Python's type system,
including workarounds for type checker limitations and utilities for runtime type inspection.

### `TypeExpression`

```python
class TypeExpression
```


A workaround for type checker limitations when using complex type expressions.

    This class serves as a wrapper for types that cannot normally be used in positions
requiring `type[T]`, such as `Any`, `Union[...]`, or `Literal[...]`. It provides a
    way to pass these complex type expressions to functions expecting concrete types.

Example:
        Instead of `output_type=Union[str, int]` (which may cause type errors),
        use `output_type=TypeExpression[Union[str, int]]`.

Note:
        This is a workaround for the lack of TypeForm in the Python type system.

### `unpack_type_expression`

```python
def unpack_type_expression(type_: TypeOrTypeExpression[T]) -> type[T]
```


Extract the actual type from a TypeExpression wrapper or return the type directly.

Args:
    type_: Either a direct type or a TypeExpression wrapper.

Returns:
    The unwrapped type, ready for use in runtime type operations.

### `Some`

```python
class Some
```


Container for explicitly present values in Maybe type pattern.

This class represents a value that is definitely present, as opposed to None.
It's part of the Maybe pattern, similar to Option/Maybe in functional programming,
allowing distinction between "no value" (None) and "value is None" (Some(None)).

```python
value: T
```

### `get_callable_name`

```python
def get_callable_name(callable_: Any) -> str
```


Extract a human-readable name from a callable object.

Args:
    callable_: Any callable object (function, method, class, etc.).

Returns:
    The callable's __name__ attribute if available, otherwise its string representation.