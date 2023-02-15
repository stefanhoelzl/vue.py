from vue import *


class InlineHandler(VueComponent):
    message = ""

    def change(self, to):
        self.message = to

    template = """
    <button @click="change('changed')" id="btn">{{ message }}</button>
    """


app = InlineHandler("#app")
