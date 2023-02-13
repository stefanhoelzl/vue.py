from .base import pyjs_bridge, VueDecorator


class Computed(VueDecorator):
    __key__ = "computed"

    def __init__(self, fn):
        self.__id__ = fn.__name__
        self.__name__ = fn.__name__
        self.__call__ = pyjs_bridge(fn)
        self._setter = None

    def setter(self, fn):
        self._setter = pyjs_bridge(fn, inject_vue_instance=True)
        return self

    @property
    def __value__(self):
        vue_object = {"get": self.__call__}
        if self._setter:
            vue_object["set"] = self._setter
        return vue_object


def computed(fn):
    return Computed(fn)
