from vue import *


class ComponentWithFilter(VueComponent):
    message = "Message"

    @staticmethod
    @filters
    def lower_case(value):
        return value.lower()

    template = "<div id='content'>{{ message | lower_case }}</div>"


app = ComponentWithFilter("#app")
