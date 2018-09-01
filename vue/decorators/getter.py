from .base import pyjs_bridge, VueDecorator
from vue.bridge import VuexInstance


class Getter(VueDecorator):
    __key__ = "getters"

    def __init__(self, name, value):
        self.__id__ = name
        self.__value__ = value


def getter(fn):
    def wrapper(state, getters, *args):
        if fn.__code__.co_argcount == 1:
            return fn(VuexInstance(state=state, getters=getters))
        else:
            def getter_method(*args_, **kwargs):
                return fn(VuexInstance(state=state, getters=getters),
                          *args_,
                          **kwargs)
            return getter_method
    return Getter(fn.__name__, pyjs_bridge(wrapper))
