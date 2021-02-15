from vue import *


def app(el):
    class SubComponent(VueComponent):
        prop: int = 100
        content = ""
        template = "<div>{{ content }}</div>"

        def created(self):
            assert 100 == self.prop
            self.content = "text"

    SubComponent.register()

    class App(VueComponent):
        template = """
        <sub-component id="component"></sub-component>
        """

    return App(el)


app = app("#app")
