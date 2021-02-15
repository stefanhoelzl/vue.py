# vue.py
[![Build Status](https://github.com/stefanhoelzl/vue.py/workflows/CI/badge.svg)](https://github.com/stefanhoelzl/vue.py/actions)
[![PyPI](https://img.shields.io/pypi/v/vuepy.svg)](https://pypi.org/project/vuepy/)
[![License](https://img.shields.io/pypi/l/vuepy.svg)](LICENSE)

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

## Installation
```bash
$ pip install vuepy
```


## Development Status
The goal is to provide a solution to write fully-featured Vue applications in pure Python.

To get an overview what currently is supported, have a look at the [Documentation](https://stefanhoelzl.github.io/vue.py/docs/).

Have a look [here](https://stefanhoelzl.github.io/vue.py/planning.html) to see whats planned!

See also the [Limitations](https://stefanhoelzl.github.io/vue.py/docs/pyjs_bridge.html)

## Documentation
Documentation for the last release is available [here](https://stefanhoelzl.github.io/vue.py/docs/).

Documentation fo the current master branch can be found [here](https://github.com/stefanhoelzl/vue.py/blob/master/docs/docs/index.md).

Examples can be found [here](https://stefanhoelzl.github.io/vue.py/examples).
These are vue.py versions of the [Vue.js examples](https://vuejs.org/v2/examples/)

## Performance
Initial loading times of `vue.py` apps can be very long.
Especially when loading a lot of python files.
Still figuring out how to solve this.

Have not done any peformance tests, but havent noticed any issues with performance
as soon as the app was fully loaded.

## Development
### Getting Started
Open in [gitpod.io](https://gitpod.io#github.com/stefanhoelzl/vue.py)

Get the code
```bash
$ git clone https://github.com/stefanhoelzl/vue.py.git
$ cd vue.py
```

Optionally you can create a [venv](https://docs.python.org/3.8/library/venv.html)
```bash
$ python -m venv venv
$ source venv/bin/activate
```

Install required python packages, the chromedriver for selenium and brython
```bash
$ make env.up
```

Format the code
```bash
$ make format
```

Run tests
```bash
$ make tests           # runs all tets
$ make tests.unit      # runs unit tests
$ make tests.selenium  # runs selenium tests
$ make tests.cli       # runs cli tests
$ make tests TEST=cli/test_provider.py::TestRenderIndex::test_defaults # run explicit test
```

Run an example
```bash
$ make run APP=examples/tree_view  # makes example available on port 5000
```

Clean up your working directory.
```bash
$ make env.clean
```

Reset your development environment
_(clean up, reinstall packages and redownload needed files)_
```bash
$ make env.down
$ make env.up
```

Publish a new release
```bash
$ make release            # bumps minor version number
$ make release MODE=major # bumps major version number
$ make release MODE=patch # bumps patch number
```

### Contributing
see [CONTRIBUTING](CONTRIBUTING)

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/stefanhoelzl/vue.py/blob/master/LICENSE) file for details
