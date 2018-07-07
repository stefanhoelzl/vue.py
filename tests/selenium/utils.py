import inspect
import re
from pathlib import Path

import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import *

URL = "http://localhost:8000/tests/selenium/_html/{}.html"
DEFAULT_TIMEOUT = 1


@pytest.fixture(scope="session")
def selenium_():
    Path("_html").mkdir(exist_ok=True)
    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    desired = DesiredCapabilities.CHROME
    desired['loggingPrefs'] = {"browser": "ALL"}

    driver = webdriver.Chrome("./chromedriver",
                              chrome_options=options,
                              desired_capabilities=desired)
    yield driver
    driver.close()


@pytest.fixture
def selenium(selenium_):
    logs = []
    def get_logs_and_save(only_new=True):
        new_logs = selenium_.get_log("browser")
        logs.extend(new_logs)
        return new_logs if only_new else logs
    selenium_.get_logs = get_logs_and_save
    yield selenium_
    analyze_logs(selenium_.get_logs(only_new=False))


def analyze_logs(logs):
    errors = []
    exceptions = [
        r"[^ ]+ 7692 Synchronous XMLHttpRequest on the main thread is deprecated because of its detrimental effects to the end user's experience. For more help, check https://xhr.spec.whatwg.org/.",
        r"[^ ]+ {}".format(re.escape("7706 Failed to load resource: the server responded with a status of 404 (File not found)")),
    ]
    for log in logs:
        if log['level'] != "INFO":
            for exception in exceptions:
                if re.match(exception, log["message"]):
                    break
            else:
                errors.append(log)
    if errors:
        raise Exception("\n".join(str(error) for error in errors))



def prepare(selenium, app):
    name = app.__name__
    code = inspect.getsource(app)
    code = "\n".join(l[4:] for l in code.split("\n"))
    code += "  app = {}('#app')".format(name)
    template = Path("index.html").read_text()
    template = template.replace("CODE", code)
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
