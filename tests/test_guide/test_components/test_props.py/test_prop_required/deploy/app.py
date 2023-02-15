from vue import *


def app(el):
    class SubComponent(VueComponent):
        prop: int
        content = ""
        template = "<div>{{ content }}</div>"

        def created(self):
            self.content = "text"

    SubComponent.register()

    class App(VueComponent):
        template = """
        <sub-component id="component">SUB</sub-component>
        """

    return App(el)


app = app("#app")
