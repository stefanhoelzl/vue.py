from vue import *


def has_base_attribute(el):
    from vue.vue import Wrapper

    assert (object,) == Wrapper.__bases__


app = has_base_attribute("#app")
