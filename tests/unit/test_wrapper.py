from unittest import mock

import pytest

from vue.wrapper import JSObjectWrapper, window, Vue, List


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


class TestJSObjectWrapper:
    def test_vue(self):
        class This:
            def _isVue(self):
                return True
        assert isinstance(JSObjectWrapper(This()), Vue)

    def test_array(self):
        with mock.patch.object(window.Array, "isArray", return_value=True):
            jow = JSObjectWrapper(ArrayMock(1, 2, 3))
        assert [1, 2, 3] == jow


class TestVue:
    def test_getattr(self):
        class This:
            def __init__(self):
                self.attribute = "value"

        this = This()
        vue = Vue(this)
        assert "value" == vue.attribute
        this.attribute = "new_value"
        assert "new_value" == vue.attribute

    def test_setattr(self):
        class This:
            def __init__(self):
                self.attribute = False

            def __getattr__(self, item):
                if item == "$props":
                    return ()
                return self.__getattribute__(item)

        this = This()
        vue = Vue(this)
        vue.attribute = True
        assert vue.attribute
        assert this.attribute

    def test_set_attribute_with_set(self):
        class This:
            def __init__(self):
                self.list = ArrayMock([1, 2, 3, 4])

            def __getattr__(self, item):
                if item == "$props":
                    return ()
                return self.__getattribute__(item)

        this = This()
        vue = Vue(this)
        list_id = id(this.list)
        with mock.patch.object(window.Array, "isArray", return_value=True):
            vue.list = [0, 1, 2]
        assert [0, 1, 2] == vue.list._data
        assert list_id == id(this.list)


class TestList:
    def test_len(self):
        assert 3 == len(List(ArrayMock(1, 2, 3)))

    def test_getitem(self):
        assert 3 == List(ArrayMock(1, 2, 3))[2]
        assert [2, 3] == List(ArrayMock(1, 2, 3, 4))[1:3]
        assert 3 == List(ArrayMock(1, 2, 3))[-1]
        assert [2] == List(ArrayMock(1, 2, 3))[-2:-1]

    def test_delitem(self):
        l = List(ArrayMock(1, 2, 3))
        del l[1]
        assert [1, 3] == l

    def test_delitem_range(self):
        l = List(ArrayMock(1, 2, 3, 4))
        del l[1:3]
        assert [1, 4] == l

    def test_setitem(self):
        l = List(ArrayMock(1, 2, 3))
        l[1] = 5
        assert [1, 5, 3] == l

    def test_setitem_range(self):
        l = List(ArrayMock(1, 2, 3))
        l[:] = [5]
        assert [5] == l

    def test_setitem_negative(self):
        l = List(ArrayMock(1, 2, 3, 4))
        l[-3:-1] = [8, 9]
        assert [1, 8, 9, 4] == l

    def test_iter(self):
        assert [1, 2, 3] == [i for i in List(ArrayMock(1, 2, 3))]

    def test_eq(self):
        assert [1, 2, 3] == List(ArrayMock(1, 2, 3))

    def test_mul(self):
        assert [1, 2, 1, 2, 1, 2] == List(ArrayMock(1, 2))*3

    def test_index(self):
        assert 3 == List(ArrayMock(1, 2, 3, 4)).index(4)

    def test_index_start(self):
        assert 4 == List(ArrayMock(4, 1, 2, 3, 4)).index(4, start=1)

    def test_index_not_in_list(self):
        with pytest.raises(ValueError):
            List(ArrayMock(1, 2, 3)).index(4)

    def test_extend(self):
        l = List(ArrayMock(1, 2))
        l.extend([3, 4])
        assert [1, 2, 3, 4] == l

    def test_contains(self):
        assert 3 in List(ArrayMock(1, 2, 3))

    def test_count(self):
        assert 2 == List(ArrayMock(1, 2, 1)).count(1)

    def test_repr(self):
        assert "[1, 2, 3]" == repr(List(ArrayMock(1, 2, 3)))

    def test_str(self):
        assert "[1, 2, 3]" == str(List(ArrayMock(1, 2, 3)))

    def test_append(self):
        l = List(ArrayMock(1, 2))
        l.append(3)
        assert [1, 2, 3] == l

    def test_insert(self):
        l = List(ArrayMock(1, 3))
        l.insert(1, 2)
        assert [1, 2, 3] == l

    def test_remove(self):
        l = List(ArrayMock(1, 2, 1, 3))
        l.remove(1)
        assert [2, 3] == l

    def test_pop(self):
        l = List(ArrayMock(1, 2, 3))
        assert 3 == l.pop()

    def test_sort(self):
        l = List(ArrayMock(4, 3, 6, 1))
        l.sort()
        assert [1, 3, 4, 6] == l

    def test_reverse(self):
        l = List(ArrayMock(4, 3, 6, 1))
        l.reverse()
        assert [1, 6, 3, 4] == l

    def test_set(self):
        l = List(ArrayMock(4, 3, 6, 1))
        l.__set__([1, 2, 3, 4])
        assert [1, 2, 3, 4] == l
