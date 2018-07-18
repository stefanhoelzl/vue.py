# Computed Properties
Computed properties can be defined with the `@computed` decorator
```python
from vue import VueComponent, computed

class ComponentWithMethods(VueComponent):
    message = "Hallo vue.py"
    @computed
    def reversed(self):
        return "".join(reversed(self.message))
```

computed setters are defined similar to plain python setters
```python
class ComputedSetter(VueComponent):
    message = "Hallo vue.py"

    @computed
    def reversed_message(self):
        return self.message[::-1]

    @reversed_message.setter
    def reversed_message(self, reversed_message):
        self.message = reversed_message[::-1]
```

# Watchers
Watchers can be defined with the `@watch` decorator.
```python
from vue import VueComponent, watch

class Watch(VueComponent):
    message = ""

    @watch("message")
    def log_message_changes(self, new, old):
        print("'message' changed from '{}' to '{}'".format(old, new)
```


`deep` and `immediate` watchers can be configured via arguments

```python
from vue import VueComponent, watch

class Watch(VueComponent):
    message = ""

    @watch("message", deep=True, immediate=True)
    def log_message_changes(self, new, old):
        print("'message' changed from '{}' to '{}'".format(old, new)
```
