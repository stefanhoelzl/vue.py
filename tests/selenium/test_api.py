from vue import *


def test_app_with_props_and_data(selenium):
    def app_with_props_data(el):
        class App(VueComponent):
            text: str
            template = """
            <div id="el">{{ text }}</div>
            """
        return App(el, text="TEXT")
    with selenium.app(app_with_props_data):
        assert selenium.element_has_text("el", "TEXT")


def test_emit_method(selenium):
    def call_emit(el):
        class Emitter(VueComponent):
            template = "<p></p>"

            def created(self):
                self.emit("creation", "YES")
        Emitter.register()

        class App(VueComponent):
            text = "NO"
            template = """
            <div>
                <emitter @creation="change"></emitter>
                <div id='el'>{{ text }}</div>
            </div>
            """

            def change(self, ev=None):
                self.text = ev
        return App(el)
    with selenium.app(call_emit):
        assert selenium.element_has_text("el", "YES")


def test_extend(selenium):
    def extended_component(el):
        class Base(VueComponent):
            template = "<div id='comps'>{{ components_string }}</div>"
            components = []

            def created(self):
                self.components.append("BASE")

            @computed
            def components_string(self):
                return " ".join(self.components)

        class Sub(Base):
            extends = True

            def created(self):
                self.components.append("SUB")

        return Sub(el)
    with selenium.app(extended_component):
        assert selenium.element_has_text("comps", "BASE SUB")


def test_extend_from_dict(selenium):
    class Component(VueComponent):
        template = "<div id='done'>{{ done }}</div>"
        done = "NO"
        extends = {
            "created": lambda: print("CREATED BASE")
        }

        def created(self):
            print("CREATED SUB")
            self.done = "YES"

    with selenium.app(Component):
        assert selenium.element_has_text("done", "YES")
    assert "CREATED BASE" in selenium.logs[-2]["message"]
    assert "CREATED SUB" in selenium.logs[-1]["message"]
