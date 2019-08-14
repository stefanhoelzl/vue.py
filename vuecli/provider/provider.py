import pkg_resources
from pathlib import Path

import yaml
from jinja2 import Template

INDEX_CONTENT = pkg_resources.resource_string("vuecli", "index.html")
LOADING_CONTENT = pkg_resources.resource_string("vuecli", "loading.gif")
VUE_PATH = pkg_resources.resource_filename("vue", "")
JS_PATH = pkg_resources.resource_filename("vuecli", "js")


class Provider:
    Arguments = {}

    def __init__(self, path=None):
        self.path = Path(path if path else ".")

    def load_config(self):
        config_file = Path(self.path, "vuepy.yml")
        if config_file.exists():
            with open(config_file, "r") as fh:
                config = yaml.safe_load(fh.read())
            if config:
                return config
        return {}

    def content(self, endpoint, route, content):
        raise NotImplementedError()

    def directory(self, endpoint, route, path, deep=False):
        raise NotImplementedError()

    def render_index(self):
        config = self.load_config()

        default_scripts = {
            "brython": "_js/brython_dist.js",
            "vue": "_js/vue.js",
            "vuex": "_js/vuex.js",
            "vue-router": "_js/vue-router.js",
        }
        scripts = {"brython": True, "vue": True}
        custom_scripts = config.get("scripts", {})
        if isinstance(custom_scripts, list):
            custom_scripts = {k: k for k in custom_scripts}
        scripts.update(custom_scripts)
        scripts = {
            k: default_scripts[k] if v is True else v
            for k, v in scripts.items() if v
        }

        brython_args = config.get("brython_args", {})
        if brython_args:
            joined = ", ".join(f"{k}: {v}" for k, v in brython_args.items())
            brython_args = f"{{ {joined} }}"
        else:
            brython_args = ""

        return Template(INDEX_CONTENT.decode("utf-8")).render(
            entry_point=config.get("entry_point", "app.py"),
            stylesheets=config.get("stylesheets", []),
            scripts=scripts,
            templates={
                id_: Path(self.path, template).read_text("utf-8")
                for id_, template in config.get("templates", {}).items()
            },
            brython_args=brython_args
        )

    def setup(self):
        self.content("index", "/", self.render_index)
        self.content("loading", "/loading.gif", lambda: LOADING_CONTENT)
        self.directory("application", "/", Path(self.path), deep=True)
        self.directory("js", "/_js", JS_PATH)
        self.directory("vuepy", "/vue", VUE_PATH, deep=True)

    def deploy(self, **kwargs):
        raise NotImplementedError()
