from browser import window


class JSObjectWrapper:
    def __new__(cls, jsobject):
        if window.Array.isArray(jsobject):
            return List(jsobject)
        if hasattr(jsobject, "_isVue") and jsobject._isVue:
            return Vue(jsobject)
        return jsobject


class Vue:
    def __init__(self, this):
        self._this = this

    def __getattr__(self, item):
        return JSObjectWrapper(getattr(self._this, item))

    def __setattr__(self, key, value):
        if key in ["_this"]:
            object.__setattr__(self, key, value)
        # elif hasattr(getattr(self, key), "__set__"):
        #     getattr(self, key).__set__(value)
        else:
            setattr(self._this, key, value)


class List:
    def _slice(self, slc):
        if isinstance(slc, int):
            return slc, slc+1
        start = slc.start if slc.start is not None else 0
        stop = slc.stop if slc.stop is not None else len(self)
        return start, stop

    def __init__(self, array):
        self._array = array

    def __eq__(self, other):
        return other == [i for i in self]

    def __mul__(self, other):
        return [i for i in self]*other

    def index(self, obj, start=0, stop=-1):
        index = self._array.indexOf(obj, start)
        if index == -1:
            raise ValueError("{} not in list".format(obj))
        return index

    def extend(self, iterable):
        self._array.push(*(i for i in iterable))

    def __len__(self):
        return self._array.length

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
        self._array.reverse()

    def __delitem__(self, key):
        start, stop = self._slice(key)
        self._array.splice(start, stop-start)

    def __setitem__(self, key, value):
        start, stop = self._slice(key)
        value = value if isinstance(value, list) else [value]
        self._array.splice(start, stop-start, *value)

    def __getitem__(self, item):
        start, stop = self._slice(item)
        value = self._array.slice(start, stop)
        if isinstance(item, int):
            return value[0]
        return value

    def __reversed__(self):
        raise NotImplementedError()

    def __rmul__(self, other):
        raise NotImplemented()

    def append(self, obj):
        self._array.push(obj)

    def insert(self, index, obj):
        self._array.splice(index, 0, obj)

    def remove(self, obj):
        index = self._array.indexOf(obj)
        while index != -1:
            del self[self._array.indexOf(obj)]
            index = self._array.indexOf(obj)

    def __iadd__(self, other):
        raise NotImplemented()

    def __iter__(self):
        def _iter(lst):
            for i in range(len(lst)):
                yield lst[i]
        return _iter(self)

    def pop(self, index=-1):
        return self._array.splice(index, 1)[0]

    def sort(self, key=None, reverse=False):
        self[:] = sorted(self, key=key, reverse=reverse)

    def __add__(self, other):
        raise NotImplemented()

    def clear(self):
        raise NotImplemented()

    def copy(self):
        raise NotImplemented()

    def __set__(self, new):
        raise NotImplementedError()

    def __repr__(self):
        return "[{}]".format(", ".join(repr(i) for i in self))
