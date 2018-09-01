from vue.bridge.vuex_instance import VuexInstance


class Getter:
    def __init__(self, **kwargs):
        self.vars = kwargs

    def __getattr__(self, item):
        return self.vars[item]


class Callable:
    def __init__(self):
        self.args = None

    def __call__(self, *args):
        self.args = args


def test_get_state():
    vuex = VuexInstance(state=dict(i=1))
    assert 1 == vuex.i


def test_get_root_state():
    vuex = VuexInstance(root_state=dict(i=1))
    assert 1 == vuex.i


def test_set_state():
    state = dict(i=0)
    vuex = VuexInstance(state=state)
    vuex.i = 1
    assert 1 == state["i"]


def test_set_root_state():
    state = dict(i=0)
    vuex = VuexInstance(root_state=state)
    vuex.i = 1
    assert 1 == state["i"]


def test_access_getter():
    vuex = VuexInstance(getters=Getter(i=1))
    assert 1 == vuex.i


def test_access_root_getter():
    vuex = VuexInstance(root_getters=Getter(i=1))
    assert 1 == vuex.i


def test_access_comit():
    c = Callable()
    vuex = VuexInstance(commit=c)
    vuex.commit("mutation", 1, a=0)
    assert "mutation" == c.args[0]
    assert {"args": (1,), "kwargs": {"a": 0}} == c.args[1]


def test_access_dispatch():
    c = Callable()
    vuex = VuexInstance(dispatch=c)
    vuex.dispatch("action", 1, a=0)
    assert "action" == c.args[0]
    assert {"args": (1,), "kwargs": {"a": 0}} == c.args[1]
