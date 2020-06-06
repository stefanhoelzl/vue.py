from pkg_resources import resource_filename, resource_string
from functools import partial
from pathlib import Path

import yaml
from jinja2 import Template


VuePath = resource_filename("vue", "")
IndexTemplate = resource_string("vuecli", "index.html")
StaticContents = {
    "/loading.gif": resource_string("vuecli", "loading.gif"),

    "/vuepy.js": b"\n".join([
        resource_string("brython", "data/brython.js"),
        resource_string("brython", "data/brython_stdlib.js"),
    ]),

    "/vue.js": resource_string("vuecli", "js/vue.js"),
    "/vuex.js": resource_string("vuecli", "js/vuex.js"),
    "/vue-router.js": resource_string("vuecli", "js/vue-router.js"),
}


class Provider:
    Arguments = {}

    def __init__(self, path=None):
        self.path = Path(path if path else ".")

    @staticmethod
    def _normalize_config(config):
        default_scripts = {
            "vuepy": "vuepy.js",
            "vue": "vue.js",
            "vuex": "vuex.js",
            "vue-router": "vue-router.js",
        }
        scripts = {"vuepy": True, "vue": True}
        custom_scripts = config.get("scripts", {})
        if isinstance(custom_scripts, list):
            custom_scripts = {k: k for k in custom_scripts}
        scripts.update(custom_scripts)
        config["scripts"] = {
            k: default_scripts[k] if v is True else v
            for k, v in scripts.items() if v
        }

    def load_config(self):
        config_file = Path(self.path, "vuepy.yml")
        config = {}
        if config_file.exists():
            with open(config_file, "r") as fh:
                config = yaml.safe_load(fh.read())
        self._normalize_config(config)
        return config

    def content(self, endpoint, route, content):
        raise NotImplementedError()

    def directory(self, endpoint, route, path, deep=False):
        raise NotImplementedError()

    def render_index(self, config):
        brython_args = config.get("brython_args", {})
        if brython_args:
            joined = ", ".join(f"{k}: {v}" for k, v in brython_args.items())
            brython_args = f"{{ {joined} }}"
        else:
            brython_args = ""

        return Template(IndexTemplate.decode("utf-8")).render(
            stylesheets=config.get("stylesheets", []),
            scripts=config.get("scripts", {}),
            templates={
                id_: Path(self.path, template).read_text("utf-8")
                for id_, template in config.get("templates", {}).items()
            },
            brython_args=brython_args
        )

    def setup(self):
        config = config = self.load_config()
        self.directory("application", "/", Path(self.path), deep=True)
        self.directory("vuepy", "/vue", VuePath, deep=True)

        entry_point = config.get("entry_point", "app")
        self.content(
            "entry_point", "/__entry_point__.py",
            lambda: f"import {entry_point}"
        )
        self.content("index", "/", lambda: self.render_index(config))
        for route in StaticContents:
            self.content(route, route, partial(StaticContents.get, route))

    def deploy(self, **kwargs):
        raise NotImplementedError()
