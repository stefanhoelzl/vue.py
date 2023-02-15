from vue import *


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


app = app("#app")
