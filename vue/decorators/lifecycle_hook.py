from .base import pyjs_bridge, VueDecorator


class LifecycleHook(VueDecorator):
    mapping = {"before_create": "beforeCreate",
               "created": "created",
               "before_mount": "beforeMount",
               "mounted": "mounted",
               "before_update": "beforeUpdate",
               "updated": "updated",
               "before_destroy": "beforeDestroy",
               "destroyed": "destroyed"}

    def __init__(self, name, fn):
        self.__key__ = self.mapping[name]
        self.__value__ = pyjs_bridge(fn, inject_vue_instance=True)


def lifecycle_hook(name):
    def wrapper(fn):
        return LifecycleHook(name, fn)
    return wrapper
