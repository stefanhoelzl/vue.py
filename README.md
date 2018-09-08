# vue.py
[![Build Status](https://travis-ci.org/stefanhoelzl/vue.py.svg?branch=master)](https://travis-ci.org/stefanhoelzl/vue.py)

use [Vue.js](https://www.vuejs.org) with pure Python

vue.py provides Python bindings for [Vue.js](https://www.vuejs.org).
It uses [brython](https://github.com/brython-dev/brython) to run Python in the browser.

Here is a simple example of an vue.py component
```python
from browser import alert
from vue import VueComponent

class HelloVuePy(VueComponent):
    greeting = "Hello vue.py"

    def greet(self, event):
        alert(self.greeting)

    template = """
    <button @click="greet">click me</button>
    """

HelloVuePy("#app")
```


## Development Status
The goal is to provide a solution to write fully-featured Vue applications in pure Python.

To get an overview what currently is supported, have a look at the [Documentation](https://stefanhoelzl.github.io/vue.py/docs/).

Have a look [here](https://stefanhoelzl.github.io/vue.py/planning.html) to see whats planned!

See also the [Limitations](https://stefanhoelzl.github.io/vue.py/docs/pyjs_bridge.html)

## Documentation
Documentation is available [here](https://stefanhoelzl.github.io/vue.py/docs/).

Examples can be found [here](https://stefanhoelzl.github.io/vue.py/examples).
These are vue.py versions of the [Vue.js examples](https://vuejs.org/v2/examples/)


## Installation
```bash
$ pip install https://stefanhoelzl.github.io/vue.py/vuepy.whl
```

## Development
Get the code
```bash
$ git clone https://github.com/stefanhoelzl/vue.py.git
$ cd vue.py
```

Install required python packages, the chromedriver for selenium and brython
```bash
$ make env.up
```

Start server (needed for tests)
```bash
$ make serve
```

Run tests
```bash
$ make tests          # runs all tets
$ make tests.unit     # runs unit tests
$ make test.selenium  # runs selenium tests
```

Clean up your working directory.
```bash
$ make env.clean
```

Reset your development environment
_(clean up, reinstall packages and redownload needed files)_
```bash
$ make env.down
```

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/stefanhoelzl/fancy-dict/blob/master/LICENSE) file for details
