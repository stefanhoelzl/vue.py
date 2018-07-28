# Filter

## Local Registration
Local registration of filters is done with the `@filters` decorator.
```python
from vue import VueComponent, filters

class ComponentWithFilter(VueComponent):
    message = "Message"

    @filters
    def lower_case(value):
        return value.lower()

    template = "<div id='content'>{{ message | lower_case }}</div>"
```

To avoid errors on source code checking errors in modern IDEs, an additional `@staticmethod` decorator can be added
```python
from vue import VueComponent, filters

class ComponentWithFilter(VueComponent):
    @staticmethod
    @filters
    def lower_case(value):
        return value.lower()
```

## Global Registration
Global registration of filters works similar to Vue.js
```python
from vue import Vue

Vue.filter("capitalize", str.capitalize)
```

Additionally in vue.py it is allowd to only pass a function to `Vue.filter`.
In this case the filter gets registered under the function name.
```python
from vue import Vue

def my_filter(val):
    return "filtered({})".format(val)

Vue.filter(my_filter)
```
