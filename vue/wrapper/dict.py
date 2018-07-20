from browser import window
from .object import Object


class Dict(Object):
    @staticmethod
    def __unwraps__():
        return dict

    @staticmethod
    def __can_wrap__(obj):
        return (str(type(obj)) == "<undefined>") or \
               (obj.__class__.__name__ == "JSObject"
                and not callable(obj) and not isinstance(obj, dict))

    def __eq__(self, other):
        return other == {k: v for k, v in self.items()}

    def __getitem__(self, item):
        if str(type(self._js)) == "<undefined>":  # Workaround
            for key, value in window.Object.entries(self._js):
                if key == item:
                    return Object.from_js(value)
        return Object.from_js(self._js[item])

    def __iter__(self):
        return (k for k in self.keys())

    def pop(self, k, default=...):
        if k not in self and not isinstance(default, type(Ellipsis)):
            return default
        item = self[k]
        del self[k]
        return item

    def popitem(self):
        key = self.keys()[0]
        return key, self.pop(key)

    def setdefault(self, k, default=None):
        if k not in self:
            self[k] = default
        return self[k]

    def __len__(self):
        return len(self.items())

    def __contains__(self, item):
        return Object.to_js(item) in self.keys()

    def __delitem__(self, key):
        window.Vue.delete(self._js, Object.to_js(key))

    def __setitem__(self, key, value):
        if key not in self:
            window.Vue.set(self._js, Object.to_js(key), Object.to_js(value))
        else:
            self._js[Object.to_js(key)] = Object.to_js(value)

    def get(self, k, default=None):
        if k not in self:
            return default
        return self[k]

    def values(self):
        return tuple(self[key] for key in self)

    def update(self, _m=None, **kwargs):
        if _m is None:
            _m = {}
            _m.update(kwargs)
        window.Object.assign(self._js, Object.to_js(_m))

    def clear(self):
        while len(self) > 0:
            self.popitem()

    @classmethod
    def fromkeys(seq):
        raise NotImplementedError()

    def copy(self):
        raise NotImplementedError()

    def items(self):
        return tuple((key, self[key]) for key in self)

    def keys(self):
        if str(type(self._js)) == "<undefined>":  # Workaround
            return window.Object.keys(self._js)
        return [Object.from_js(key) for key in self._js]

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "{{{}}}".format(
            ", ".join("{!r}: {!r}".format(k, v) for k, v in self.items())
        )

    def __set__(self, new):
        self.clear()
        self.update(new)

    def __bool__(self):
        return len(self) > 0

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        if key in ["_js"]:
            return super().__setattr__(key, value)
        self[key] = value

    def __py__(self):
        return {Object.to_py(k): Object.to_py(v) for k, v in self.items()}

    def __js__(self):
        if isinstance(self, dict):
            return {Object.to_js(k): Object.to_js(v) for k, v in self.items()}
        return self._js


Object.Default = Dict
