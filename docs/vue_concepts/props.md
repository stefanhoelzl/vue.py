# Props
A prop is defined by adding a type hint to a class variable.
```python
from vue import VueComponent

class ComponentWithData(VueComponent):
    prop: str
```

## Types
Unlike Vue.js, vue.py enforces prop types (if not type hint is provided, it is a data field).

The following types are currently supported:
* `int`
* `float`
* `str`
* `bool`
* `list`
* `dict`

## Default
By assigning a value to a prop, the default value can be defined.
```python
from vue import VueComponent

class ComponentWithData(VueComponent):
    prop: str = "default"
```

## Required
If no default value is given, the prop is automatically required.

## Validator
With the `@validator` decorator are prop validators defined
```python
from vue import VueComponent, validator

class ComponentWithData(VueComponent):
    prop: int

    @validator("prop")
    def prop_must_be_greater_than_100(self, value):
        return value > 100
```
