from unittest import mock
from .mocks import ArrayMock
from vue.wrapper.vue import Vue
from browser import window


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
