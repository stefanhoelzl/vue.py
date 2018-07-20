from unittest import mock

from vue import *


def test_method():
    class Component(VueComponent):
        def do(self, event):
            return self, event

    with mock.patch("vue.vue.window.Vue.new") as new, \
        mock.patch("vue.decorators.base.javascript.this", return_value="THIS"):
        c = Component("app")
        assert "SELF", "EVENT" == c.do("EVENT")
    assert "do" in new.call_args[0][0]["methods"]


def test_method_as_coroutine():
    import asyncio
    class Component(VueComponent):
        @asyncio.coroutine
        def co(self):
            return self

    with mock.patch("vue.vue.window.Vue.new") as new, \
         mock.patch("vue.decorators.base.javascript.this"):
        Component("app")
    assert "co" in new.call_args[0][0]["methods"]


def test_data():
    class Component(VueComponent):
        attribute = 1

    with mock.patch("vue.vue.window.Vue.new") as new:
        Component("app")
    assert {"attribute": 1} == new.call_args[0][0]["data"]("THIS")


def test_data_as_property():
    class Component(VueComponent):
        @data
        def attribute(self):
            return self

    with mock.patch("vue.vue.window.Vue.new") as new:
        Component("app")
    assert {"attribute": "THIS"} == new.call_args[0][0]["data"]("THIS")


def test_props():
    class Component(VueComponent):
        prop: int

    with mock.patch("vue.vue.window.Vue.new") as new:
        Component("app")
    assert {"prop": {"type": int, "required": True}} \
            == new.call_args[0][0]["props"]


def test_props_with_default():
    class Component(VueComponent):
        prop: int = 100

    with mock.patch("vue.vue.window.Vue.new") as new:
        Component("app")
    props = {"prop": {"type": int, "default": 100}}
    assert props == new.call_args[0][0]["props"]


def test_props_validator():
    class Component(VueComponent):
        prop: int

        @validator("prop")
        def is_lt_100(self, value):
            return value < 100

    with mock.patch("vue.vue.window.Vue.new") as new:
        Component("app")
    assert not new.call_args[0][0]["props"]["prop"]["validator"](100)
    assert new.call_args[0][0]["props"]["prop"]["validator"](99)


def test_props_data():
    class Component(VueComponent):
        prop: str

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


def test_customize_model():
    class Component(VueComponent):
        model = Model(prop="prop", event="event")

    with mock.patch("vue.vue.window.Vue.new") as new:
        Component("app")
    assert {"prop": "prop", "event": "event"} == new.call_args[0][0]["model"]


def test_filter():
    class Component(VueComponent):
        @staticmethod
        @filters
        def lower_case(value):
            return value.lower()

    with mock.patch("vue.vue.window.Vue.new") as new:
        Component("app")
    assert "abc" == new.call_args[0][0]["filters"]["lower_case"]("Abc")


def test_watch():
    class Component(VueComponent):
        @watch("data")
        def lower_case(self, new, old):
            return old, new

    with mock.patch("vue.vue.window.Vue.new") as new:
        Component("app")
    result = new.call_args[0][0]["watch"]["data"]["handler"]("new", "old")
    assert "new", "old" == result


def test_watch_deep():
    class Component(VueComponent):
        @watch("data", deep=True)
        def lower_case(self, new, old):
            return new, old

    with mock.patch("vue.vue.window.Vue.new") as new:
        Component("app")
    is_deep = new.call_args[0][0]["watch"]["data"]["deep"]
    assert is_deep


def test_watch_immediate():
    class Component(VueComponent):
        @watch("data", immediate=True)
        def lower_case(self, new, old):
            return new, old

    with mock.patch("vue.vue.window.Vue.new") as new:
        Component("app")
    is_immediate = new.call_args[0][0]["watch"]["data"]["immediate"]
    assert is_immediate


def test_function_directive():
    class Component(VueComponent):
        @staticmethod
        @directive
        def focus(el, binding, vnode, old_vnode):
            return el, binding, vnode, old_vnode

    with mock.patch("vue.vue.window.Vue.new") as new:
        Component("app")
    res = ["el", "binding", "vnode", "old_vnode"]
    assert res == new.call_args[0][0]["directives"]["focus"]("el",
                                                             "binding",
                                                             "vnode",
                                                             "old_vnode")


def test_full_directive_different_hooks():
    class Component(VueComponent):
        @staticmethod
        @directive("focus")
        def bind():
            return "bind"

        @staticmethod
        @directive("focus")
        def inserted():
            return "inserted"

        @staticmethod
        @directive("focus")
        def update():
            return "update"

        @staticmethod
        @directive("focus")
        def component_updated():
            return "componentUpdated"

        @staticmethod
        @directive("focus")
        def unbind():
            return "unbind"

    with mock.patch("vue.vue.window.Vue.new") as new:
        Component("app")
    directive_map = new.call_args[0][0]["directives"]["focus"]
    for fn_name in ("bind", "inserted", "update",
                    "componentUpdated", "unbind"):
        assert fn_name == directive_map[fn_name]()


def test_full_directive_single_hook():
    class Component(VueComponent):
        @staticmethod
        @directive("focus", "bind", "inserted",
                   "update", "component_updated", "unbind")
        def hook():
            return "hook"

    with mock.patch("vue.vue.window.Vue.new") as new:
        Component("app")
    directive_map = new.call_args[0][0]["directives"]["focus"]
    for fn_name in ("bind", "inserted", "update",
                    "componentUpdated", "unbind"):
        assert "hook" == directive_map[fn_name]()


def test_directive_replace_dash():
    class Component(VueComponent):
        @staticmethod
        @directive
        def focus_dashed(el, binding, vnode, old_vnode):
            return el, binding, vnode, old_vnode

    with mock.patch("vue.vue.window.Vue.new") as new:
        Component("app")
    assert "focus-dashed" in new.call_args[0][0]["directives"]
