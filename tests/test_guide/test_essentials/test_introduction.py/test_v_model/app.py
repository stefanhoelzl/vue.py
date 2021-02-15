from vue import *


class VModel(VueComponent):
    clicked = False
    template = (
        "<div>"
        "    <p id='p'>{{ clicked }}</p>"
        "    <input type='checkbox' id='c' v-model='clicked'>"
        "</div>"
    )


app = VModel("#app")
