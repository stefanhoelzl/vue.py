# Configuration

Your `vue.py` application can be customized via a `vuepy.yml` file
located in your application folder.

## Stylesheets
If you want to use custom CSS stylsheets, add this section to the configuration file:
```yaml
stylesheets:
  - <path of the stylesheet relative to your application folder>
  - <URL of the stylesheet>
```

## Scripts
### Javascript Libraries
If you want to use custom javascript libraries, add this section to the configuration file:
```yaml
scripts:
  - <path of the script relative to your application folder>
  - <URL of the script>
```
or if combined with [extensions](#Extensions) or [custom versions](#Custom-Versions)
```yaml
scripts:
  "local_lib_name": <path of the script relative to your application folder>
  "lib_name": <URL of the script>
```

### Extensions
`vue.py` comes with some vue.js extensions builtin:
* [vuex](https://vuex.vuejs.org)
* [vue-router](https://router.vuejs.org)
The extensions can be activated as followed:
```yaml
scripts:
  vuex: true
  vue-router: true
```
By default all extensions are deactivated to avoid loading unnecessary files.


### Custom Versions
`vue.py` comes with vue.js and brython built-in.
If different versions can be used as followed:
```yaml
scripts:
  vue: <URL/Path to custom vue.js file>
  brython: <URL/Path to custom brython_dist.js file>
  vuex: <URL/Path to custom vuex.js file>
  vue-router: <URL/Path to custom vue-router.js file>
```

## EntryPoint
By default the `app.py` in your project directory is the entry point for your app.
If you want to point to a custom entry point `custom.py`, add this section:
```yaml
entry_point: custom
```

## Templates
Since writing HTML in python strings can be tedious 
you can write your templates in .html files 
and link them as your template string.
```yaml
templates:
    myhtml: my.html
```

```python
from vue import VueComponent

class MyComponent(VueComponent):
    template = "#myhtml"
```
