# Custom Directives
Currently only locally registered directives are supported.

For [function directives](https://vuejs.org/v2/guide/custom-directive.html#Function-Shorthand)
is just a decorator necessary
```python
from vue import VueComponent, directive

class CustomDirective(VueComponent):
    @staticmethod
    @directive
    def custom_focus(el, binding, vnode, old_vnode, *args):
        pass
```

To define custom hook functions, add the directive name as argument to
the decorator
```python
from vue import VueComponent, directive

class CustomDirective(VueComponent):
    @staticmethod
    @directive("focus")
    def component_updated(el, binding, vnode, old_vnode, *args):
        # implement 'componentUpdated' hook function here
        pass

    @staticmethod
    @directive("focus")
    def inserted(el, binding, vnode, old_vnode, *args):
        # implement 'inserted' hook function here
        pass
```

To avoid code duplication when adding the same hook function to different hooks,
the hooks can be specified as decorator arguments.
```python
from vue import VueComponent, directive

class CustomDirective(VueComponent):
    @staticmethod
    @directive("focus", "component_updated", "inserted")
    def combined_hook(el, binding, vnode, old_vnode, *args):
        # implement function for 'componentUpdated' and 'inserted' hook here
        pass
```

**The Vue.js hook `componentUpdated` is called `component_updated` to be more pythonic**

The `@staticmethod` decorator is only necessary to avoid IDE checker errors.

Underscores in directive names get replaced by dashes, so `custom_focus` gets `v-custom-focus`.
