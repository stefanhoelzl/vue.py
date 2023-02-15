from .base import pyjs_bridge, VueDecorator


class Custom(VueDecorator):
    def __init__(self, fn, key, name=None, static=False):
        self.__key__ = f"{key}.{name if name is not None else fn.__name__}"
        self.__value__ = pyjs_bridge(fn, inject_vue_instance=not static)


def custom(key, name=None, static=False):
    def wrapper(fn):
        return Custom(fn, key, name, static)

    return wrapper
