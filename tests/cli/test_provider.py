from xml.etree import ElementTree

import yaml
import pytest

from vuecli.provider.provider import Provider


@pytest.fixture
def render_index(tmp_path):
    def render(config=None):
        tmp_path.joinpath("vuepy.yml").write_text(yaml.dump(config or {}))
        provider = Provider(tmp_path)
        config = provider.load_config()
        return provider.render_index(config)
    return render


def parse_index(index):
    et = ElementTree.fromstring(index)
    return {
        "stylesheets": [e.attrib["href"] for e in et.findall("head/link")],
        "scripts": [e.attrib["src"] for e in et.findall("head/script")],
        "templates": {
            e.attrib["id"]: e.text.strip()
            for e in et.findall("body/script[@type='x-template']")
        },
        "brython": et.find("body").attrib["onload"]
    }


class TestRenderIndex:
    def test_defaults(self, render_index):
        index = render_index()
        assert parse_index(index) == {
            "stylesheets": [],
            "scripts": ["brython.js", "brython_stdlib.js", "vue.js"],
            "templates": {},
            "brython": "brython();"
        }

    def test_custom_stylesheets(self, render_index):
        index = render_index({"stylesheets": ["first.css", "second.css"]})
        assert parse_index(index)["stylesheets"] == ["first.css", "second.css"]

    @pytest.mark.parametrize("ext, js", [
        ("vuex", "vuex.js"), ("vue-router", "vue-router.js")
    ])
    def test_enable_builtin_script(self, render_index, ext, js):
        index = render_index({"scripts": {ext: True}})
        assert js in parse_index(index)["scripts"]

    @pytest.mark.parametrize("ext", ["vue", "brython", "vuex", "vue-router"])
    def test_customize_builtin_script(self, render_index, ext):
        index = render_index({"scripts": {ext: "custom"}})
        assert "custom" in parse_index(index)["scripts"]

    def test_custom_script(self, render_index):
        index = render_index({"scripts": ["myscript.js"]})
        assert "myscript.js" in parse_index(index)["scripts"]

    def test_custom_template(self, render_index, tmp_path):
        tmp_path.joinpath("my.html").write_text("content")
        index = render_index({"templates": {"my": "my.html"}})
        assert parse_index(index)["templates"] == {"my": "content"}

    def test_custom_brython_args(self, render_index):
        index = render_index({"brython_args": {"debug": 10}})
        assert parse_index(index)["brython"] == "brython({ debug: 10 });"
