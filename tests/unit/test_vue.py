from contextlib import contextmanager
from unittest import mock

import pytest

from vue import Vue, VueComponent, VueDirective, VueMixin
from vue.bridge.dict import window


@pytest.fixture(autouse=True)
def window_object():
    with mock.patch.object(window, "Object", new=dict):
        yield


class VueMock(mock.MagicMock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_dict = None
        self.register_name = None
        self.directive_name = None
        self._directive = None

    @contextmanager
    def new(self):
        with mock.patch("vue.vue.window.Vue.new", new=self) as new:
            yield self
        self.init_dict = new.call_args[0][0]

    @contextmanager
    def component(self):
        with mock.patch("vue.vue.window.Vue.component", new=self) as component:
            component.side_effect = lambda *args, **kwargs: self.init_dict
            yield self
        self.init_dict = (
            component.call_args[0][1] if len(component.call_args[0]) > 1 else component
        )
        self.register_name = component.call_args[0][0]

    @contextmanager
    def directive(self):
        with mock.patch("vue.vue.window.Vue.directive", new=self) as drctv:
            drctv.side_effect = lambda *args, **kwargs: self._directive
            yield self
        self.directive_name = drctv.call_args[0][0]
        self._directive = drctv.call_args[0][1] if len(drctv.call_args[0]) > 1 else None

    @contextmanager
    def filter(self):
        with mock.patch("vue.vue.window.Vue.filter", new=self) as flt:
            yield self
        flt._filter_name = flt.call_args[0][0]
        flt._filter = flt.call_args[0][1]

    @contextmanager
    def mixin(self):
        with mock.patch("vue.vue.window.Vue.mixin", new=self) as mixin:
            yield self
        mixin.init_dict = mixin.call_args[0][0]

    @contextmanager
    def use(self):
        with mock.patch("vue.vue.window.Vue.use", new=self) as use:
            yield self
        use.plugin = use.call_args[0][0]


class TestVueComponent:
    def test_el(self):
        class Component(VueComponent):
            pass

        with VueMock().new() as new:
            Component("app")
        assert "app" == new.init_dict["el"]

    def test_props_data(self):
        class Component(VueComponent):
            prop: str

        with VueMock().new() as new:
            Component("app", props_data={"prop": "PROP"})
        assert {"prop": "PROP"} == new.init_dict["propsData"]

    def test_register(self):
        class Component(VueComponent):
            pass

        with VueMock().component() as component:
            Component.register()
        assert "Component" == component.register_name

        with VueMock().component() as component:
            Component.register("new-name")
        assert "new-name" == component.register_name


class TestVue:
    def test_directive(self):
        class Drctv(VueDirective):
            def bind(self):
                pass

        with VueMock().directive() as dirctv:
            Vue.directive("directive", Drctv)
        assert "directive" == dirctv.directive_name
        assert "bind" in dirctv._directive

    def test_directive_with_implicit_name(self):
        class Drctv(VueDirective):
            def bind(self):
                pass

        with VueMock().directive() as dirctv:
            Vue.directive(Drctv)
        assert "drctv" == dirctv.directive_name
        assert "bind" in dirctv._directive

    def test_function_directive(self):
        def function_directive(a):
            return a

        with VueMock().directive() as dirctv:
            Vue.directive("my-directive", function_directive)
        assert "my-directive" == dirctv.directive_name
        assert "a" == dirctv._directive("a")

    def test_function_directive_with_implicit_name(self):
        def function_directive(a):
            return a

        with VueMock().directive() as dirctv:
            Vue.directive(function_directive)
        assert "function_directive" == dirctv.directive_name
        assert "a" == dirctv._directive("a")

    def test_directive_getter(self):
        with VueMock().directive() as drctv:
            drctv._directive = "DIRECTIVE"
            drctv.directive_name = "my-directive"
            assert "DIRECTIVE" == Vue.directive("my-durective")

    def test_filter(self):
        with VueMock().filter() as filter_mock:
            Vue.filter("my_filter", lambda val: "filtered({})".format(val))
        assert "my_filter" == filter_mock._filter_name
        assert "filtered(value)" == filter_mock._filter("value")

    def test_filter_use_function_name(self):
        def flt(v):
            return "filtered({})".format(v)

        with VueMock().filter() as filter_mock:
            Vue.filter(flt)
        assert "flt" == filter_mock._filter_name
        assert "filtered(value)" == filter_mock._filter("value")

    def test_mixin(self):
        class Mixin(VueMixin):
            def created(self):
                return "created"

        with VueMock().mixin() as mixin_mock:
            Vue.mixin(Mixin)
        assert "created" == mixin_mock.init_dict["created"]()

    def test_use(self):
        with VueMock().use() as use:
            Vue.use("Plugin")
        assert "Plugin" == use.plugin

    def test_component(self):
        with VueMock().component() as component:
            Vue.component("my-component", {"a": 0})
        assert {"a": 0} == component.init_dict
        assert "my-component" == component.register_name

    def test_vuepy_component(self):
        class MyComponent(VueComponent):
            pass

        with VueMock().component() as component:
            Vue.component("my-component", MyComponent)
        assert {} == component.init_dict
        assert "my-component" == component.register_name

    def test_vuepy_component_implicit_naming(self):
        class MyComponent(VueComponent):
            pass

        with VueMock().component() as component:
            Vue.component(MyComponent)
        assert {} == component.init_dict
        assert "MyComponent" == component.register_name

    def test_component_getter(self):
        with VueMock().component() as comp:
            comp.init_dict = {"a": 0}
            component = Vue.component("my-component")
        assert {"a": 0} == component
