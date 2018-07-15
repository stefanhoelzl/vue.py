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
Currently only global registration is available.
```python
MyComponent.register()
```
the `register()` methods accepts a argument to change the name under which the component is available later.

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
Keyword-arguments can be used to pass [propsData](https://vuejs.org/v2/api/#propsData) to the instance
```python
App("#app", prop="value")
```
