class Object:
    SubClasses = []
    Default = None

    @classmethod
    def from_js_object(cls, jsobj):
        for sub_class in cls.SubClasses:
            if sub_class.__can_wrap__(jsobj):
                return sub_class(jsobj)
        if cls.Default and cls.Default.__can_wrap__(jsobj):
            return cls.Default(jsobj)
        return jsobj

    @classmethod
    def to_js(cls, pyobj):
        if isinstance(pyobj, Object):
            return pyobj._js
        if isinstance(pyobj, list):
            return [Object.to_js(item) for item in pyobj]
        if isinstance(pyobj, dict):
            return {Object.to_js(k): Object.to_js(v) for k, v in pyobj.items()}
        return pyobj

    @staticmethod
    def __can_wrap__(obj):
        return False

    def __init__(self, js):
        self._js = js
