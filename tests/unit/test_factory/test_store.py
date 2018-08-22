from vue import *


def test_state():
    class Store(VueStore):
        attribute = 1
    assert {"attribute": 1} == Store.init_dict()["state"]


def test_mutation():
    class Store(VueStore):
        @staticmethod
        @mutation
        def mutation(state, payload):
            return state, payload

    assert [1, 2] == Store.init_dict()["mutations"]["mutation"](1, 2)


def test_action():
    class Store(VueStore):
        @staticmethod
        @action
        def action(context, payload):
            return context, payload

    assert [1, 2] == Store.init_dict()["actions"]["action"](1, 2, None)
