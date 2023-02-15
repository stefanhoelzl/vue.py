from vue import *


class ComputedSetter(VueComponent):
    message = ""

    @computed
    def reversed_message(self):
        return self.message[::-1]

    @reversed_message.setter
    def reversed_message(self, reversed_message):
        self.message = reversed_message[::-1]

    def created(self):
        self.reversed_message = "olleh"

    template = """
    <div>
        <p id="msg">{{ message }}</p>
    </div>
    """


app = ComputedSetter("#app")
