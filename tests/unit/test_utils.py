import pytest
from unittest import mock
from vue import utils
from vue.utils import *


@pytest.fixture
def fix_load_and_window():
    utils.CACHE.clear()

    class WindowMock:
        def __getattr__(self, item):
            return item

    class LoadMock:
        def __init__(self):
            self.call_count = 0

        def __call__(self, path):
            self.call_count += 1
            path, mods = path.split(";")
            mods = mods.split(",")
            for mod in mods:
                if mod:
                    setattr(WindowMock, mod, mod)

    with mock.patch.object(utils, "load", new=LoadMock()), mock.patch.object(
        utils, "window", new=WindowMock
    ):
        yield


@pytest.mark.usefixtures("fix_load_and_window")
class TestJsLoad:
    def test_single(self):
        assert "a" == js_load("path;a")

    def test_multiple(self):
        assert {"a": "a", "b": "b"} == js_load("path;a,b")

    def test_different(self):
        assert "a" == js_load("first;a")
        assert "b" == js_load("second;b")
        assert 2 == utils.load.call_count

    def test_using_cache(self):
        assert "a" == js_load("path;a")
        assert "a" == js_load("path;a")
        assert 1 == utils.load.call_count

    def test_none(self):
        assert js_load("path;") is None

    def test_ignore_dollar(self):
        assert js_load("path;$test") is None


class TestJsLib:
    def test_getattr_of_window(self):
        class WindowMock:
            attribute = "ATTRIBUTE"

        with mock.patch.object(utils, "window", new=WindowMock):
            assert "ATTRIBUTE" == js_lib("attribute")

    def test_get_default(self):
        class AttributeWithDefault:
            default = "DEFAULT"

            def __dir__(self):
                return ["default"]

        class WindowMock:
            attribute = AttributeWithDefault()

        with mock.patch.object(utils, "window", new=WindowMock):
            assert "DEFAULT" == js_lib("attribute")
