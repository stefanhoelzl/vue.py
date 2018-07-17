from browser import window

class Object:
    SubClasses = []
    Default = None

    @classmethod
    def from_js_object(cls, jsobject):
        for sub_class in cls.SubClasses:
            if sub_class.__can_wrap__(jsobject):
                return sub_class(jsobject)
        if jsobject.__class__.__name__ == "JSObject" and cls.Default:
            return cls.Default(jsobject)
        return jsobject

    @staticmethod
    def __can_wrap__(obj):
        return False

    def __init__(self, js):
        self._js = js
