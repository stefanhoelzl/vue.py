from vue import *


class OnClickMethod(VueComponent):
    message = "message"
    template = "<button @click='reverse' id='btn'>{{ message }}</button>"

    def reverse(self, event):
        self.message = "".join(reversed(self.message))


app = OnClickMethod("#app")
