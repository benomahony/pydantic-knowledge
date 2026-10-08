# `pydantic_ai.format_prompt`

### `format_as_xml`

```python
def format_as_xml(obj: Any, root_tag: str | None=None, item_tag: str='item', none_str: str='null', indent: str | None='  ', include_field_info: Literal['once'] | bool=False) -> str
```


Format a Python object as XML.

This is useful since LLMs often find it easier to read semi-structured data (e.g. examples) as XML,
rather than JSON etc.

Supports: `str`, `bytes`, `bytearray`, `bool`, `int`, `float`, `Decimal`, `date`, `datetime`, `time`, `timedelta`,
`UUID`, `Enum`, `Mapping`, `Iterable`, `dataclass`, and `BaseModel`.

Args:
    obj: Python Object to serialize to XML.
    root_tag: Outer tag to wrap the XML in, use `None` to omit the outer tag.
    item_tag: Tag to use for each item in an iterable (e.g. list), this is overridden by the class name
        for dataclasses and Pydantic models.
    none_str: String to use for `None` values.
    indent: Indentation string to use for pretty printing.
    include_field_info: Whether to include attributes like Pydantic `Field` attributes and dataclasses `field()`
        `metadata` as XML attributes. In both cases the allowed `Field` attributes and `field()` metadata keys are
        `title` and `description`. If a field is repeated in the data (e.g. in a list) by setting `once`
        the attributes are included only in the first occurrence of an XML element relative to the same field.

Returns:
    XML representation of the object.

Example:
```python {title="format_as_xml_example.py" lint="skip"}
from pydantic_ai import format_as_xml

print(format_as_xml({'name': 'John', 'height': 6, 'weight': 200}, root_tag='user'))
'''
<user>
  <name>John</name>
  <height>6</height>
  <weight>200</weight>
</user>
'''
```