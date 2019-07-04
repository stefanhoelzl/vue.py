import pkg_resources
from pathlib import Path

import yaml
from jinja2 import Template

INDEX_CONTENT = pkg_resources.resource_string("vuecli", "index.html")
LOADING_CONTENT = pkg_resources.resource_string("vuecli", "loading.gif")
VUE_PATH = pkg_resources.resource_filename("vue", None)
JS_PATH = pkg_resources.resource_filename("vuecli", "js")


class Provider:
    Arguments = {}

    def __init__(self, path=None):
        self.path = Path(path if path else ".")
        self.config = {}
        self._load_config()

    def _load_config(self):
        config_file = Path(self.path, "vuepy.yml")
        if config_file.exists():
            with open(config_file, "r") as fh:
                config = yaml.safe_load(fh.read())
            if config:
                self.config = config

    def content(self, endpoint, route, content):
        raise NotImplementedError()

    def directory(self, endpoint, route, path, deep=False):
        raise NotImplementedError()

    def render_template(self, template):
        templates = self.config.get("templates", {})
        return Template(template).render(
            stylesheets=self.config.get("stylesheets", []),
            scripts=self.config.get("scripts", []),
            templates={id_: Path(self.path, template).read_text("utf-8")
                       for id_, template in templates.items()},
            debug_level=self.config.get("debug-level", 0)
        )

    def setup(self):
        self.content("index", "/",
                     self.render_template(INDEX_CONTENT.decode("utf-8")))
        self.content("loading", "/loading.gif", LOADING_CONTENT)
        self.directory("application", "/", Path(self.path), deep=True)
        self.directory("js", "/_js", JS_PATH)
        self.directory("vuepy", "/vue", VUE_PATH, deep=True)

    def deploy(self, **kwargs):
        raise NotImplementedError()
