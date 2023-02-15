from .base import VueDecorator


class State(VueDecorator):
    def __init__(self, name, value):
        self.__key__ = f"state.{name}"
        self.__value__ = value
