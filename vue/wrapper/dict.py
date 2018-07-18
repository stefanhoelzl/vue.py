from browser import window
from .object import Object


class Dict(Object):
    @staticmethod
    def __can_wrap__(obj):
        return obj.__class__.__name__ == "JSObject" \
               and not callable(obj) and not isinstance(obj, dict)

    def __eq__(self, other):
        return other == {k: v for k, v in self.items()}

    def __getitem__(self, item):
        return self.from_js_object(self._js[item])

    def __iter__(self):
        return (k for k in self.keys())

    def pop(self, k, **kwargs):
        raise NotImplementedError()

    def popitem(self):
        raise NotImplementedError()

    def setdefault(self, k, default=None):
        if k not in self:
            self[k] = default
        return self[k]

    def __len__(self):
        return len(self.items())

    def __contains__(self, item):
        return item in self.keys()

    def __delitem__(self, key):
        raise NotImplementedError()

    def __setitem__(self, key, value):
        if key not in self:
            window.Vue.set(self._js, key, value)
        else:
            self._js[key] = value

    def get(self, k, default=None):
        if k not in self:
            return default
        return self[k]

    def values(self):
        return window.Object.values(self._js)

    def update(self, __m=None, **kwargs):
        if __m is None:
            __m = {}
        __m.update(kwargs)
        window.Object.assign(self._js, __m)

    def clear(self):
        raise NotImplementedError()

    @classmethod
    def fromkeys(seq):
        raise NotImplementedError()

    def copy(self):
        raise NotImplementedError()

    def items(self):
        return window.Object.entries(self._js)

    def keys(self):
        return window.Object.keys(self._js)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "{{{}}}".format(
            ", ".join("{!r}: {!r}".format(k, v) for k, v in self.items())
        )

    def __set__(self, new):
        raise NotImplementedError()

    def __bool__(self):
        return len(self) > 0


Object.Default = Dict
