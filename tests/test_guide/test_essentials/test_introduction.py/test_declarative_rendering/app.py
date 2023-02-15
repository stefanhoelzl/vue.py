from vue import *


class DeclarativeRendering(VueComponent):
    message = "MESSAGE CONTENT"
    template = "<div id='content'>{{ message }}</div>"


app = DeclarativeRendering("#app")
