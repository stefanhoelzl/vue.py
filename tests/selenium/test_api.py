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
