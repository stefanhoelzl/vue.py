from vue import *


def test_data_must_be_function(selenium):
    def app(el):
        class ClickCounter(VueComponent):
            count = 0
            template = """
            <button v-on:click="count++">{{ count }}</button>
            """
        ClickCounter.register()
        class App(VueComponent):
            template = """
            <div id="components-demo">
              <click-counter id="btn0"></click-counter>
              <click-counter id="btn1"></click-counter>
            </div>
            """

        return App(el)

    with selenium.app(app):
        assert selenium.element_has_text("btn0", "0")
        assert selenium.element_has_text("btn1", "0")
        selenium.find_element_by_id("btn1").click()
        assert selenium.element_has_text("btn0", "0")
        assert selenium.element_has_text("btn1", "1")


def test_register_with_name(selenium):
    def app(el):
        class SubComponent(VueComponent):
            template = """
            <div>TEXT</div>
            """
        SubComponent.register("another-name")
        class App(VueComponent):
            template = """
            <another-name id="component"></another-name>
            """

        return App(el)

    with selenium.app(app):
        assert selenium.element_has_text("component", "TEXT")


def test_passing_data_with_props(selenium):
    def app(el):
        class SubComponent(VueComponent):
            prop = Property()
            template = """
            <div>{{ prop }}</div>
            """
        SubComponent.register()
        class App(VueComponent):
            template = """
            <sub-component id="component" prop="message"></sub-component>
            """

        return App(el)

    with selenium.app(app):
        assert selenium.element_has_text("component", "message")


def test_emit_event(selenium):
    def app(el):
        class SubComponent(VueComponent):
            template = """
            <button @click="$emit('my-event', 'value')"></button>
            """
        SubComponent.register()
        class App(VueComponent):
            text = ""

            def handler(self, value):
                self.text = value

            template = """
            <div>
                <p id="content">{{ text }}</p>
                <sub-component id="component" @my-event='handler'></sub-component>
            </div>
            """

        return App(el)

    with selenium.app(app):
        selenium.find_element_by_id("component").click()
        assert selenium.element_has_text("content", "value")
