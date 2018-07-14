"""stub to avoid import errors"""


class window:
    String = None
    Number = None
    Object = None
    Boolean = None

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
