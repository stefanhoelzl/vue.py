# Extend
Vue.js uses `Vue.extend` or the `extends` Component attribute to extend
components. Per default `vue.py` sticks to the Pythonic way and uses the
python class inheritance behavior.
```python
from vue import VueComponent

class Base(VueComponent):
    def created(self):
        print("Base")

class Sub(Base):
    def created(self):
        super().created()
        print("Sub")
```
which outputs on the console
```
Base
Sub
```

To use the merging strategies Vue.js applies when using `extends`
in `vue.py` just set the `extends` attribute to `True`

```python
from vue import VueComponent

class Base(VueComponent):
    def created(self):
        print("Base")

class Sub(Base):
    extends = True

    def created(self):
        print("Sub")
```
which outputs on the console
```
Base
Sub
```

The `extend` attribute can also be a native Vue.js component to extend from this.
```
from vue import *
from vue.utils import js_lib
NativeVueJsComponent = js_lib("NativeVueJsComponent")

class Sub(VueComponent):
    extends = NativeVueJsComponent
```

## Template Merging
Vue.js does not support extending templates out-of-the-box and it is
[recommended](https://vuejsdevelopers.com/2017/06/11/vue-js-extending-components/)
to use third-party libraries like [pug](https://pugjs.org/api/getting-started.html).

With `vue.py` a feature called `template merging` is included,
which can be activated with the `template_merging` attribute.

```python
from vue import VueComponent

class Base(VueComponent):
    template_merging = True
    template = "<h1>{}</h1>"

class Sub(Base):
    template = "heading"
```
The `Sub` component gets rendered as
```html
<h1>heading</h1>
```

### Template Slots
If you want to insert templates from the sub component in different places in your
base components template, there is a attribute called `template_slots`.

```python
from vue import VueComponent

class Base(VueComponent):
    template_merging = True
    template_slots = {
        "heading": "Default Heading",
        "footer": "Default Footer",
    }
    template = """
    <div>
        <h1>{heading}</h1>
        {}
        <small>{footer}</small>
    </div>
    """

class Sub(Base):
    template_slots = {
        "heading": "My Custom Heading"
    }
    template = "content..."
```
The `Sub` component gets rendered as
```html
<h1>My Custom Heading</h1>
content...
<small>Default Footer</small>
```

The sub components `template` value is inserted in the default slot `{}`.
All other slots are filled with the sub components values of `templates_slots`.
If a sub component does not provide a slot, the base components default value is used.

