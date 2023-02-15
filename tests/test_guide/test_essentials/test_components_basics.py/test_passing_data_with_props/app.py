from vue import *


def app(el):
    class SubComponent(VueComponent):
        prop: str
        template = """
        <div>{{ prop }}</div>
        """

    SubComponent.register()

    class App(VueComponent):
        template = """
        <sub-component id="component" prop="message"></sub-component>
        """

    return App(el)


app = app("#app")
