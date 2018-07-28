from vue import *


def test_local_filter(selenium):
    class ComponentWithFilter(VueComponent):
        message = "Message"

        @staticmethod
        @filters
        def lower_case(value):
            return value.lower()

        template = "<div id='content'>{{ message | lower_case }}</div>"

    with selenium.app(ComponentWithFilter):
        assert selenium.element_has_text("content", "message")


def test_global_filter(selenium):
    def app(el):
        Vue.filter("lower_case", lambda v: v.lower())

        class ComponentUsesGlobalFilter(VueComponent):
            message = "Message"
            template = "<div id='content'>{{ message | lower_case }}</div>"
        return ComponentUsesGlobalFilter(el)

    with selenium.app(app):
        assert selenium.element_has_text("content", "message")
