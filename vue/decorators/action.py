from .base import pyjs_bridge, VueDecorator
from vue.bridge import VuexInstance


class Action(VueDecorator):
    __key__ = "actions"

    def __init__(self, name, value):
        self.__id__ = name
        self.__value__ = value


def action(fn):
    def wrapper(context, *payload):
        payload = payload[0] if payload else {"args": (), "kwargs": {}}
        return fn(VuexInstance(state=context.state,
                               getters=context.getters,
                               root_state=context.rootState,
                               root_getters=context.rootGetters,
                               commit=context.commit,
                               dispatch=context.dispatch),
                  *payload.get("args", ()),
                  **payload.get("kwargs", {}))
    return Action(fn.__name__, pyjs_bridge(wrapper))
