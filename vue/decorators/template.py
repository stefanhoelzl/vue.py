from .base import VueDecorator


class Template(VueDecorator):
    __key__ = "template"

    def __init__(self, template):
        self.__value__ = template
