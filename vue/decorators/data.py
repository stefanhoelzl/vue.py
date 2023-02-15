from .base import pyjs_bridge, VueDecorator


class Data(VueDecorator):
    def __init__(self, name, value):
        self.__key__ = f"data.{name}"
        self.__value__ = value


def data(fn):
    return Data(fn.__name__, pyjs_bridge(fn))
