# vue.py
use [Vue.js](https://www.vuejs.org) with pure python

vue.py provides Python bindings for [Vue.js](https://www.vuejs.org).
It uses [brython](https://github.com/brython-dev/brython) to run Python in the browser.


## Installation
```bash
$ git clone https://github.com/stefanhoelzl/vue.py.git
$ cd vue.py
```
_Tested under macOS (should work under Linux)_

## Demo
```bash
$ make env.serve
```
Goto [http://localhost:8000/demo/demo.html] and enjoy vue.py!

## Demo Code
Python
```python
from vue import VueComponent, Data, method, Property


class TodoItem(VueComponent):
    todo = Property()

    template = """
    <li>
        <input type="checkbox" v-model="todo.done"></input>
        <s v-if="todo.done">{{ todo.text }}</s>
        <span v-else>{{ todo.text }}</span>
    </li>
    """
TodoItem.register()


class DemoApp(VueComponent):
    new_todo = Data("")
    todos = Data([{"id": 1, "text": "Like Vue.js", "done": True},
                  {"id": 0, "text": "Try out vue.py", "done": False}])
    next_id = Data(1)

    @method
    def add(self, event):
        self.todos.push({"id": self.next_id, "text":  self.new_todo})
        self.new_todo = ""
        self.next_id += 1

    template = """
    <div>
        <input type="text" placeholder="new todo" v-model="new_todo"></input>
        <button @click="add">add</button>
        <ol>
            <todo-item v-for="todo in todos" :todo="todo" :key="todo.id">
            </todo-item>
        </ol>
    </div>
    """


DemoApp("#app")

```
HTML
```html
<html>
<head>
  <link rel="pythonpath" href="/" hreflang="py" />
  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  <script src="http://localhost:8000/demo/brython.js"></script>
</head>
<body onload="brython(1)">
  <div id="app"></div>
  <script type="text/python" src="http://localhost:8000/demo/demo.py"></script>
</body>
</html>

```
## Development
```bash
$ make env.install
```
Installs required python packages, the chromedriver for selenium and brython

```bash
$ make env.clean
```
Cleans up your working directory (also uninstalls python packages).

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/stefanhoelzl/fancy-dict/blob/master/LICENSE) file for details
