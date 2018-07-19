# Customize V-Model
To customize the event and prop used by `v-model` a class variable of the type `Model()` can be defined.
```python
from vue import VueComponent, Model

class CustomVModel(VueComponent):
    model = Model(prop="checked", event="change")
    checked: bool
    template = """
    <div>
        <p id="component">{{ checked }}</p>
        <input
            id="c"
            type="checkbox"
            :checked="checked"
            @change="$emit('change', $event.target.checked)"
        >
    </div>
    """
```
