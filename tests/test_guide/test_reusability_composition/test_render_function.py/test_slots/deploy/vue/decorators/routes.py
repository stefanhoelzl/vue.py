from .base import VueDecorator


class Routes(VueDecorator):
    __key__ = "routes"

    def __init__(self, routes):
        self.__value__ = list(routes)
