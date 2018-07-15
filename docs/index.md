# Documentation
`vue.py` provides bindings for [Vue.js](https://vuejs.org/).
If you are not familiar with [Vue.js](https://vuejs.org/) read the [Vue.js Guide](https://vuejs.org/v2/guide/)
and then get back here to learn how to use [Vue.js](https://vuejs.org/) with pure Python.

## Getting Started

First clone the repository
```bash
$ git clone https://github.com/stefanhoelzl/vue.py.git
$ cd vue.py
```

set up the environment
```bash
$ make env.up
```

and start a http server
```bash
$ make serve
```

Now you are ready to build your first `vue.py` application.

## First Application
Create a folder for your app
```bash
mkdir app
cd app
```

add a `app.html` file where your app lives
```html
<html>
<head>
  <link rel="pythonpath" href="/" hreflang="py" />
  <script src="http://localhost:8000/js/vue.js"></script>
  <script src="http://localhost:8000/js/brython_dist.js"></script>
</head>
<body onload="brython(1)">
  <div id="app"></div>
  <script type="text/python" src="http://localhost:8000/app/app.py"></script>
</body>
</html>
```

and as last step create a `app.py` where you create your Vue Component
```python
from vue import *

class App(VueComponent):
    template = "<div>Hello vue.py</div>"
App("#app")
```
Now goto [http://localhost:8000/app/app.html](http://localhost:8000/app/app.html) and see your first vue.py app.

## How to use Vue.js concepts
* [Instance and Components](instance_components.md)
* [Data and Methods](data_methods.md)
* [Computed Properties and Watchers](computed_properties.md)
* [Props](props.md)
* [Lifecycle Hooks](lifecycle_hooks.md)
* [Customize V-Model](custom_vmodel.md)
