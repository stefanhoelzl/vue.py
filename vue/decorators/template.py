from .base import VueDecorator


class Template(VueDecorator):
    __key__ = "template"
    __overwrite__ = True

    def __init__(self, template):
        self.__value__ = template
