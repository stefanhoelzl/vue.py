from .base import VueDecorator


class State(VueDecorator):
    __key__ = "state"

    def __init__(self, name, value):
        self.__id__ = name
        self.__value__ = value
