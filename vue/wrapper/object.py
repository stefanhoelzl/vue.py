class Object:
    SubClasses = []

    @classmethod
    def from_js_object(cls, jsobject):
        for sub_class in cls.SubClasses:
            if sub_class.__can_wrap__(jsobject):
                return sub_class(jsobject)
        return jsobject

    @staticmethod
    def __can_wrap__(obj):
        raise NotImplementedError()

    def __init__(self, js):
        self._js = js
