from vue import *


def components(el):
    class SubComponent(VueComponent):
        template = """
        <h1 id="header">HEADER</h1>
        """

    SubComponent.register()

    class App(VueComponent):
        template = """
        <sub-component></sub-component>
        """

    return App(el)


app = components("#app")
