from vue import *
from vue.bridge import VuexInstance


def test_state():
    class Store(VueStore):
        attribute = 1
    assert {"attribute": 1} == Store.init_dict()["state"]


def test_mutation():
    class Store(VueStore):
        @mutation
        def mutation(self, payload):
            return self, payload

    store, arg = Store.init_dict()["mutations"]["mutation"]({}, {"args": (2,)})
    assert 2 == arg
    assert isinstance(store, VuexInstance)


def test_action():
    class Context:
        def __init__(self):
            self.state = {}
            self.getters = {}
            self.rootState = {}
            self.rootGetters = {}
            self.commit = None
            self.dispatch = None

    class Store(VueStore):
        @action
        def action(self, payload):
            return self, payload

    store, arg = Store.init_dict()["actions"]["action"](Context(),
                                                        {"args": (2,)})
    assert 2 == arg
    assert isinstance(store, VuexInstance)


def test_getter():
    class Store(VueStore):
        @staticmethod
        @getter
        def getter(self):
            return self

    vuex = Store.init_dict()["getters"]["getter"]({}, {})
    assert isinstance(vuex, VuexInstance)


def test_getter_method():
    class Store(VueStore):
        @staticmethod
        @getter
        def getter(self, value):
            return self, value

    vuex, value = Store.init_dict()["getters"]["getter"]({}, {})(3)
    assert isinstance(vuex, VuexInstance)
    assert 3 == value


def test_plugin_registration():
    class Store(VueStore):
        plugins = [1]

    assert [1] == Store.init_dict()["plugins"]
