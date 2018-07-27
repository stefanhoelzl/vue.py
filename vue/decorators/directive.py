from .base import pyjs_bridge, VueDecorator


def map_hook(hook_name):
    if hook_name == "component_updated":
        return "componentUpdated"
    return hook_name


class DirectiveHook(VueDecorator):
    def __init__(self, fn, hooks=(), name=None):
        name = name if name else fn.__name__
        self.__key__ = "directives"
        self.__id__ = name.replace("_", "-")
        self.__value__ = pyjs_bridge(fn)

        if hooks:
            self.__value__ = {map_hook(hook): self.__value__
                              for hook in hooks}


def _directive_hook(name, hooks):
    def wrapper(fn):
        _hooks = (fn.__name__,) if not hooks else hooks
        return DirectiveHook(fn, hooks=_hooks, name=name)
    return wrapper


def directive(fn, *hooks):
    if callable(fn):
        return DirectiveHook(fn)
    return _directive_hook(fn, hooks)
