from .base import pyjs_bridge, VueDecorator


class Getter(VueDecorator):
    __key__ = "getters"

    def __init__(self, name, value):
        self.__id__ = name
        self.__value__ = value


def getter(fn):
    def fn_(*args):
        return fn(args[0], args[1])
    return Getter(fn.__name__, pyjs_bridge(fn_))


def getter_method(fn):
    def fn_(arg0, arg1, *args):
        def fn__(*args):
            return fn(arg0, arg1, *args)
        return fn__
    return Getter(fn.__name__, pyjs_bridge(fn_))
