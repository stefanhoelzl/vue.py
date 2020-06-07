"""stub to avoid import errors"""

import local_storage


def load(path):
    ...


def bind(target, ev):
    ...


class window:
    String = str
    Number = int
    Boolean = bool

    class Object:
        def __init__(self, obj):
            ...

        @staticmethod
        def assign(target, *sources):
            ...

        @staticmethod
        def keys(obj):
            ...

    @staticmethod
    def bind(el, ev):
        ...

    class location:
        hash = ""

    class Array:
        def __init__(self, *objs):
            ...

        @classmethod
        def isArray(cls, obj):
            ...

    class Vuex:
        class Store:
            @classmethod
            def new(cls, *args, **kwargs):
                ...

    class VueRouter:
        @classmethod
        def new(cls, *args, **kwargs):
            ...

    class Vue:
        @classmethod
        def new(cls, *args, **kwargs):
            ...

        @classmethod
        def component(cls, name, opts=None):
            ...

        @classmethod
        def set(cls, obj, key, value):
            ...

        @classmethod
        def delete(cls, obj, key):
            ...

        @classmethod
        def use(cls, plugin, *args, **kwargs):
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


class ajax:
    class ajax:
        def open(self, method, url, asnc):
            ...

        def bind(self, ev, method):
            ...

        def send(self):
            ...
