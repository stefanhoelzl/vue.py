"""stub to avoid import errors"""


class window:
    String = str
    Number = int
    Object = object
    Boolean = bool

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
        def set(cls, key, value):
            pass
