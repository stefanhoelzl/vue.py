from .base import pyjs_bridge, VueDecorator


class Getter(VueDecorator):
    __key__ = "getters"

    def __init__(self, name, value):
        self.__id__ = name
        self.__value__ = value


def getter(fn):
    def fn_(*args, **kwargs):
        return fn(args[0], args[1])
    return Getter(fn.__name__, pyjs_bridge(fn_))
