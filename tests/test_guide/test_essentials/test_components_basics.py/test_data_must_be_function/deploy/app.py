from vue import *


def app(el):
    class ClickCounter(VueComponent):
        count = 0
        template = """
        <button v-on:click="count++">{{ count }}</button>
        """

    ClickCounter.register()

    class App(VueComponent):
        template = """
        <div id="components-demo">
          <click-counter id="btn0"></click-counter>
          <click-counter id="btn1"></click-counter>
        </div>
        """

    return App(el)


app = app("#app")
