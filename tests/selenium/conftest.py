import re
import os
import inspect
from pathlib import Path
from contextlib import contextmanager

import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import *


TEST_PATH = Path(__file__).parent
CHROME_DRIVER_PATH = TEST_PATH / "chromedriver"
HTML_OUTPUT_PATH = TEST_PATH / "_html"
TEMPLATE_PATH = TEST_PATH / "template.html"
APP_URL = "http://localhost:8000/{}/{}.html"
EXAMPLE_URL = "http://localhost:8000/examples/{}"
EXAMPLE_SCREENSHOT_PATH = TEST_PATH / "_screenshots"
DEFAULT_TIMEOUT = 5


@pytest.fixture(scope="session")
def selenium_session():
    with SeleniumSession() as selenium_session_:
        yield selenium_session_


@pytest.fixture()
def selenium(selenium_session, request):
    selenium_session.request = request
    yield selenium_session
    selenium_session.request = None


class ErrorLogException(Exception):
    def __init__(self, errors):
        super().__init__("\n".join(str(error) for error in errors))
        self.errors = errors


class SeleniumSession:
    def __init__(self):
        self.driver = None
        self.request = None

        self.logs = []

    def __getattr__(self, item):
        return getattr(self.driver, item)

    def __enter__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        if os.environ.get("CI"):
            options.add_argument("disable-gpu")
            options.add_argument("disable-dev-shm-usage")
            options.add_argument("no-sandbox")

        desired = DesiredCapabilities.CHROME
        desired['loggingPrefs'] = {"browser": "ALL"}

        self.driver = webdriver.Chrome(CHROME_DRIVER_PATH,
                                       chrome_options=options,
                                       desired_capabilities=desired)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()

    def get_logs(self):
        new_logs = self.driver.get_log("browser")
        self.logs.extend(new_logs)
        return new_logs

    def clear_logs(self):
        self.get_logs()
        self.logs.clear()

    @contextmanager
    def url(self, url):
        self.clear_logs()
        self.driver.get(url)
        try:
            yield
        finally:
            self.analyze_logs()

    @contextmanager
    def app(self, app):
        test_name = self.request.function.__name__
        self._create_app_html(test_name, app)
        url_base = str(self._app_output_path.relative_to(Path(".").absolute()))
        url = APP_URL.format(url_base, test_name)
        with self.url(url):
            yield

    @property
    def _app_output_path(self):
        sub_path = Path(self.request.node.nodeid.split("::", 1)[0])
        output_path = HTML_OUTPUT_PATH / sub_path.relative_to("selenium")
        output_path.mkdir(exist_ok=True, parents=True)
        return output_path

    def _create_app_html(self, file_name, app):
        code = inspect.getsource(app)
        code = "\n".join(l[4:] for l in code.split("\n"))
        code += "  app = {}('#app')".format(app.__name__)
        template = Path(TEMPLATE_PATH).read_text()
        template = template.replace("CODE", code)
        Path(self._app_output_path, "{}.html".format(file_name))\
            .write_text(template)

    @contextmanager
    def example(self):
        test_name = self.request.function.__name__
        name = test_name[5:]
        EXAMPLE_SCREENSHOT_PATH.mkdir(exist_ok=True)
        img_file = EXAMPLE_SCREENSHOT_PATH / "{}.png".format(name)
        with self.url(EXAMPLE_URL.format(name)):
            yield
            self.driver.save_screenshot(str(img_file))

    def analyze_logs(self):
        errors = []
        exceptions = [
            r"[^ ]+ 7692 Synchronous XMLHttpRequest on the main thread is deprecated because of its detrimental effects to the end user's experience. For more help, check https://xhr.spec.whatwg.org/.",
            r"[^ ]+ {}".format(re.escape(
                "7706 Failed to load resource: the server responded with a status of 404 (File not found)")),
        ]
        self.get_logs()
        for log in self.logs:
            if log['level'] != "INFO":
                for exception in exceptions:
                    if re.match(exception, log["message"]):
                        break
                else:
                    errors.append(log)
        if errors:
            raise ErrorLogException(errors)

    def element_has_text(self, id_, text, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            ec.text_to_be_present_in_element((By.ID, id_), text)
        )

    def element_present(self, id_, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            ec.presence_of_element_located((By.ID, id_))
        )

    def element_not_present(self, id_, timeout=DEFAULT_TIMEOUT):
        def check(driver_):
            try:
                driver_.find_element_by_id(id_)
            except NoSuchElementException:
                return True
            return False

        return WebDriverWait(self.driver, timeout).until(check)

    def element_attribute_has_value(self, id_, attribute, value,
                                    timeout=DEFAULT_TIMEOUT):
        def check(driver_):
            element = driver_.find_element_by_id(id_)
            if element.get_attribute(attribute) == value:
                return element
            else:
                return False

        return WebDriverWait(self.driver, timeout).until(check)
