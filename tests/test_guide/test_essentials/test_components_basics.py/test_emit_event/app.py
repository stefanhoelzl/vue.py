from vue import *


def app(el):
    class SubComponent(VueComponent):
        template = """
        <button @click="$emit('my-event', 'value')"></button>
        """

    SubComponent.register()

    class App(VueComponent):
        text = ""

        def handler(self, value):
            self.text = value

        template = """
        <div>
            <p id="content">{{ text }}</p>
            <sub-component id="component" @my-event='handler'></sub-component>
        </div>
        """

    return App(el)


app = app("#app")
