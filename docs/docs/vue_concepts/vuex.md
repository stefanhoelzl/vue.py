# Vuex
## Define
A Vuex store can be defined by writing a sub-class of `VueStore`
and used by setting the `store` parameter when initializing a app.
```python
from vue import VueComponent, VueStore

class Store(VueStore):
    pass

class App(VueComponent):
    pass

App("#app", store=Store())
```

enable the vuex extension in the `vuepy.yml` [config file](../management/configuration.md):
```yaml
scripts:
  vuex: true
```

## State Variables
```python
from vue import VueComponent, VueStore

class Store(VueStore):
    greeting = "Hello Store"

class App(VueComponent):
    def created(self):
        print(self.store.greeting)

App("#app", store=Store())
```


## Getter
```python
from vue import VueComponent, VueStore, getter

class Store(VueStore):
    greeting = "Hello"

    @getter
    def get_greeting(self):
        return self.greeting

    @getter
    def personalized_greeting(self, name):
        return "{} {}".format(self.greeting, name)

class App(VueComponent):
    def created(self):
        print(self.store.get_greeting) # "Hello"
        print(self.store.personalized_greeting("Store")) # "Hello Store"

App("#app", store=Store())
```

## Mutations
Unlike `Vue.js` mutations in `vue.py` can have multiple arguments and
even keyword-arguments
```python
from vue import VueComponent, VueStore, mutation

class Store(VueStore):
    greeting = ""

    @mutation
    def set_greeting(self, greeting, name=None):
        self.greeting = greeting
        if name:
            self.greeting += " " + name

class App(VueComponent):
    def created(self):
        self.store.commit("set_greeting", "Hello", name="Store")
        print(self.store.greeting) # "Hello Store"

App("#app", store=Store())
```

## Mutations
Similar to mutations actions in `vue.py` can have multiple arguments and
even keyword-arguments.
```python
from vue import VueComponent, VueStore, mutation

class Store(VueStore):
    @action
    def greet(self, greeting, name=None):
        if name:
            greeting += " " + name
        print(greeting)

class App(VueComponent):
    def created(self):
        self.store.dispatch("greet", "Hello", name="Store")

App("#app", store=Store())
```

## Plugins
```python
class Plugin(VueStorePlugin):
    def initialize(self, store):
        store.message = "Message"

    def subscribe(self, mut, *args, **kwargs):
        print(mut, args, kwargs)

class Store(VueStore):
    plugins = [Plugin().install] # list can also contain native vuex plugins

    message = ""

    @mutation
    def msg(self, prefix, postfix=""):
        pass

class ComponentUsingGetter(VueComponent):
    @computed
    def message(self):
        return self.store.message

    def created(self):
        self.store.commit("msg", "Hallo", postfix="!")

    template = "<div id='content'>{{ message }}</div>"
```
