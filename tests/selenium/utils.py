import inspect
from pathlib import Path

import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

URL = "http://localhost:8000/tests/selenium/_html/{}.html"
DEFAULT_TIMEOUT = 1


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
