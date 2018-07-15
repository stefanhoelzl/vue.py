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
