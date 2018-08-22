from .base import pyjs_bridge, VueDecorator


class Mutation(VueDecorator):
    __key__ = "mutations"

    def __init__(self, name, value):
        self.__id__ = name
        self.__value__ = value


def mutation(fn):
    return Mutation(fn.__name__, pyjs_bridge(fn))
