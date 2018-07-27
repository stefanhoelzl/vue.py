from .base import pyjs_bridge, VueDecorator


class Watcher(VueDecorator):
    __key__ = "watch"

    def __init__(self, name, fn, deep=False, immediate=False):
        self.__id__ = name
        self._fn = pyjs_bridge(fn, inject_vue_instance=True)
        self._deep = deep
        self._immediate = immediate

    @property
    def __value__(self):
        return {
            "handler": self._fn,
            "deep": self._deep,
            "immediate": self._immediate
        }


def watch(name, deep=False, immediate=False):
    def decorator(fn):
        return Watcher(name, fn, deep, immediate)
    return decorator
