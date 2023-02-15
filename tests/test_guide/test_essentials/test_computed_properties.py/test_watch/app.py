from vue import *


class Watch(VueComponent):
    message = "message"
    new_val = ""

    @watch("message")
    def _message(self, new, old):
        self.new_val = new

    def created(self):
        self.message = "changed"

    template = """
    <div>
        <p id="change">{{ new_val }}</p>
    </div>
    """


app = Watch("#app")
