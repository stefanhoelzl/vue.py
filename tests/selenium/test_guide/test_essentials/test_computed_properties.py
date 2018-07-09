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


def test_watch(selenium):
    class Watch(VueComponent):
        message = Data("message")
        new_val = Data("")

        @watch("message")
        def _message(self, new, old):
            self.new_val = new

        def created(self):
            self.message = "changed"

        template = """
        <div>
            <p id="change">{{ new_val }}</p>
        </div>
        """

    with selenium.app(Watch):
        assert selenium.element_has_text("change", "changed")


def test_computed_setter(selenium):
    class ComputedSetter(VueComponent):
        message = Data("")

        @computed
        def reversed_message(self):
            return self.message[::-1]

        @reversed_message.setter
        def reversed_message(self, reversed_message):
            self.message = reversed_message[::-1]

        def created(self):
            self.reversed_message = "olleh"

        template = """
        <div>
            <p id="msg">{{ message }}</p>
        </div>
        """

    with selenium.app(ComputedSetter):
        assert selenium.element_has_text("msg", "hello")
