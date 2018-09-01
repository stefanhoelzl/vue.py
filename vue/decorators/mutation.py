from vue.bridge import VuexInstance
from .base import pyjs_bridge, VueDecorator


class Mutation(VueDecorator):
    __key__ = "mutations"

    def __init__(self, name, value):
        self.__id__ = name
        self.__value__ = value


def mutation(fn):
    def wrapper(state, payload):
        return fn(VuexInstance(state=state),
                  *payload.get("args", ()),
                  **payload.get("kwargs", {}))
    return Mutation(fn.__name__, pyjs_bridge(wrapper))
