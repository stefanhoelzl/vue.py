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

## Javascript Libraries
If you want to use custom javascript libraries, add this section to the configuration file:
```yaml
scripts:
  - <path of the script relative to your application folder>
  - <URL of the script>
```

## Extensions
`vue.py` comes with some vue.js extensions builtin:
* [vuex](https://vuex.vuejs.org)
The extensions can be activated as followed:
```yaml
extensions:
  - vuex
  - vue-router
```
By default all extensions are deactivated to avoid loading unnecessary files.

## EntryPoint
By default the `app.py` in your project directory is the entry point for your app.
If you want to point to a custom entry point, add this section:
```yaml
entry_point: custom.py
```
