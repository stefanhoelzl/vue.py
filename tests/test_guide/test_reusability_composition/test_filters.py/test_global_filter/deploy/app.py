from vue import *


def app(el):
    Vue.filter("lower_case", lambda v: v.lower())

    class ComponentUsesGlobalFilter(VueComponent):
        message = "Message"
        template = "<div id='content'>{{ message | lower_case }}</div>"

    return ComponentUsesGlobalFilter(el)


app = app("#app")
