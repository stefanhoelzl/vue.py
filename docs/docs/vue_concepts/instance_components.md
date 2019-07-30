# Components
## Define
A Vue component can be defined by writing a sub-class of `VueComponent`
```python
from vue import VueComponent

class MyComponent(VueComponent):
    pass
```

## Registration
Every component has to be [registered](https://vuejs.org/v2/guide/components-registration.html) to be available in other components.
### Local Registration
```python
from vue import VueComponent

class MyComponent(VueComponent):
    components = [
        MyVuePyComponent,
        AnotherNativeVueJsComponent,
    ]
```
The component to register can be either a `vue.py` component or a native
Vue.js component loaded with `js_lib` or `js_import`
### Global Registration
```python
from vue import Vue

# For vue.py components or native Vue.js component loaded with js_lib or js_import
Vue.component(MyComponent)
Vue.component("my-custom-name", MyComponent)

# Only for vue.py components
MyComponent.register()
MyComponent.register("my-custom-name")
```

## Template
The component html template can be defined with a class variable called `template`
```python
from vue import VueComponent

class MyComponent(VueComponent):
    template = """
    <div>
        Hallo vue.py!
    </div>
    """
```

`vue.py` templates look the same than Vue.js templates. This means inline expressions must be javascript!!.
```python
from vue import VueComponent

class MyComponent(VueComponent):
    message = "Hallo vue.py!"
    template = """
    <div>
        {{ message.split('').reverse().join('') }}
    </div>
    """
```


# Instance
## Start
To start a component as Vue application, just pass a css selector at initialization
```
App("#app")
```

## Prop Data
[propsData](https://vuejs.org/v2/api/#propsData) can be passed in as a dictionary.
```python
App("#app", props_data={"prop": "value"})
```


## API
### Dollar Methods
$-methods like `$emit` can be called by omitting the `$`
```python
from vue import VueComponent

class MyComponent(VueComponent):
    def created(self):
        self.emit("creation", "Arg")
```

In the case your Component has another attribute with the same name, you can use a workaround and directly call `getattr()`
```python
from vue import VueComponent

class MyComponent(VueComponent):
    emit = "already used"
    def created(self):
        getattr(self, "$emit")("creation", "Arg")
```

