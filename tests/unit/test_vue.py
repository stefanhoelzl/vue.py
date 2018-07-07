from unittest import mock

from vue.vue import *


def test_vue():
    class This:
        def __init__(self):
            self.attribute = "value"
    this = This()
    vue = Vue(this)
    assert "value" == vue.attribute
    this.attribute = "new_value"
    assert "new_value" == vue.attribute


def test_method():
    class Component(VueComponent):
        @method
        def do(self, event):
            return self, event

    with mock.patch("vue.vue.window.Vue.new") as new, \
        mock.patch("vue.vue.javascript.this", return_value="THIS"):
        c = Component("app")
        assert "SELF", "EVENT" == c.do("EVENT")
    assert "do" in new.call_args[0][0]["methods"]


def test_data():
    class Component(VueComponent):
        attribute = Data(1)

    with mock.patch("vue.vue.window.Vue.new") as new:
        Component("app")
    assert {"attribute": 1} == new.call_args[0][0]["data"]


def test_props():
    class Component(VueComponent):
        prop = Property()

    with mock.patch("vue.vue.window.Vue.new") as new:
        Component("app")
    assert ["prop"] == new.call_args[0][0]["props"]


def test_props_data():
    class Component(VueComponent):
        prop = Property()

    with mock.patch("vue.vue.window.Vue.new") as new:
        Component("app", prop="PROP")
    assert {"prop": "PROP"} == new.call_args[0][0]["propsData"]


def test_template():
    class Component(VueComponent):
        template = "TEMPLATE"

    with mock.patch("vue.vue.window.Vue.new") as new:
        Component("app")
    assert "TEMPLATE" == new.call_args[0][0]["template"]


def test_register():
    class Component(VueComponent):
        template = "TEMPLATE"

    with mock.patch("vue.vue.window.Vue.component") as component:
        Component.register()
    component.assert_called_once()
    assert "Component" == component.call_args[0][0]
    assert "TEMPLATE" == component.call_args[0][1]["template"]


def test_regiser_with_different_name():
    class Component(VueComponent):
        pass

    with mock.patch("vue.vue.window.Vue.component") as component:
        Component.register("my-component")
    component.assert_called_once()
    assert "my-component" == component.call_args[0][0]
