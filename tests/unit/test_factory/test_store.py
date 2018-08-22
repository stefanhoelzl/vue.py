from vue import *


def test_state():
    class Store(VueStore):
        attribute = 1
    assert {"attribute": 1} == Store.init_dict()["state"]
