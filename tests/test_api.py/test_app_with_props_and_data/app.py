from vue import *


def app_with_props_data(el):
    class App(VueComponent):
        text: str
        template = """
        <div id="el">{{ text }}</div>
        """

    return App(el, props_data={"text": "TEXT"})


app = app_with_props_data("#app")
