from .base import pyjs_bridge, VueDecorator


class Computed(VueDecorator):
    __key__ = "computed"

    def __init__(self, fn):
        self.__id__ = fn.__name__
        self._getter = pyjs_bridge(fn)
        self._setter = None

    def setter(self, fn):
        self._setter = pyjs_bridge(fn, inject_vue_instance=True)
        return self

    @property
    def __value__(self):
        vue_object = {"get": self._getter}
        if self._setter:
            vue_object["set"] = self._setter
        return vue_object


def computed(fn):
    return Computed(fn)
