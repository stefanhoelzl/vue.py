import inspect
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

from vue import *

URL = "http://localhost:8000/tests/selenium/_html/{}.html"
DEFAULT_TIMEOUT = 1


def method(fn):
    return fn


@pytest.fixture(scope="session")
def selenium():
    Path("_html").mkdir(exist_ok=True)
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome("./chromedriver", chrome_options=options)
    yield driver
    driver.close()


def prepare(selenium, app, html=""):
    name = app.__name__
    code = inspect.getsource(app)
    code = "\n".join(l[4:] for l in code.split("\n"))
    code += "  app = {}('#app')".format(name)
    template = Path("index.html").read_text()
    template = template.replace("CODE", code)
    template = template.replace("HTML", html)
    Path("_html", "{}.html".format(name)).write_text(template)
    selenium.get(URL.format(name))


def element_has_text(driver, id_, text, timeout=DEFAULT_TIMEOUT):
    return WebDriverWait(driver, timeout).until(
        EC.text_to_be_present_in_element((By.ID, id_), text)
    )


def element_present(driver, id_, timeout=DEFAULT_TIMEOUT):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, id_))
    )


def element_not_present(driver, id_, timeout=DEFAULT_TIMEOUT):
    def check(driver_):
        try:
            driver_.find_element_by_id(id_)
        except NoSuchElementException:
            return True
        return False
    return WebDriverWait(driver, timeout).until(check)


def element_attribute_has_value(driver, id_, attribute, value,
                                timeout=DEFAULT_TIMEOUT):
    def check(driver_):
        element = driver_.find_element_by_id(id_)
        if element.get_attribute(attribute) == value:
            return element
        else:
            return False
    return WebDriverWait(driver, timeout).until(check)


def test_declarative_rendering(selenium):
    class DeclarativeRendering(VueComponent):
        message = Data("MESSAGE CONTENT")
    prepare(selenium, DeclarativeRendering, "{{ message }}")
    assert element_has_text(selenium, "app", "MESSAGE CONTENT")


def test_bind_element_title(selenium):
    class BindElementTitle(VueComponent):
        title = Data("TITLE")
    prepare(selenium, BindElementTitle,
            "<div id='withtitle' v-bind:title='title'></div>")
    assert element_attribute_has_value(selenium, "withtitle", "title", "TITLE")


def test_if_condition(selenium):
    class IfCondition(VueComponent):
        show = Data(False)
    prepare(selenium, IfCondition,
            "<div id='notpresent' v-if='show'>DONT SHOW</div>"
            "<div id='present' />")
    assert element_present(selenium, "present")
    assert element_not_present(selenium, "notpresent")


def test_for_loop(selenium):
    class ForLoop(VueComponent):
        items = Data(["0", "1", "2"])
    prepare(selenium, ForLoop,
            "<ol id='list'>"
            "   <li v-for='item in items' :id='item'>{{ item }}</li>"
            "</ol>")
    for idx in range(3):
        assert element_has_text(selenium, str(idx), str(idx))


def test_on_click_method(selenium):
    class OnClickMethod(VueComponent):
        message = Data("message")

        @method
        def reverse(self, event):
            self.message = "".join(reversed(self.message))

    prepare(selenium, OnClickMethod,
            "<button @click='reverse' id='btn'>{{ message }}</button>")
    assert element_has_text(selenium, "btn", "message")
    selenium.find_element_by_id("btn").click()
    assert element_has_text(selenium, "btn", "egassem")


def test_v_model(selenium):
    class VModel(VueComponent):
        clicked = Data(False)
    prepare(selenium, VModel,
            "<p id='p'>{{ clicked }}</p>"
            "<input type='checkbox' id='c' v-model='clicked'>")
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
            template = """
            <h1 id="header">{{ text }}</h1>
            """
        SubComponent.register()

        class App(VueComponent):
            template = """
            <sub-component text="TEXT"></sub-component>
            """
        return App(el)
    prepare(selenium, components_with_properties)
    assert element_has_text(selenium, "header", "TEXT")
