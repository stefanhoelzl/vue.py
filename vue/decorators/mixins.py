from .base import VueDecorator


class Mixins(VueDecorator):
    __key__ = "mixins"
    __overwrite__ = True

    def __init__(self, *mixins):
        self.__value__ = mixins
