class Dict:
    def __getitem__(self, item):
        raise NotImplementedError()

    def __iter__(self):
        raise NotImplementedError()

    def pop(self, k):
        raise NotImplementedError()

    def popitem(self):
        raise NotImplementedError()

    def setdefault(self, k, default=None):
        raise NotImplementedError()

    def __len__(self):
        raise NotImplementedError()

    def __contains__(self, item):
        raise NotImplementedError()

    def __delitem__(self, key):
        raise NotImplementedError()

    def __setitem__(self, key, value):
        raise NotImplementedError()

    def get(self, k):
        raise NotImplementedError()

    def values(self):
        raise NotImplementedError()

    def update(self, __m=None, **kwargs):
        raise NotImplementedError()

    def clear(self):
        raise NotImplementedError()

    @classmethod
    def fromkeys(seq):
        raise NotImplementedError()

    def copy(self):
        raise NotImplementedError()

    def items(self):
        raise NotImplementedError()

    def keys(self):
        raise NotImplementedError()

    def __set__(self, new):
        raise NotImplementedError()
