from browser import window
from .object import Object


class List(Object):
    @staticmethod
    def __unwraps__():
        return list, tuple

    @staticmethod
    def __can_wrap__(obj):
        return window.Array.isArray(obj) and not isinstance(obj, list)

    def _slice(self, slc):
        if isinstance(slc, int):
            if slc < 0:
                slc = len(self) + slc
            return slc, slc+1
        start = slc.start if slc.start is not None else 0
        stop = slc.stop if slc.stop is not None else len(self)
        return start, stop

    def __eq__(self, other):
        return other == [i for i in self]

    def __mul__(self, other):
        return [i for i in self]*other

    def index(self, obj, start=0, _stop=-1):
        index = self._js.indexOf(Object.to_js(obj), start)
        if index == -1:
            raise ValueError("{} not in list".format(obj))
        return index

    def extend(self, iterable):
        self._js.push(*(i for i in iterable))

    def __len__(self):
        return self._js.length

    def __contains__(self, item):
        try:
            self.index(item)
            return True
        except ValueError:
            return False

    def __imul__(self, other):
        raise NotImplementedError()

    def count(self, obj):
        return [i for i in self].count(obj)

    def reverse(self):
        self._js.reverse()

    def __delitem__(self, key):
        start, stop = self._slice(key)
        self._js.splice(start, stop-start)

    def __setitem__(self, key, value):
        start, stop = self._slice(key)
        value = value if isinstance(value, list) else [value]
        self._js.splice(start, stop-start, *value)

    def __getitem__(self, item):
        start, stop = self._slice(item)
        value = self._js.slice(start, stop)
        if isinstance(item, int):
            return Object.from_js(value[0])
        return [Object.from_js(i) for i in value]

    def __reversed__(self):
        raise NotImplementedError()

    def __rmul__(self, other):
        raise NotImplemented()

    def append(self, obj):
        self._js.push(Object.to_js(obj))

    def insert(self, index, obj):
        self._js.splice(index, 0, Object.to_js(obj))

    def remove(self, obj):
        index = self._js.indexOf(Object.to_js(obj))
        while index != -1:
            del self[self._js.indexOf(Object.to_js(obj))]
            index = self._js.indexOf(Object.to_js(obj))

    def __iadd__(self, other):
        raise NotImplemented()

    def __iter__(self):
        def _iter(lst):
            for i in range(lst.__len__()):
                yield lst[i]
        return _iter(self)

    def pop(self, index=-1):
        return Object.from_js(self._js.splice(index, 1)[0])

    def sort(self, key=None, reverse=False):
        self[:] = sorted(self, key=key, reverse=reverse)

    def __add__(self, other):
        raise NotImplemented()

    def clear(self):
        raise NotImplemented()

    def copy(self):
        raise NotImplemented()

    def __set__(self, new):
        self[:] = new

    def __repr__(self):
        return "[{}]".format(", ".join(repr(i) for i in self))

    def __py__(self):
        return [Object.to_py(item) for item in self]

    def __js__(self):
        if isinstance(self, (list, tuple)):
            return window.Array(*[Object.to_js(item) for item in self])
        return self._js


Object.SubClasses.append(List)
