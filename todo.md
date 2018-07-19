## Features
* make $-methods available
  * e.g. `$emit`
* plugins
* local component registration
* global filter registration
* full directives
* ...

## Docs
* host on gh-pages
  *  live examples possible (jsfiddle?)
* documenting the limitations
  * wrapper around dict/list
    * `json.dumps` breaks
    * problem when passing Dict/List to js function (e.g. elastic header example)


## Tools
* cmd line tool to init vue.py project
* make available on pip

## Internals
* solve issue with `import asyncio`
  * needs very long to load page
* implicit load vue.js
  * also other js libs
  * use `load`

## Vue.py Universe
* python version of vuex
  * synchronize over WebSockets with python backend
* desktop toolkit
  * based on [pywebview](https://github.com/r0x0r/pywebview) ??
