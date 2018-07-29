from unittest import mock
import asyncio

from vue import *


def test_empty():
    class Empty(VueComponent):
        pass
    assert {} == Empty.init_dict()


def test_method():
    class Component(VueComponent):
        def do(self, event):
            return self, event

    vue_dict = Component.init_dict()
    assert "do" in vue_dict["methods"]
    method = vue_dict["methods"]["do"]
    with mock.patch("vue.decorators.base.javascript.this", return_value="THIS"):
        assert "SELF", "EVENT" == method("EVENT")


def test_method_as_coroutine():
    class Component(VueComponent):
        @asyncio.coroutine
        def co(self):
            return self

    assert "co" in Component.init_dict()["methods"]


def test_data():
    class Component(VueComponent):
        attribute = 1
    assert {"attribute": 1} == Component.init_dict()["data"]("THIS")


def test_data_as_property():
    class Component(VueComponent):
        @data
        def attribute(self):
            return self

    assert {"attribute": "THIS"} == Component.init_dict()["data"]("THIS")


def test_props():
    class Component(VueComponent):
        prop: int

    init_dict = Component.init_dict()
    assert {"prop": {"type": int, "required": True}} == init_dict["props"]


def test_props_with_default():
    class Component(VueComponent):
        prop: int = 100

    init_dict = Component.init_dict()
    props = {"prop": {"type": int, "default": 100}}
    assert props == init_dict["props"]


def test_props_validator():
    class Component(VueComponent):
        prop: int

        @validator("prop")
        def is_lt_100(self, value):
            return value < 100

    init_dict = Component.init_dict()
    assert not init_dict["props"]["prop"]["validator"](100)
    assert init_dict["props"]["prop"]["validator"](99)


def test_template():
    class Component(VueComponent):
        template = "TEMPLATE"

    init_dict = Component.init_dict()
    assert "TEMPLATE" == init_dict["template"]


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

    init_dict = Component.init_dict()
    assert "beforeCreate" in init_dict
    assert "created" in init_dict
    assert "beforeMount" in init_dict
    assert "mounted" in init_dict
    assert "beforeUpdate" in init_dict
    assert "updated" in init_dict
    assert "beforeDestroy" in init_dict
    assert "destroyed" in init_dict


def test_customize_model():
    class Component(VueComponent):
        model = Model(prop="prop", event="event")

    init_dict = Component.init_dict()
    assert {"prop": "prop", "event": "event"} == init_dict["model"]


def test_filter():
    class Component(VueComponent):
        @staticmethod
        @filters
        def lower_case(value):
            return value.lower()

    init_dict = Component.init_dict()
    assert "abc" == init_dict["filters"]["lower_case"]("Abc")


def test_watch():
    class Component(VueComponent):
        @watch("data")
        def lower_case(self, new, old):
            return old, new

    init_dict = Component.init_dict()
    result = init_dict["watch"]["data"]["handler"]("new", "old")
    assert "new", "old" == result


def test_watch_deep():
    class Component(VueComponent):
        @watch("data", deep=True)
        def lower_case(self, new, old):
            return new, old

    init_dict = Component.init_dict()
    assert init_dict["watch"]["data"]["deep"]


def test_watch_immediate():
    class Component(VueComponent):
        @watch("data", immediate=True)
        def lower_case(self, new, old):
            return new, old

    init_dict = Component.init_dict()
    assert init_dict["watch"]["data"]["immediate"]


def test_function_directive():
    class Component(VueComponent):
        @staticmethod
        @directive
        def focus(el, binding, vnode, old_vnode):
            return el, binding, vnode, old_vnode

    init_dict = Component.init_dict()
    res = ["el", "binding", "vnode", "old_vnode"]
    assert res == init_dict["directives"]["focus"]("el", "binding",
                                                   "vnode", "old_vnode")


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

    init_dict = Component.init_dict()
    directive_map = init_dict["directives"]["focus"]
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

    init_dict = Component.init_dict()
    directive_map = init_dict["directives"]["focus"]
    for fn_name in ("bind", "inserted", "update",
                    "componentUpdated", "unbind"):
        assert "hook" == directive_map[fn_name]()


def test_directive_replace_dash():
    class Component(VueComponent):
        @staticmethod
        @directive
        def focus_dashed(el, binding, vnode, old_vnode):
            return el, binding, vnode, old_vnode

    init_dict = Component.init_dict()
    assert "focus-dashed" in init_dict["directives"]


def test_mixins():
    class Component(VueComponent):
        mixins = [{"created": "fn"}]

    assert [{"created": "fn"}] == Component.init_dict()["mixins"]


def test_vuepy_mixin():
    class MyMixin(VueMixin):
        pass

    class Component(VueComponent):
        mixins = [MyMixin]
    assert [{}] == Component.init_dict()["mixins"]


def test_attributes_from_base_class():
    class Component(VueComponent):
        template = "TEMPLATE"

    class SubComponent(Component):
        pass

    assert "TEMPLATE" == SubComponent.init_dict()["template"]


def test_extends():
    class Component(VueComponent):
        template = "TEMPLATE"

    class SubComponent(Component):
        extends = True

    assert {"template": "TEMPLATE"} == SubComponent.init_dict()["extends"]


def test_template_merging():
    class Base(VueComponent):
        template = "<p>BASE {}</p>"

    class Middle(Base):
        template_slots = "MIDDLE {}"

    class Sub(Middle):
        template_slots = "SUB"

    assert "<p>BASE MIDDLE SUB</p>" == Sub.init_dict()["template"]


def test_template_merging_with_slots():
    class Base(VueComponent):
        template_slots = {"pre": "DEFAULT", "post": "DEFAULT"}
        template = "<p>{pre} {} {post}</p>"

    class WithSlots(Base):
        template_slots = {"pre": "PRE", "default": "SUB"}

    class WithDefault(Base):
        template_slots = "SUB"

    assert "<p>PRE SUB DEFAULT</p>" == WithSlots.init_dict()["template"]
    assert "<p>DEFAULT SUB DEFAULT</p>" == WithDefault.init_dict()["template"]


def test_components():
    class Component(VueComponent):
        components = [{"created": "fn"}]

    assert [{"created": "fn"}] == Component.init_dict()["components"]


def test_vuepy_components():
    class SubComponent(VueComponent):
        pass

    class Component(VueComponent):
        components = [SubComponent]
    assert [{}] == Component.init_dict()["components"]
