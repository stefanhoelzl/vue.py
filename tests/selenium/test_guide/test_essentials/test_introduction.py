from vue import *


def test_declarative_rendering(selenium):
    class DeclarativeRendering(VueComponent):
        message = Data("MESSAGE CONTENT")
        template = "<div id='content'>{{ message }}</div>"

    with selenium.app(DeclarativeRendering):
        assert selenium.element_has_text("content", "MESSAGE CONTENT")


def test_bind_element_title(selenium):
    class BindElementTitle(VueComponent):
        title = Data("TITLE")
        template = "<div id='withtitle' v-bind:title='title'></div>"

    with selenium.app(BindElementTitle):
        assert selenium.element_attribute_has_value("withtitle",
                                                    "title", "TITLE")


def test_if_condition(selenium):
    class IfCondition(VueComponent):
        show = Data(False)
        template = "<div>" \
                   "    <div id='notpresent' v-if='show'>DONT SHOW</div>" \
                   "    <div id='present' />" \
                   "</div>"

    with selenium.app(IfCondition):
        assert selenium.element_present("present")
        assert selenium.element_not_present("notpresent")


def test_for_loop(selenium):
    class ForLoop(VueComponent):
        items = Data(["0", "1", "2"])
        template = "<ol id='list'>" \
                   "   <li v-for='item in items' :id='item'>{{ item }}</li>" \
                   "</ol>"

    with selenium.app(ForLoop):
        for idx in range(3):
            assert selenium.element_has_text(str(idx), str(idx))


def test_on_click_method(selenium):
    class OnClickMethod(VueComponent):
        message = Data("message")
        template = "<button @click='reverse' id='btn'>{{ message }}</button>"

        @method
        def reverse(self, event):
            self.message = "".join(reversed(self.message))

    with selenium.app(OnClickMethod):
        assert selenium.element_has_text("btn", "message")
        selenium.find_element_by_id("btn").click()
        assert selenium.element_has_text("btn", "egassem")


def test_v_model(selenium):
    class VModel(VueComponent):
        clicked = Data(False)
        template = "<div>" \
                   "    <p id='p'>{{ clicked }}</p>" \
                   "    <input type='checkbox' id='c' v-model='clicked'>" \
                   "</div>"

    with selenium.app(VModel):
        assert selenium.element_has_text("p", "false")
        selenium.find_element_by_id("c").click()
        assert selenium.element_has_text("p", "true")


def test_component(selenium):
    def components(el):
        class SubComponent(VueComponent):
            template = """
            <h1 id="header">HEADER</h1>
            """

        SubComponent.register()

        class App(VueComponent):
            template = """
            <sub-component></sub-component>
            """

        return App(el)

    with selenium.app(components):
        assert selenium.element_has_text("header", "HEADER")


def test_component_with_props(selenium):
    def components_with_properties(el):
        class SubComponent(VueComponent):
            text = Property()
            sub = Data("SUB")
            template = """
            <div>
            <h1 id="header">{{ text }}</h1>
            <h2 id="sub">{{ sub }}</h2>
            </div>
            """

        SubComponent.register()

        class App(VueComponent):
            template = """
            <sub-component text="TEXT"></sub-component>
            """

        return App(el)

    with selenium.app(components_with_properties):
        assert selenium.element_has_text("header", "TEXT")
        assert selenium.element_has_text("sub", "SUB")
