from vue import *


def has_base_attribute(el):
    class A(VueComponent):
        pass

    assert VueComponent == A.__base__


app = has_base_attribute("#app")
