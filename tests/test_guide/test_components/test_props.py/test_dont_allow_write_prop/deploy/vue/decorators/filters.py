from .base import pyjs_bridge, VueDecorator


class Filter(VueDecorator):
    __key__ = "filters"

    def __init__(self, fn, name):
        self.__value__ = pyjs_bridge(fn)
        self.__id__ = name


def filters(fn):
    return Filter(fn, fn.__name__)
