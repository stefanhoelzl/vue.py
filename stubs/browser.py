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
            ...

    class Vue:
        @classmethod
        def new(cls, *args, **kwargs):
            ...

        @classmethod
        def component(cls, name, opts):
            ...

        @classmethod
        def set(cls, obj, key, value):
            ...

        @classmethod
        def delete(cls, obj, key):
            ...

        @classmethod
        def use(cls, plugin, *args):
            ...

        @classmethod
        def directive(cls, name, directive=None):
            ...

        @classmethod
        def filter(cls, name, method):
            ...

        @classmethod
        def mixin(cls, mixin):
            ...


class timer:
    @staticmethod
    def set_interval(fn, interval):
        ...
