import re
import os
import json
import inspect
from pathlib import Path
from contextlib import contextmanager
from textwrap import dedent
from threading import Thread
from http.server import HTTPServer, SimpleHTTPRequestHandler
from http.client import HTTPConnection

import yaml
import pytest

from vuecli.provider.static import Static

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException

Address = "localhost"
Port = 8001
BaseUrl = f"http://{Address}:{Port}"

TEST_PATH = Path(__file__).parent
CHROME_DRIVER_PATH = TEST_PATH / "chromedriver"
HTML_OUTPUT_PATH = TEST_PATH / "_html"
APP_URL = BaseUrl + "/{}/{}/deploy"
EXAMPLE_URL = BaseUrl + "/examples_static/{}"
EXAMPLE_SCREENSHOT_PATH = "examples_static/{}/screenshot.png"
DEFAULT_TIMEOUT = 5


@pytest.fixture(scope="session")
def http_server():
    timeout = 10

    class RequestHandler(SimpleHTTPRequestHandler):
        protocol_version = "HTTP/1.0"

        def log_message(self, *args):
            pass

    with HTTPServer((Address, Port), RequestHandler) as httpd:
        thread = Thread(target=httpd.serve_forever, daemon=True)
        thread.start()

        c = HTTPConnection(Address, Port, timeout=timeout)
        c.request("GET", "/", "")
        assert c.getresponse().status == 200

        try:
            yield httpd
        finally:
            httpd.shutdown()
            thread.join(timeout=timeout)


@pytest.fixture(scope="session")
def selenium_session(http_server):
    with SeleniumSession() as session:
        yield session


@pytest.fixture()
def selenium(selenium_session, request):
    selenium_session.request = request
    yield selenium_session
    selenium_session.request = None


class ErrorLogException(Exception):
    def __init__(self, errors):
        formatted_errors = []
        for error in errors:
            formatted_error = {**error}
            formatted_error["message"] = formatted_error["message"].split("\\n")
            formatted_errors.append(formatted_error)
        super().__init__(json.dumps(formatted_errors, indent=2))
        self.errors = errors


class SeleniumSession:
    def __init__(self):
        self.driver = None
        self.request = None

        self.allowed_errors = []
        self.logs = []
        self._screenshot_file = None

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
        desired["goog:loggingPrefs"] = {"browser": "ALL"}

        self.driver = webdriver.Chrome(
            CHROME_DRIVER_PATH, options=options, desired_capabilities=desired
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()

    def get_logs(self):
        new_logs = self.driver.get_log("browser")
        self.logs.extend(new_logs)
        return new_logs

    def clear_logs(self):
        self.allowed_errors.clear()
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
    def app(self, app, config=None, files=None):
        test_name = self.request.function.__name__
        self._create_app_content(test_name, app, config or {}, files or {})
        url_base = str(self._app_output_path.relative_to(Path(".").absolute()))
        url = APP_URL.format(url_base, test_name)
        with self.url(url):
            yield

    @property
    def _app_output_path(self):
        sub_path = Path(self.request.node.nodeid.split("::", 1)[0])
        try:
            sub_path = sub_path.relative_to("selenium")
        except ValueError:
            pass  # WORKAROUND when running single tests from PyCharm
        output_path = HTML_OUTPUT_PATH / sub_path
        output_path.mkdir(exist_ok=True, parents=True)
        return output_path

    def _create_app_content(self, test_name, app, config, files):
        path = self._app_output_path / test_name
        path.mkdir(exist_ok=True, parents=True)

        code = "from vue import *\n\n\n"
        code += dedent("\n".join(inspect.getsource(app).split("\n")))
        code += """\n\napp = {}("#app")\n""".format(app.__name__)
        (path / "app.py").write_text(code)

        (path / "vuepy.yml").write_text(yaml.dump(config))

        for filename, content in files.items():
            (path / filename).write_text(content)

        provider = Static(path)
        provider.setup()
        provider.deploy(path / "deploy")

    @contextmanager
    def example(self, hash_=None):
        test_name = self.request.function.__name__
        name = test_name[5:]
        self._screenshot_file = Path(EXAMPLE_SCREENSHOT_PATH.format(name))
        url = EXAMPLE_URL.format(name)

        provider = Static("examples/{}".format(name))
        provider.setup()
        provider.deploy("examples_static/{}".format(name), package=True)

        if hash_:
            url = "{}#{}".format(url, hash_)
        with self.url(url):
            try:
                yield
            finally:
                self.screenshot()

    def screenshot(self):
        if self._screenshot_file:
            self.driver.save_screenshot(str(self._screenshot_file))
        self._screenshot_file = None

    def analyze_logs(self):
        errors = []
        exceptions = [
            r"[^ ]+ \d+"
            r" Synchronous XMLHttpRequest on the main thread is deprecated"
            r" because of its detrimental effects to the end user's experience."
            r" For more help, check https://xhr.spec.whatwg.org/.",
            r"[^ ]+ (\d+|-) {}".format(
                re.escape(
                    "Failed to load resource:"
                    " the server responded with a status of 404 (File not found)"
                )
            ),
        ]
        self.get_logs()
        for log in self.logs:
            if log["level"] != "INFO":
                for exception in exceptions + self.allowed_errors:
                    if re.match(exception, log["message"]):
                        break
                else:
                    if log["source"] not in ["deprecation"]:
                        errors.append(log)
        if errors:
            raise ErrorLogException(errors)

    def element_has_text(self, id_, text, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            ec.text_to_be_present_in_element((By.ID, id_), text)
        )

    def element_with_tag_name_has_text(self, tag_name, text, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            ec.text_to_be_present_in_element((By.TAG_NAME, tag_name), text)
        )

    def element_present(self, id_, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            ec.presence_of_element_located((By.ID, id_))
        )

    def element_with_tag_name_present(self, tag, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            ec.presence_of_element_located((By.TAG_NAME, tag))
        )

    def element_not_present(self, id_, timeout=DEFAULT_TIMEOUT):
        def check(driver_):
            try:
                driver_.find_element_by_id(id_)
            except NoSuchElementException:
                return True
            return False

        return WebDriverWait(self.driver, timeout).until(check)

    def element_attribute_has_value(
        self, id_, attribute, value, timeout=DEFAULT_TIMEOUT
    ):
        def check(driver_):
            element = driver_.find_element_by_id(id_)
            if element.get_attribute(attribute) == value:
                return element
            else:
                return False

        return WebDriverWait(self.driver, timeout).until(check)
