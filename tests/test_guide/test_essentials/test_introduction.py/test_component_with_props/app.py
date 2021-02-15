from vue import *


def components_with_properties(el):
    class SubComponent(VueComponent):
        text: str
        sub = "SUB"
        template = """
        <div>
        <h1 id="header">{{ text }}</h1>
        <h2 id="sub">{{ sub }}</h2>
        </div>
        """

    SubComponent.register()

    class App(VueComponent):
        template = """
        <sub-component text="TEXT"></sub-component>
        """

    return App(el)


app = components_with_properties("#app")
