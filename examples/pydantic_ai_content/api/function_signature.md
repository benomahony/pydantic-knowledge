# `pydantic_ai.function_signature`

Generate function signatures from functions and JSON schemas.

This module provides utilities to represent tool definitions as human-readable
function signatures, which LLMs can understand more easily than raw
JSON schemas. Used by code mode to present tools as callable functions.

### `SimpleTypeExpr`

```python
class SimpleTypeExpr
```


A simple named type like `str`, `int`, `Any`, `None`.

```python
name: SimpleTypeName
```

```python
kind: Literal['simple'] = 'simple'
```

### `LiteralTypeExpr`

```python
class LiteralTypeExpr
```


A Literal type expression like `Literal['a', 'b']` or `Literal[42]`.

```python
values: list[Any]
```

```python
kind: Literal['literal'] = 'literal'
```

### `GenericTypeExpr`

```python
class GenericTypeExpr
```


A generic type expression like `list[User]`, `dict[str, User]`, `tuple[int, str]`.

```python
base: str
```

```python
args: list[TypeExpr]
```

```python
kind: Literal['generic'] = 'generic'
```

### `UnionTypeExpr`

```python
class UnionTypeExpr
```


A union type expression like `User | None`, `str | int`.

```python
members: list[TypeExpr]
```

```python
kind: Literal['union'] = 'union'
```



### `TypeFieldSignature`

```python
class TypeFieldSignature
```


A single field in a TypedDict-style type definition.

```python
name: str
```

```python
type: TypeExpr
```

```python
required: bool = False
```

```python
description: str | None = None
```

```python
kind: Literal['field'] = 'field'
```



### `TypeSignature`

```python
class TypeSignature
```


A TypedDict-style class definition with named fields.

```python
name: str
```

```python
description: str | None = None
```

```python
fields: dict[str, TypeFieldSignature] = field(default_factory=dict[str, TypeFieldSignature])
```

```python
kind: Literal['type'] = 'type'
```

#### `display_name`

```python
def display_name(self) -> str
```


The type name, with tool-name prefix applied if rendering context is set.



#### `render_definition`

```python
def render_definition(self, *, owner_name: str | None=None, conflicting_type_names: frozenset[str]=frozenset()) -> str
```


Render the full TypedDict class definition.

Args:
    owner_name: The owning tool name, used to build prefixed type names
        for conflicting types (e.g. `get_user_Address`).
    conflicting_type_names: Set of type names that need tool-name prefixes
        (from `get_conflicting_type_names`). Only effective when `owner_name`
        is also provided.



#### `structurally_equal`

```python
def structurally_equal(self, other: TypeSignature) -> bool
```


Compare two TypeSignatures structurally, ignoring descriptions.

### `FunctionParam`

```python
class FunctionParam
```


A single parameter in a function signature.

```python
name: str
```

```python
type: TypeExpr
```

```python
default: str | None = None
```

```python
description: str | None = None
```

```python
kind: Literal['param'] = 'param'
```



### `FunctionSignature`

```python
class FunctionSignature
```


Function signature shape with referenced type definitions.

This class holds the structural data (params, return type, referenced types)
needed to render a function signature. Name and description can be overridden
at render time (e.g. from a `ToolDefinition`).

```python
name: str
```

```python
description: str | None = None
```

```python
params: dict[str, FunctionParam] = field(default_factory=dict[str, FunctionParam])
```

```python
return_type: TypeExpr
```

```python
referenced_types: list[TypeSignature] = field(default_factory=list[TypeSignature])
```

```python
is_async: bool = False
```

```python
kind: Literal['function'] = 'function'
```

#### `render`

```python
def render(self, body: str, *, name: str | None=None, description: str | None=None, is_async: bool | None=None, conflicting_type_names: frozenset[str]=frozenset()) -> str
```


Render the signature with a specific body.

Sets `_type_name_overrides` so that dedup-prefixed types resolve
correctly during rendering.

Args:
    body: The function body (e.g. `'...'` or `'return await tool()'`).
    name: The function name (also used for dedup prefix resolution). Falls back to `self.name`.
    description: Optional docstring to include. Falls back to `self.description`.
    is_async: Override async rendering. If `None`, uses `self.is_async`.
    conflicting_type_names: Set of type names that need tool-name prefixes (from `get_conflicting_type_names`).

#### `from_schema`

```python
def from_schema(cls, *, name: str, parameters_schema: dict[str, Any], return_schema: dict[str, Any] | None=None) -> FunctionSignature
```


Build a FunctionSignature from JSON schemas.

`name` is stored on the resulting signature and also used for generating
fallback type names (e.g. `GetUserAddress`) when the schema has no `title`.

Parameter and return schemas are processed independently — each resolves
`$ref`s against its own `$defs`. Name collisions between parameter and return
types (e.g. both define a `User` `$def` with different structures) are handled
by `get_conflicting_type_names` at a later stage.

#### `get_conflicting_type_names`

```python
def get_conflicting_type_names(signatures: list[FunctionSignature]) -> frozenset[str]
```


Identify TypedDict name conflicts across multiple tool signatures.

Each signature keeps all its referenced types (so it remains self-contained),
but identical types (same name and structure) are unified to the same object
instance.

Returns the set of type names that have conflicts (same name, different
structure) and need tool-name prefixes at render time. Pass this set to
`FunctionSignature.render(conflicting_type_names=...)`.

Use `collect_unique_referenced_types()` when rendering to emit each
definition once.

#### `collect_unique_referenced_types`

```python
def collect_unique_referenced_types(signatures: list[FunctionSignature]) -> list[TypeSignature]
```


Collect unique TypeSignature objects from signatures, deduplicating by identity.

#### `render_type_definitions`

```python
def render_type_definitions(signatures: list[FunctionSignature], conflicting_type_names: frozenset[str]) -> list[str]
```


Render unique TypedDict definitions for a set of function signatures.

For types whose names conflict across signatures (as identified by
`get_conflicting_type_names`), each definition is rendered with a
tool-name prefix (e.g. `get_user_Address`).

Args:
    signatures: The function signatures (after `get_conflicting_type_names`).
    conflicting_type_names: The set returned by `get_conflicting_type_names`.

Returns:
    A list of rendered TypedDict class definitions as strings.



























