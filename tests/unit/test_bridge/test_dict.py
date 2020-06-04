from unittest import mock

import pytest

from tests.unit.test_bridge.mocks import ObjectMock, VueMock

from vue.bridge.dict import window, Dict


@pytest.fixture(scope="module", autouse=True)
def window_object():
    with mock.patch.object(window, "Object", new=ObjectMock), \
         mock.patch.object(window, "Vue", new=VueMock):
        yield


class JsObjectMock:
    def __init__(self, attribtes):
        self.attributes = attribtes

    def __getattr__(self, item):
        return self.attributes[item]

    def __setattr__(self, key, value):
        if key == "attributes":
            super().__setattr__(key, value)
        else:
            self.attributes[key] = value

    def __delattr__(self, item):
        del self.attributes[item]

    def __iter__(self):
        return iter(self.attributes)


def make_dict(dct):
    return Dict(JsObjectMock(dct))


class TestDict:
    def test_getitem(self):
        assert "value" == make_dict({"key": "value"})["key"]

    def test_items(self):
        assert (("a", 1), ("b", 2)) == make_dict({"a": 1, "b": 2}).items()

    def test_eq(self):
        assert {"a": 1} != make_dict({"a": 2})
        assert {"a": 0, "b": 1} == make_dict({"a": 0, "b": 1})

    def test_keys(self):
        assert ("a", "b") == make_dict({"a": 0, "b": 1}).keys()

    def test_iter(self):
        assert ["a", "b"] == list(iter(make_dict({"a": 0, "b": 1})))

    def test_setitem(self):
        d = make_dict({})
        d["a"] = 1
        assert 1 == d["a"]

    def test_contains(self):
        assert "a" in make_dict({"a": 0, "b": 1})

    def test_setdefault(self):
        d = make_dict({})
        assert 1 == d.setdefault("a", 1)
        assert 1 == d.setdefault("a", 2)

    def test_len(self):
        assert 2 == len(make_dict({"a": 0, "b": 1}))

    def test_get(self):
        assert 1 == make_dict({"a": 0, "b": 1}).get("b", "default")
        assert "default" == make_dict({"a": 0, "b": 1}).get("c", "default")

    def test_values(self):
        assert (0, 1) == make_dict({"a": 0, "b": 1}).values()

    def test_repr(self):
        assert str({"a": 0, "b": 1}) == str(make_dict({"a": 0, "b": 1}))

    def test_update(self):
        d = make_dict({"a": 0, "b": 1})
        d.update(a=2)
        assert {"a": 2, "b": 1} == d
        d.update(c=0)
        assert {"a": 2, "b": 1, "c": 0} == d
        d.update({"c": 3, "d": 0})
        assert {"a": 2, "b": 1, "c": 3, "d": 0} == d

    def test_bool(self):
        assert not make_dict({})
        assert make_dict({"a": 0})

    def test_delitem(self):
        d = make_dict({"a": 0, "b": 1})
        del d["a"]
        assert {"b": 1} == d

    def test_pop(self):
        d = make_dict({"a": 0, "b": 1})
        assert 1 == d.pop("b")
        assert {"a": 0} == d

    def test_pop_default(self):
        d = make_dict({"a": 0, "b": 1})
        assert "default" == d.pop("c", "default")
        assert {"a": 0, "b": 1} == d

    def test_pop_key_error(self):
        d = make_dict({"a": 0, "b": 1})
        with pytest.raises(KeyError):
            d.pop("c")

    def test_popitem(self):
        d = make_dict({"a": 2})
        assert ("a", 2) == d.popitem()
        assert {} == d

    def test_clear(self):
        d = make_dict({"a": 0, "b": 1})
        d.clear()
        assert not d

    def test_set(self):
        d = make_dict({"a": 0, "b": 1})
        old_id = id(d)
        d.__set__({"c": 1, "d": 2})
        assert old_id == id(d)
        assert {"c": 1, "d": 2} == d

    def test_getattr(self):
        d = make_dict({"a": 0, "b": 1})
        assert 1 == d.b

    def test_setattr(self):
        d = make_dict({"a": 1})
        d.a = 2
        assert {"a": 2} == d

    def test_str_toString(self):
        d = make_dict({})
        d.toString = lambda: "STRING"
        assert "STRING" == str(d)
