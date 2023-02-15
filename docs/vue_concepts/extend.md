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

## Template Slots
Vue.js does not support extending templates out-of-the-box and it is
[recommended](https://vuejsdevelopers.com/2017/06/11/vue-js-extending-components/)
to use third-party libraries like [pug](https://pugjs.org/api/getting-started.html).

With `vue.py` a feature called `template_slots` is included to extend templates.
A base component can define slots in the template
and a sub component can fill the slots with the attribute `template_slots`.
The base component can also define default values for the slots.

```python
from vue import VueComponent

class Base(VueComponent):
    template_slots = {
        "heading": "Default Heading",
        "footer": "Default Footer",
    }
    template = """
    <div>
        <h1>{heading}</h1>
        {content}
        <small>{footer}</small>
    </div>
    """

class Sub(Base):
    template_slots = {
        "heading": "My Custom Heading",
        "content": "content..."
    }
```
The `Sub` component gets rendered as
```html
<h1>My Custom Heading</h1>
content...
<small>Default Footer</small>
```

If you only have one slot in your component, the `template_slots` attribute
can be the template string

```python
from vue import VueComponent

class Base(VueComponent):
    template = "<h1>{}</h1>"

class Sub(Base):
    template_slots = "heading"
```
The `Sub` component gets rendered as
```html
<h1>heading</h1>
```

Mixing both is also possible
```python
class Base(VueComponent):
    template_slots = {"pre": "DEFAULT", "post": "DEFAULT"}
    template = "<p>{pre} {} {post}</p>"

class WithSlots(Base):
    template_slots = {"pre": "PRE", "default": "SUB"}

class WithDefault(Base):
    template_slots = "SUB"
```

The `WithSlots` component gets rendered as
```html
<p>PRE SUB DEFAULT</p>
```

The `WithDefault` component gets rendered as
```html
<p>DEFAULT SUB DEFAULT</p>
```
