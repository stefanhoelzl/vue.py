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
