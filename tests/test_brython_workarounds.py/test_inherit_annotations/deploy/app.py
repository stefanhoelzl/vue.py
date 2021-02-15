from vue import *


def inherit_annotations(el):
    class A(VueComponent):
        prop: str

    class B(A):
        pass

    assert {"prop": str} == B.__annotations__


app = inherit_annotations("#app")
