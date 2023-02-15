# Custom Directives

## Local Registration
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


## Global Registration
Global directives can be created by sub-classing `VueDirective`.
```python
from vue import Vue, VueDirective
class MyDirective(VueDirective):
    def bind(el, binding, vnode, old_vnode):
        pass

    def component_updated(el, binding, vnode, old_vnode):
        pass

Vue.directive("my-directive", MyDirective)
```
and for function directives just pass the function to `Vue.directive`
```python
from vue import Vue
def my_directive(el, binding, vnode, old_vnode):
    pass

Vue.directive("my-directive", my_directive)
```
`vue.py` offeres a shorthand, if you like to take the **lower-cased** name
of the function/directive-class as directive name.
```python
from vue import Vue
def my_directive(el, binding, vnode, old_vnode):
    pass

Vue.directive(my_directive) # directive name is 'my_directive'
```

## Retrieve Global Directives
Getter for global directives works similar to Vue.js
```python
from vue import Vue
directive = Vue.directive('directive-name')
```
