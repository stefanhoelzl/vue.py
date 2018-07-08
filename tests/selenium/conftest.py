import inspect
import re
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

HTTP_HTML_BASE = HTML_OUTPUT_PATH.relative_to(Path(".").absolute())
URL = "http://localhost:8000/{}/{{}}.html".format(HTTP_HTML_BASE)
DEFAULT_TIMEOUT = 1


@pytest.fixture(scope="session")
def selenium_session():
    with SeleniumSession() as selenium_session_:
        yield selenium_session_


@pytest.fixture()
def selenium(selenium_session, request):
    selenium_session.request = request
    yield selenium_session
    selenium_session.request = None


class SeleniumSession:
    def __init__(self):
        self.driver = None
        self.request = None

        self.logs = []
        self.output_path = Path(HTML_OUTPUT_PATH)
        self.output_path.mkdir(exist_ok=True)

    def __getattr__(self, item):
        return getattr(self.driver, item)

    def __enter__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")

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

    @contextmanager
    def app(self, app):
        test_name = self.request.function.__name__
        self._setup_html_with_app(test_name, app)
        self.driver.get(URL.format(test_name))
        yield
        self.analyze_logs()
        self.logs.clear()

    def _setup_html_with_app(self, file_name, app):
        code = inspect.getsource(app)
        code = "\n".join(l[4:] for l in code.split("\n"))
        code += "  app = {}('#app')".format(app.__name__)
        template = Path(TEMPLATE_PATH).read_text()
        template = template.replace("CODE", code)
        Path(self.output_path, "{}.html".format(file_name))\
            .write_text(template)

    def analyze_logs(self):
        errors = []
        exceptions = [
            r"[^ ]+ 7692 Synchronous XMLHttpRequest on the main thread is deprecated because of its detrimental effects to the end user's experience. For more help, check https://xhr.spec.whatwg.org/.",
            r"[^ ]+ {}".format(re.escape(
                "7706 Failed to load resource: the server responded with a status of 404 (File not found)")),
        ]
        for log in self.logs:
            if log['level'] != "INFO":
                for exception in exceptions:
                    if re.match(exception, log["message"]):
                        break
                else:
                    errors.append(log)
        if errors:
            raise Exception("\n".join(str(error) for error in errors))

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
