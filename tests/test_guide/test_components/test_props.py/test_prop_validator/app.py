from vue import *


def app(el):
    class SubComponent(VueComponent):
        prop: str

        @validator("prop")
        def is_text(self, value):
            return "text" == value

        template = "<div>{{ prop }}</div>"

    SubComponent.register()

    class App(VueComponent):
        template = """
        <sub-component id="component" prop="not text"></sub-component>
        """

    return App(el)


app = app("#app")
