from .base import pyjs_bridge, VueDecorator


class Filter(VueDecorator):
    def __init__(self, fn, name):
        self.name = name
        self.__key__ = f"filters.{name}"
        self.__value__ = pyjs_bridge(fn)


def filters(fn):
    return Filter(fn, fn.__name__)
