from .base import VueDecorator


class Extends(VueDecorator):
    __key__ = "extends"

    def __init__(self, init_dict):
        self.__value__ = init_dict
