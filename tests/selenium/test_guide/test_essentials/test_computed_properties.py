from vue import *


def test_basics(selenium):
    class ComputedPropertiesBasics(VueComponent):
        message = Data("message")

        @computed
        def reversed_message(self):
            return self.message[::-1]

        template = """
        <div>
            <p id="original">{{ message }}</p>
            <p id="reversed">{{ reversed_message }}</p>
        </div>
        """

    with selenium.app(ComputedPropertiesBasics):
        assert selenium.element_has_text("reversed", "egassem")

