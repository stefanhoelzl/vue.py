import os
import shutil
import tempfile
import pkg_resources
from pathlib import Path

import yaml
from jinja2 import Template
from flask import Flask as FlaskApp, send_file, abort

INDEX_CONTENT = pkg_resources.resource_string("vuecli", "index.html")
LOADING_CONTENT = pkg_resources.resource_string("vuecli", "loading.gif")
VUE_PATH = pkg_resources.resource_filename("vue", None)
JS_PATH = pkg_resources.resource_filename("vuecli", "js")


def copytree(src, dst, deep=True):
    if not dst.exists():
        dst.mkdir()

    for item in os.listdir(src):
        s = Path(src, item)
        d = Path(dst, item)
        if s.is_dir() and deep:
            d.mkdir()
            copytree(s, d)
        elif s.is_file():
            shutil.copy2(str(s), str(d))


class Provider:
    def __init__(self, path=None):
        self.path = Path(path if path else ".")
        self.config = {}
        self._load_config()

    def _load_config(self):
        config_file = Path(self.path, "vuepy.yml")
        if config_file.exists():
            with open(config_file, "r") as fh:
                self.config = yaml.load(fh.read())

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


class Flask(Provider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = FlaskApp(__name__)

    def content(self, endpoint, route, content):
        self.app.add_url_rule(route, endpoint, lambda: content)

    def directory(self, endpoint, route, path, deep=False):
        def view_func(filename):
            full_path = Path(path, filename)
            if not full_path.exists():
                abort(404)
            return send_file(str(full_path.absolute()))
        flask_route = os.path.join(
            route, "<{}filename>".format("path:" if deep else ""))
        self.app.add_url_rule(flask_route, endpoint, view_func)

    def deploy(self):
        self.app.run()


class Static(Provider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.temppath = Path(tempfile.mkdtemp())

    def content(self, endpoint, route, content):
        path = self.temppath / Path(route).relative_to("/")
        if path.is_dir():
            path = path / "index.html"

        mode = "w+" if isinstance(content, str) else "wb+"
        with open(path, mode) as dest_file:
            dest_file.write(content)

    def directory(self, endpoint, route, path, deep=False):
        dest = self.temppath / Path(route).relative_to("/")
        copytree(Path(path), dest, deep=deep)

    def deploy(self, destination):
        shutil.rmtree(destination, ignore_errors=True)
        shutil.copytree(self.temppath, Path(destination))
