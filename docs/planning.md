# Future Plans

## Features
* full access to Vue object (global configuration etc.)
* ...

## Bugs and Issues
* investigate directive arguments
  * different hooks get different arguments??
* solve issue with `import asyncio`
  * needs very long to load page
* try dynamics example again with latest bridge changes

### VueStore
* state acces in mutations must be via `state["key"]`
* unknown third argument at actions

## Docs
* embed examples in gallery

## Tools
* cmd line tool to init vue.py project
* pre-transpile to javascript
* make available on pip

## Internals
* write tests for decorators

## Vue.py Universe
* python bindings for vuex
  * synchronize with local/session storage
  * synchronize over WebSockets with python backend
* python bindings for vue-router
* desktop toolkit
  * based on [pywebview](https://github.com/r0x0r/pywebview) ??
