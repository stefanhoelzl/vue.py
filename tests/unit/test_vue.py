from contextlib import contextmanager
from unittest import mock

from vue import *


class VueMock(mock.MagicMock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_dict = None
        self.register_name = None

    @contextmanager
    def new(self):
        with mock.patch("vue.vue.window.Vue.new", new=self) as new:
            yield self
        self.init_dict = new.call_args[0][0]

    @contextmanager
    def component(self):
        with mock.patch("vue.vue.window.Vue.component", new=self) as component:
            yield self
        self.init_dict = component.call_args[0][1]
        self.register_name = component.call_args[0][0]


def test_el():
    class Component(VueComponent):
        pass

    with VueMock().new() as new:
        Component("app")
    assert "app" == new.init_dict["el"]


def test_props_data():
    class Component(VueComponent):
        prop: str

    with VueMock().new() as new:
        Component("app", prop="PROP")
    assert {"prop": "PROP"} == new.init_dict["propsData"]


def test_register():
    class Component(VueComponent):
        pass

    with VueMock().component() as component:
        Component.register()
    assert "Component" == component.register_name

    with VueMock().component() as component:
        Component.register("new-name")
    assert "new-name" == component.register_name
