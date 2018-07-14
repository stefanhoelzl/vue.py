from unittest import mock

from vue.vue import *


def test_method():
    class Component(VueComponent):
        def do(self, event):
            return self, event

    with mock.patch("vue.vue.window.Vue.new") as new, \
        mock.patch("vue.vue.javascript.this", return_value="THIS"):
        c = Component("app")
        assert "SELF", "EVENT" == c.do("EVENT")
    assert "do" in new.call_args[0][0]["methods"]


def test_data():
    class Component(VueComponent):
        attribute = 1

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


def test_lifecycle_hooks():
    class Component(VueComponent):
        def before_create(self):
            return self
        def created(self):
            return self
        def before_mount(self):
            return self
        def mounted(self):
            return self
        def before_update(self):
            return self
        def updated(self):
            return self
        def before_destroy(self):
            return self
        def destroyed(self):
            return self

    with mock.patch("vue.vue.window.Vue.component") as component:
        Component.register()
    component.assert_called_once()
    assert "beforeCreate" in component.call_args[0][1]
    assert "created" in component.call_args[0][1]
    assert "beforeMount" in component.call_args[0][1]
    assert "mounted" in component.call_args[0][1]
    assert "beforeUpdate" in component.call_args[0][1]
    assert "updated" in component.call_args[0][1]
    assert "beforeDestroy" in component.call_args[0][1]
    assert "destroyed" in component.call_args[0][1]
