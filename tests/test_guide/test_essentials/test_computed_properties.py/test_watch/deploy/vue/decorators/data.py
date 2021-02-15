from .base import pyjs_bridge, VueDecorator


class Data(VueDecorator):
    __key__ = "data"

    def __init__(self, name, value):
        self.__id__ = name
        self.__value__ = value


def data(fn):
    return Data(fn.__name__, pyjs_bridge(fn))
