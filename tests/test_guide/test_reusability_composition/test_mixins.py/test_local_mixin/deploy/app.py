from vue import *


def app(el):
    class MyMixin(VueMixin):
        def created(self):
            print("created")

        @staticmethod
        @filters
        def lower_case(value):
            return value.lower()

    class ComponentUsesGlobalFilter(VueComponent):
        message = "Message"
        mixins = [MyMixin]
        template = "<div id='content'>{{ message | lower_case }}</div>"

    return ComponentUsesGlobalFilter(el)


app = app("#app")
