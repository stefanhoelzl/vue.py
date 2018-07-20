from .base import pyjs_bridge, VueDecorator


class Directive(VueDecorator):
    __key__ = "directives"

    def __init__(self, fn, hooks=(), name=None):
        name = name if name else fn.__name__
        self.__name__ = name.replace("_", "-")
        self.__value__ = pyjs_bridge(fn)
        self._hooks = hooks

    def update(self, vue_dict):
        if not self._hooks:
            super().update(vue_dict)
        for hook in self._hooks:
            if hook == "component_updated":
                hook = "componentUpdated"
            base = vue_dict.setdefault(self.__key__, {})\
                .setdefault(self.__name__, {})
            base.update({hook: self.__value__})


def _directive_hook(name, hooks):
    def wrapper(fn):
        _hooks = (fn.__name__,) if not hooks else hooks
        return Directive(fn, hooks=_hooks, name=name)
    return wrapper


def directive(fn, *hooks):
    if callable(fn):
        return Directive(fn)
    return _directive_hook(fn, hooks)
