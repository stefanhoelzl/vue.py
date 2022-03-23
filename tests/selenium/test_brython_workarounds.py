import time
from vue import *


def test_inherit_annotations(selenium):
    def inherit_annotations(el):
        class A(VueComponent):
            prop: str

        class B(A):
            pass

        assert "prop" in B.__annotations__, B.__annotations__

    with selenium.app(inherit_annotations):
        time.sleep(0.1)


def test_annotation_value_type(selenium):
    def inherit_annotations(el):
        class A(VueComponent):
            prop: str

        class B(A):
            pass

        assert {"prop": str} == B.__annotations__, B.__annotations__

    with selenium.app(inherit_annotations):
        time.sleep(0.1)


def test_base_attribute(selenium):
    def has_base_attribute(el):
        class A(VueComponent):
            pass

        assert VueComponent == A.__base__

    with selenium.app(has_base_attribute):
        time.sleep(0.1)


def test_object_in_bases(selenium):
    def has_base_attribute(el):
        from vue.vue import Wrapper

        assert (object,) == Wrapper.__bases__

    with selenium.app(has_base_attribute):
        time.sleep(0.1)
