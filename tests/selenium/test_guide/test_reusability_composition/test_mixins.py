from vue import *


def test_local_mixin(selenium):
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

    with selenium.app(app):
        assert selenium.element_has_text("content", "message")
    logs = list(filter(lambda l: "created" in l["message"], selenium.logs))
    assert 1 == len(logs)
