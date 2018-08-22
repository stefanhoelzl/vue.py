from .base import VueDecorator


class Plugin(VueDecorator):
    __key__ = "plugins"

    def __init__(self, plugins):
        self.__value__ = list(plugins)

