from vue import *


def test_inline_handlers(selenium):
    class InlineHandler(VueComponent):
        message = ""
        def change(self, to):
            self.message = to
        template = """
        <button @click="change('changed')" id="btn">{{ message }}</button>
        """

    with selenium.app(InlineHandler):
        assert selenium.element_has_text("btn", "")
        selenium.find_element_by_id("btn").click()
        assert selenium.element_has_text("btn", "changed")
