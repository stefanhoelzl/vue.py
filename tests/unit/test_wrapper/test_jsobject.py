from unittest import mock

from browser import window

from vue.wrapper import Object
from vue.wrapper.vue_instance import VueInstance

from .mocks import ArrayMock


class TestJSObjectWrapper:
    def test_vue(self):
        class This:
            def _isVue(self):
                return True
        assert isinstance(Object.from_js(This()), VueInstance)

    def test_array(self):
        with mock.patch.object(window.Array, "isArray", return_value=True):
            obj = Object.from_js(ArrayMock(1, 2, 3))
        assert [1, 2, 3] == obj

    def test_dict(self):
        assert {"a": 1, "b": 2} == Object.from_js({"a": 1, "b": 2})
