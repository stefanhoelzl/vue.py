class Object:
    SubClasses = []
    Default = None

    @classmethod
    def sub_classes(cls):
        return cls.SubClasses + ([cls.Default] if cls.Default else [])

    @classmethod
    def from_js(cls, jsobj):
        for sub_class in cls.sub_classes():
            if sub_class.__can_wrap__(jsobj):
                return sub_class(jsobj)
        return jsobj

    @classmethod
    def to_js(cls, obj):
        if isinstance(obj, Object):
            return obj.__js__()
        for sub_class in cls.sub_classes():
            if isinstance(obj, sub_class.__unwraps__()):
                return sub_class.__js__(obj)
        return obj

    @classmethod
    def to_py(cls, obj):
        obj = Object.from_js(obj)
        if isinstance(obj, Object):
            return obj.__py__()
        for sub_class in cls.sub_classes():
            if isinstance(obj, sub_class.__unwraps__()):
                return sub_class.__py__(obj)
        return obj

    @staticmethod
    def __can_wrap__(obj):
        return False

    @staticmethod
    def __unwraps__():
        return ()

    def __init__(self, js):
        self._js = js

    def __js__(self):
        return self._js

    def __py__(self):
        return self
