from vue import *


class ComputedPropertiesBasics(VueComponent):
    message = "message"

    @computed
    def reversed_message(self):
        return self.message[::-1]

    template = """
    <div>
        <p id="original">{{ message }}</p>
        <p id="reversed">{{ reversed_message }}</p>
    </div>
    """


app = ComputedPropertiesBasics("#app")
