# Documentation
`vue.py` provides bindings for [Vue.js](https://vuejs.org/).
If you are not familiar with [Vue.js](https://vuejs.org/) read the [Vue.js Guide](https://vuejs.org/v2/guide/)
and then get back here to learn how to use [Vue.js](https://vuejs.org/) with pure Python.

## Installation

Install `vue.py` via `pip`
```bash
$ pip install https://stefanhoelzl.github.io/vue.py/vuepy.tar.gz
```

## First Application
Create a folder for your app
```bash
$ mkdir app
$ cd app
```

and as last step create a `app.py` where you create your Vue Component
```python
from vue import *

class App(VueComponent):
    template = "<div>Hello vue.py</div>"
App("#app")
```

deploy your app
```bash
$ vue-cli deploy live
```
Now goto [http://localhost:5000](http://localhost:5000) and see your first vue.py app.

## How to use Vue.js concepts
* [Instance and Components](vue_concepts/instance_components.md)
* [Data and Methods](vue_concepts/data_methods.md)
* [Computed Properties and Watchers](vue_concepts/computed_properties.md)
* [Props](vue_concepts/props.md)
* [Lifecycle Hooks](vue_concepts/lifecycle_hooks.md)
* [Customize V-Model](vue_concepts/custom_vmodel.md)
* [Filter](vue_concepts/filter.md)
* [Custom Directives](vue_concepts/custom_directives.md)
* [Plugins and Mixins](vue_concepts/plugins_mixins.md)
* [Extend](vue_concepts/extend.md)
* [Vuex](vue_concepts/vuex.md)

## Management
* [Configuration](management/configuration.md)
* [vue-cli](management/cli.md)

## Python/Javascript Bridge
[here](pyjs_bridge.md)
