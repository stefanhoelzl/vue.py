from contextlib import contextmanager
from unittest import mock

from vue import *


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
            yield self
        self.init_dict = component.call_args[0][1]
        self.register_name = component.call_args[0][0]

    @contextmanager
    def directive(self):
        with mock.patch("vue.vue.window.Vue.directive", new=self) as directive:
            yield self
        self.directive_name = directive.call_args[0][0]
        self._directive = directive.call_args[0][1] \
            if len(directive.call_args[0]) > 1 else None

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
            Component("app", prop="PROP")
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
            name = "drctv"

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
        assert "a" == dirctv._directive("a")

    def test_filter(self):
        with VueMock().filter() as filter_mock:
            Vue.filter("my_filter", lambda val: "filtered({})".format(val))
        assert "my_filter" == filter_mock._filter_name
        assert "filtered(value)" == filter_mock._filter("value")

    def test_filter_useFunctionName(self):
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
