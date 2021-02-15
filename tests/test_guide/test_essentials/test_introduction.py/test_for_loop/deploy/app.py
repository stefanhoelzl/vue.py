from vue import *


class ForLoop(VueComponent):
    items = ["0", "1", "2"]
    template = (
        "<ol id='list'>"
        "   <li v-for='item in items' :id='item'>{{ item }}</li>"
        "</ol>"
    )


app = ForLoop("#app")
