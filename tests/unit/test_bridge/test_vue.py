from unittest import mock
import pytest
from .mocks import ArrayMock
from vue.bridge.vue_instance import VueInstance
from browser import window


class TestVue:
    def test_getattr(self):
        class This:
            def __init__(self):
                self.attribute = "value"

        this = This()
        vue = VueInstance(this)
        assert "value" == vue.attribute
        this.attribute = "new_value"
        assert "new_value" == vue.attribute

    def test_get_dollar_attribute(self):
        class This:
            def __getattr__(self, item):
                if item == "$dollar":
                    return "DOLLAR"
                return super().__getattribute__(item)

        vue = VueInstance(This())
        assert "DOLLAR" == vue.dollar
        with pytest.raises(AttributeError):
            assert not vue.no_dollar

    def test_setattr(self):
        class This:
            def __init__(self):
                self.attribute = False

            def __getattr__(self, item):
                if item == "$props":
                    return ()
                return self.__getattribute__(item)

        this = This()
        vue = VueInstance(this)
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
        vue = VueInstance(this)
        list_id = id(this.list)
        with mock.patch.object(window.Array, "isArray", return_value=True):
            vue.list = [0, 1, 2]
        assert [0, 1, 2] == vue.list._data
        assert list_id == id(this.list)
