# Custom Directives
Currently only [function directives](https://vuejs.org/v2/guide/custom-directive.html#Function-Shorthand) are supported
```python
from vue import VueComponent, directive

class CustomDirective(VueComponent):
    @staticmethod
    @directive
    def custom_focus(el, binding, vnode, old_vnode, *args):
        pass
```

The `@staticmethod` decorator is only necessary to avoid IDE checker errors.

Underscores in directive names get replaced by dashes, so `custom_focus` gets `v-custom-focus`.
