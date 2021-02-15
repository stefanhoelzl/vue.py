from .base import VueDecorator


class Components(VueDecorator):
    __key__ = "components"

    def __init__(self, *mixins):
        self.__value__ = list(mixins)
