from vue import *


def call_emit(el):
    class Emitter(VueComponent):
        template = "<p></p>"

        def created(self):
            self.emit("creation", "YES")

    Emitter.register()

    class App(VueComponent):
        text = "NO"
        template = """
        <div>
            <emitter @creation="change"></emitter>
            <div id='el'>{{ text }}</div>
        </div>
        """

        def change(self, ev=None):
            self.text = ev

    return App(el)


app = call_emit("#app")
