from browser import window
import javascript


class method:
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)


class Vue:
    def __init__(self, app_id, **data):
        self._vue = None
        window.Vue.new({
            "el": app_id,
            "data": data,
            "created": lambda: self._created(javascript.this()),
            "methods": {m: lambda ev: getattr(self, m)(self, ev)
                        for m in dir(self)
                        if isinstance(getattr(self, m), method)}
        })

    def _created(self, this):
        self._vue = this

    def __getattr__(self, item):
        return getattr(self._vue, item)

    def __setattr__(self, key, value):
        if key not in ["_vue"]:
            setattr(self._vue, key, value)
        object.__setattr__(self, key, value)
