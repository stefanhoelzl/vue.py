from vue import *


def app(el):
    class SubComponent(VueComponent):
        template = """
        <div>TEXT</div>
        """

    SubComponent.register("another-name")

    class App(VueComponent):
        template = """
        <another-name id="component"></another-name>
        """

    return App(el)


app = app("#app")
