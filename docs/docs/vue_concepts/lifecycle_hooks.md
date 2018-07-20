# Lifecycle Hooks
Certain names for component methods are reserved, to specify lifecycle hooks.
```python
from vue import VueComponent

class ComponentLifecycleHooks(VueComponent):
    def before_create(self):
        print("on beforeCreate")

    def created(self):
        print("on created")

    def before_mount(self):
        print("on beforeMount")

    def mounted(self):
        print("on mounted")

    def before_update(self):
        print("on beforeUpdate")

    def updated(self):
        print("on updated")

    def before_destroy(self):
        print("on beforeDestroy")

    def destroyed(self):
        print("on destroyed")
```
