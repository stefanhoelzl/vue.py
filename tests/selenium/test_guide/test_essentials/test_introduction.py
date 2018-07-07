from tests.selenium.utils import *

from vue import *


def test_declarative_rendering(selenium):
    class DeclarativeRendering(VueComponent):
        message = Data("MESSAGE CONTENT")
        template = "<div id='content'>{{ message }}</div>"
    prepare(selenium, DeclarativeRendering)
    assert element_has_text(selenium, "content", "MESSAGE CONTENT")


def test_bind_element_title(selenium):
    class BindElementTitle(VueComponent):
        title = Data("TITLE")
        template = "<div id='withtitle' v-bind:title='title'></div>"
    prepare(selenium, BindElementTitle)
    assert element_attribute_has_value(selenium, "withtitle", "title", "TITLE")


def test_if_condition(selenium):
    class IfCondition(VueComponent):
        show = Data(False)
        template = "<div>" \
                   "    <div id='notpresent' v-if='show'>DONT SHOW</div>" \
                   "    <div id='present' />" \
                   "</div>"
    prepare(selenium, IfCondition)
    assert element_present(selenium, "present")
    assert element_not_present(selenium, "notpresent")


def test_for_loop(selenium):
    class ForLoop(VueComponent):
        items = Data(["0", "1", "2"])
        template = "<ol id='list'>" \
                   "   <li v-for='item in items' :id='item'>{{ item }}</li>" \
                   "</ol>"
    prepare(selenium, ForLoop)
    for idx in range(3):
        assert element_has_text(selenium, str(idx), str(idx))


def test_on_click_method(selenium):
    class OnClickMethod(VueComponent):
        message = Data("message")
        template = "<button @click='reverse' id='btn'>{{ message }}</button>"
        @method
        def reverse(self, event):
            self.message = "".join(reversed(self.message))

    prepare(selenium, OnClickMethod)
    assert element_has_text(selenium, "btn", "message")
    selenium.find_element_by_id("btn").click()
    assert element_has_text(selenium, "btn", "egassem")


def test_v_model(selenium):
    class VModel(VueComponent):
        clicked = Data(False)
        template = "<div>" \
                   "    <p id='p'>{{ clicked }}</p>" \
                   "    <input type='checkbox' id='c' v-model='clicked'>" \
                   "</div>"
    prepare(selenium, VModel)
    assert element_has_text(selenium, "p", "false")
    selenium.find_element_by_id("c").click()
    assert element_has_text(selenium, "p", "true")


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
    prepare(selenium, components)
    assert element_has_text(selenium, "header", "HEADER")


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
    prepare(selenium, components_with_properties)
    assert element_has_text(selenium, "header", "TEXT")
    assert element_has_text(selenium, "sub", "SUB")
