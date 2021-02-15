from .base import pyjs_bridge, VueDecorator


class Render(VueDecorator):
    __key__ = "render"

    def __init__(self, fn):
        self.__value__ = pyjs_bridge(fn, inject_vue_instance=True)
