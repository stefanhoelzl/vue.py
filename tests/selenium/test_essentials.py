import time
import inspect
from pathlib import Path

import pytest
from selenium.common.exceptions import *

URL = "http://localhost:8000/tests/selenium/html/{}.html"

Vue = object


def prepare(selenium, run, html):
    name = run.__name__
    code = inspect.getsource(run)
    code = "\n".join(l[4:] for l in code.split("\n"))
    code += "  {}()".format(name)
    template = Path("index.html").read_text()
    template = template.replace("CODE", code)
    template = template.replace("HTML", html)
    Path("html", "{}.html".format(name)).write_text(template)
    selenium.get(URL.format(name))
    time.sleep(0.1)


def test_declarative_rendering(selenium):
    def declarative_rendering():
        Vue("#app", message="MESSAGE CONTENT")
    prepare(selenium, declarative_rendering, "{{ message }}")
    element = selenium.find_element_by_id("app")
    assert "MESSAGE CONTENT" == element.text


def test_bind_element_title(selenium):
    def bind_element_title():
        Vue("#app", title="TITLE")
    prepare(selenium, bind_element_title,
            "<div id='withtitle' v-bind:title='title'></div>")
    element = selenium.find_element_by_id("withtitle")
    assert "TITLE" == element.get_attribute("title")


def test_if_condition(selenium):
    def if_condition():
        Vue("#app", show=False)
    prepare(selenium, if_condition,
            "<div id='element' v-if='show'></div>")
    with pytest.raises(NoSuchElementException):
        assert selenium.find_element_by_id("element")
