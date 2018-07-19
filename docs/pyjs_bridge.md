# Python/Javascript Bridge
## Call Javascript Functions
`vue.py` provides some utilities to access Javascript libraris.

You can load Javascript libraries dynamically
```python
from vue.utils import js_load
marked = js_load("https://unpkg.com/marked@0.3.6")
html = marked("# Title")
```
This perfoms an synchrous ajax call and therefore is not recommended for responsive applications.
Furthermore prevent some browser (e.g. Chrome) load from external ressources with ajax.

Therefore a second method is provided to acces a already loaded Javascript library.
```html
<script src="https://unpkg.com/marked@0.3.6"></script>
```
```python
from vue.utils import js_lib
marked = js_lib("marked")
html = marked("# Title")
```
This uses the optimized methods a Browser uses to load all dependencies.
And provides also access to all object in the Javascript namespace.

## Limitations
Due to restrictions of Brython in combination with the reactivity system in Vue.js are custom wrapper around component data and props neccessary.
This is done mostly in the background, there are some limitations to consider.

### When Native Python Types Assumed
The wrapper around lists and dictionaries provide the same interface than native python types but due to restrictions in Brython, they are no subclasses of `list`/`dict`.
This can lead to problems when passing this methods to other native python methods.
Therefore a helper is provided to convert a wrapped Javascript object into a native python type.
```python
import json
from vue import VueComponent, computed
from vue.wrapper import Object


class MyComponent(VueComponent):
    template = "<div>{{ content_as_json }}</div>"
    content = [{"a": 1}]

    @computed
    def content_as_json(self):
        # Will break because self.content is not a native python type
        # json.dumps does not know how to serialize this types
        return json.dumps(sef.content)

        # vue.py provides a method to convert the wrapper types
        return json.dumps(Object.to_py(self.content))

```
**When converting to native python types reactivity may get lost!**


### When Native Javascript Types Assumed
A similar problem exists when passing wrapper variables to native javascript methods.
Brython can convert native Python types like lists and dicts to their javascript equivalent.
Since the wrapper types are not real lists/dicts Brython cannot convert them.
```python
from vue import VueComponent, computed
from vue.wrapper import Object
from vue.utils import js_lib

js_json = js_lib("JSON")

class MyComponent(VueComponent):
    template = "<div>{{ content_as_json }}</div>"
    content = [{"a": 1}]

    @computed
    def content_as_json(self):
        # Will break because self.content is not a native javascript type
        # JSON.stringify does not know how to serialize this types
        return js_json.stringify(self.content)

        # vue.py provides a method to convert the wrapper types
        return js_json.stringify(Object.to_js(self.content))
```

### Are These Limitations Forever?
I hope not!

Currently the main reason for this limitations is [Brython Issue 893](https://github.com/brython-dev/brython/issues/893).
When this one gets fixed, the wrapper classes can be subclasses of native python types and Brython should be able to do the right conversions under the hood.
