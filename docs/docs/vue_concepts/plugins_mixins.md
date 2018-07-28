# Mixins

## Write Mixins
Mixins are created by sub-classing from `VueMixin` and from there it is
similar to write a `VueComponent`
```python
from vue import VueMixin, computed

class MyMixin(VueMixin):
    prop: str

    value = "default"

    def created(self):
        pass

    @computed
    def upper_value(self):
        return self.value.upper()
```

## Use Mixins
### Local Registration
Local registration of a Mixin within a Component works just like in Vue.js.
```python
from vue import VueComponent

class MyComponent(VueComponent):
    mixins: [MyPyMixin, AnotherVueJsMixin]
```
Mixins wirtten in Vue.js and `vue.py` can be mixed.

### Global Registration
Global registration of a Mixin works also just like in Vue.js.
```python
from vue import Vue
Vue.mixin(MyMixin)
```

# Plugins
## Write Plugins
A plugin can be written by sub-classing `VuePlugin` and implementing
the function `install` similar to Vue.js.
```python
from vue import Vue, VuePlugin, VueMixin

class MyPlugin(VuePlugin):
    class MyMixin(VueMixin):
        def created(self):
            pass

        # 4) Within a Mixin, new instance methods can be defined
        def my_method(self, args):
            pass

    @staticmethod
    def global_method():
        pass

    @staticmethod
    def install(*args, **kwargs):
        # 1) Add a global method or property
        Vue.my_global_method = MyPlugin.global_method

        # 2) Add a global assed
        Vue.directive(MyDirective)

        # 3) Inject Mixins
        Vue.mixin(MyPlugin.MyMixin)
```

## Use Plugins
Using plugins works like in Vue.js
```python
from vue import Vue

Vue.use(MyPlugin)
```
`vue.py` supports also using native Vue.js plugins.
