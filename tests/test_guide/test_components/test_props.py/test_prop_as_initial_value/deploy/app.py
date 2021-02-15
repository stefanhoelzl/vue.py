from vue import *


def app(el):
    class SubComponent(VueComponent):
        prop: str

        @data
        def cnt(self):
            return self.prop

        template = "<div>{{ cnt }}</div>"

    SubComponent.register()

    class App(VueComponent):
        template = """
        <sub-component id="component" prop="text"></sub-component>
        """

    return App(el)


app = app("#app")
