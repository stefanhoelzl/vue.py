"""stub to avoid import errors"""

import local_storage


def load(path):
    ...


def bind(target, ev):
    ...


class window:
    String = str
    Number = int
    Object = object
    Boolean = bool

    @staticmethod
    def bind(el, ev):
        ...

    class location:
        hash = ''

    class Array:
        @classmethod
        def isArray(cls, obj):
            return False

    class Vue:
        @classmethod
        def new(cls, *args, **kwargs):
            return None

        @classmethod
        def component(cls, name, opts):
            return None

        @classmethod
        def set(cls, obj, key, value):
            ...

        @classmethod
        def delete(cls, obj, key):
            ...
