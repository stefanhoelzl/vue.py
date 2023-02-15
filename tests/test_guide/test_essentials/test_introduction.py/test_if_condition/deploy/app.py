from vue import *


class IfCondition(VueComponent):
    show = False
    template = (
        "<div>"
        "    <div id='notpresent' v-if='show'>DONT SHOW</div>"
        "    <div id='present' />"
        "</div>"
    )


app = IfCondition("#app")
