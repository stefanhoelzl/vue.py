# Render Function
A render function can be defined by overwriting the `render`  method.
```python
from vue import VueComponent

class ComponentWithData(VueComponent):
    def render(self, create_element):
        return create_element("h1", "Title")
```

## Accessing Slots
Slots can be accessed as a dictionary.
```python
from vue import VueComponent

class ComponentWithSlots(VueComponent):
    def render(self, create_element):
        return create_element(f"div", self.slots.get("default"))
```
It is recommened to access the dictionary via the `get`-method to avoid failures
when no children for the slot are provided.

## Passing Props
```python
from vue import VueComponent

class ComponentWithProps(VueComponent):
    prop: str = "p"
    template = "<div :id='prop'></div>"

ComponentWithProps.register()

class Component(VueComponent):
    def render(self, create_element):
        return create_element(
            "ComponentWithProps", {"props": {"prop": "p"}},
        )
```
