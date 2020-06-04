class VueMock:
    @staticmethod
    def set(obj, key, value):
        setattr(obj, key, value)

    @staticmethod
    def delete(obj, key):
        delattr(obj, key)


class ObjectMock:
    def __new__(cls, arg):
        return arg

    @staticmethod
    def assign(target, *sources):
        for source in sources:
            target.attributes.update(source)
        return target
    
    @staticmethod
    def keys(obj):
        return [k for k in obj]


class ArrayMock:
    def __init__(self, *items):
        self._data = list(items)

    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, key, value):
        self._data[key] = value

    @property
    def length(self):
        return len(self._data)

    def push(self, *items):
        self._data.extend(items)

    def splice(self, index, delete_count=None, *items):
        delete_count = delete_count if delete_count is not None \
            else len(self._data)-index
        index = index if index >= 0 else len(self._data)+index
        deleted = self._data[index:index+delete_count]
        self._data = self._data[0:index] \
               + list(items) \
               + self._data[index+delete_count:]
        return deleted

    def slice(self, index, stop=None):
        return self._data[index:stop]

    def indexOf(self, obj, start=0):
        try:
            return self._data.index(obj, start)
        except ValueError:
            return -1

    def reverse(self):
        self._data.reverse()
        return self._data
