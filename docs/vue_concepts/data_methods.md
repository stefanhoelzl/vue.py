# Data
All class variables of a `vue.py` component are available as data fields in the Vue instance.
```python
class ComponentWithData(VueComponent):
    data_field = "value"
```

to initialize a data field with a prop you can use the `@data` decorator
```python
from vue import VueComponent, data

class ComponentWithData(VueComponent):
    prop: str
    @data
    def initialized_with_prop(self):
        return self.prop
```

# Methods
Similar to data fields all methods of the `vue.py` component are available as methods.
```python
from vue import VueComponent

class ComponentWithMethods(VueComponent):
    counter = 0

    def increase(self):
        self.counter += 1
```

Methods used as event handler, must have a (optional) argument for the event.
```python
from vue import VueComponent

class ComponentWithMethods(VueComponent):
    def handle(self, ev):
        print(ev)
```

## self
All attributes of the Vue instance are available as attributes of `self` (e.g. methods, computed properties, props etc.).

