import pytest
from unittest import mock
from vue import js_import, utils


@pytest.fixture(autouse=True, scope="function")
def fix_and_window():
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

    with mock.patch.object(utils, "load", new=LoadMock()), \
         mock.patch.object(utils, "window", new=WindowMock):
        yield


class TestJsImport:
    def test_single(self):
        assert "a" == js_import("path;a")

    def test_multiple(self):
        assert {"a": "a", "b": "b"} == js_import("path;a,b")

    def test_different(self):
        assert "a" == js_import("first;a")
        assert "b" == js_import("second;b")
        assert 2 == utils.load.call_count

    def test_using_cache(self):
        assert "a" == js_import("path;a")
        assert "a" == js_import("path;a")
        assert 1 == utils.load.call_count

    def test_none(self):
        assert js_import("path;") is None

    def test_ignore_dollar(self):
        assert js_import("path;$test") is None
