# Vue Router
## Define
A vue router can be used by writing a sub-class of `VueRouter`, 
setting some `VueRoute`s 
and set the `router` parameter when initializing a app.
```python
from vue import VueComponent, VueRouter, VueRoute

class Foo(VueComponent):
    template = "<div>foo</div>'"

class Bar(VueComponent):
    template = "<div>bar</div>'"

class Router(VueRouter):
    routes = [
        VueRoute("/foo", Foo),
        VueRoute("/bar", Bar),
    ]

class App(VueComponent):
    template = """
        <div>
            <p>
                <router-link to="/foo">Go to Foo</router-link>
                <router-link to="/bar">Go to Bar</router-link>
            </p>
            <router-view></router-view>
        </div>
    """

App("#app", router=Router())
```

enable the vue-router extension in the `vuepy.yml` [config file](../management/configuration.md):
```yaml
scripts:
  vue-router: true
```
