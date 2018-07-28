from .base import VueDecorator


class Mixins(VueDecorator):
    __key__ = "mixins"

    def __init__(self, *mixins):
        self.__value__ = list(mixins)
