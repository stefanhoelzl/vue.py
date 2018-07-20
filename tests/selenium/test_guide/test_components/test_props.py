import pytest

from vue import *


def test_prop_types(selenium):
    def app(el):
        class SubComponent(VueComponent):
            prop: int
            content = ""
            template = "<div>{{ content }}</div>"

            def created(self):
                assert isinstance(self.prop, int)
                self.content = "text"

        SubComponent.register()
        class App(VueComponent):
            template = """
            <sub-component id="component" :prop="100"></sub-component>
            """

        return App(el)

    with selenium.app(app):
        assert selenium.element_has_text("component", "text")


def test_prop_default(selenium):
    def app(el):
        class SubComponent(VueComponent):
            prop: int = 100
            content = ""
            template = "<div>{{ content }}</div>"

            def created(self):
                assert 100 == self.prop
                self.content = "text"

        SubComponent.register()
        class App(VueComponent):
            template = """
            <sub-component id="component"></sub-component>
            """

        return App(el)

    with selenium.app(app):
        assert selenium.element_has_text("component", "text")


def test_prop_required(selenium):
    def app(el):
        class SubComponent(VueComponent):
            prop: int
            content = ""
            template = "<div>{{ content }}</div>"

            def created(self):
                self.content = "text"

        SubComponent.register()
        class App(VueComponent):
            template = """
            <sub-component id="component">SUB</sub-component>
            """

        return App(el)

    with pytest.raises(Exception) as excinfo:
        with selenium.app(app):
            selenium.element_has_text("component", "text")
    assert "[Vue warn]: Missing required prop:" \
           in excinfo.value.errors[0]["message"]


def test_prop_as_initial_value(selenium):
    def app(el):
        class SubComponent(VueComponent):
            prop: str

            @data
            def cnt(self):
                return self.prop

            template = "<div>{{ cnt }}</div>"

        SubComponent.register()

        class App(VueComponent):
            template = """
            <sub-component id="component" prop="text"></sub-component>
            """

        return App(el)

    with selenium.app(app):
        assert selenium.element_has_text("component", "text")


def test_dont_allow_write_prop(selenium):
    def app(el):
        class SubComponent(VueComponent):
            prop: str

            def created(self):
                self.prop = "HALLO"

            template = "<div>{{ prop }}</div>"

        SubComponent.register()

        class App(VueComponent):
            template = """
            <sub-component id="component" prop="text"></sub-component>
            """

        return App(el)

    with pytest.raises(Exception):
        with selenium.app(app):
            with pytest.raises(TimeoutError):
                selenium.element_has_text("component", "HALLO")


def test_prop_validator(selenium):
    def app(el):
        class SubComponent(VueComponent):
            prop: str

            @validator("prop")
            def is_text(self, value):
                return "text" == value

            template = "<div>{{ prop }}</div>"

        SubComponent.register()

        class App(VueComponent):
            template = """
            <sub-component id="component" prop="not text"></sub-component>
            """

        return App(el)

    with pytest.raises(Exception) as excinfo:
        with selenium.app(app):
            assert selenium.element_has_text("component", "not text")
    assert "[Vue warn]: Invalid prop: custom validator check failed for prop" \
           in excinfo.value.errors[0]["message"]
