from .base import pyjs_bridge, VueDecorator


class Action(VueDecorator):
    __key__ = "actions"

    def __init__(self, name, value):
        self.__id__ = name
        self.__value__ = value


def action(fn):
    def fn_(*args):
        return fn(args[0], args[1])
    return Action(fn.__name__, pyjs_bridge(fn_))
