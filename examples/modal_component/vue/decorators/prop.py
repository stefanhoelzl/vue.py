from browser import window
from .base import pyjs_bridge, VueDecorator


class Prop(VueDecorator):
    type_map = {
        int: window.Number,
        float: window.Number,
        str: window.String,
        bool: window.Boolean,
        list: window.Array,
        object: window.Object,
        dict: window.Object,
        None: None,
    }

    def __init__(self, name, typ, mixin=None):
        mixin = mixin if mixin else {}
        self.__key__ = f"props.{name}"
        self.__value__ = {"type": self.type_map[typ], **mixin}


class Validator(VueDecorator):
    def __init__(self, prop, fn):
        self.__key__ = f"props.{prop}.validator"
        self.__value__ = pyjs_bridge(fn, inject_vue_instance=True)


def validator(prop):
    def decorator(fn):
        return Validator(prop, fn)

    return decorator
