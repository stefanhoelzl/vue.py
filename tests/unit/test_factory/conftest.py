from unittest import mock
from vue.bridge.list import window as list_window
import pytest


class ArrayMock(list):
    def __new__(cls, *args):
        return list(args)

    @staticmethod
    def isArray(obj):
        return isinstance(obj, list)


@pytest.fixture(scope="module", autouse=True)
def window_object():
    with mock.patch.object(list_window, "Array", new=ArrayMock):
        yield
