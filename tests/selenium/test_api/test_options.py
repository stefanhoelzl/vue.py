from tests.selenium.utils import *

from vue import *


def test_app_with_props_and_data(selenium):
    def app_with_props_data(el):
        class App(VueComponent):
            text = Property()
            template = """
            <div id="el">{{ text }}</div>
            """
        return App(el, text="TEXT")
    prepare(selenium, app_with_props_data)
    assert element_has_text(selenium, "el", "TEXT")
