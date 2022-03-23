from pathlib import Path
from setuptools import setup

import requests
from tools import release


def make_version():
    version = release.version()
    Path("vue/__version__.py").write_text(f'__version__ = "{version}"\n')
    return version


def fetch_vue_cli_js_file(source: str, name: str) -> str:
    js_data_base = Path(__file__).parent / "vuecli" / "js"
    js_data_base.mkdir(exist_ok=True)

    dest_path = js_data_base / name
    resp = requests.get(source)
    assert resp.ok
    dest_path.write_bytes(resp.content)

    return f"js/{name}"


setup(
    name="vuepy",
    version=make_version(),
    description="Pythonic Vue",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    keywords="web reactive gui framework",
    url="https://stefanhoelzl.github.io/vue.py/",
    author="Stefan Hoelzl",
    author_email="stefan.hoelzl@posteo.de",
    license="MIT",
    packages=["vuecli", "vuecli.provider", "vue", "vue.bridge", "vue.decorators"],
    install_requires=["brython==3.8.9", "Jinja2>=2.10", "pyyaml>=5.1"],
    extras_require={"flask": ["Flask>=1.0"]},
    package_data={
        "vuecli": [
            "index.html",
            "loading.gif",
            fetch_vue_cli_js_file("https://unpkg.com/vue@2.6.14/dist/vue.js", "vue.js"),
            fetch_vue_cli_js_file(
                "https://raw.githubusercontent.com/vuejs/vue/dev/LICENSE", "LICENSE_VUE"
            ),
            fetch_vue_cli_js_file(
                "https://unpkg.com/vuex@3.6.2/dist/vuex.js", "vuex.js"
            ),
            fetch_vue_cli_js_file(
                "https://raw.githubusercontent.com/vuejs/vuex/master/LICENSE",
                "LICENSE_VUEX",
            ),
            fetch_vue_cli_js_file(
                "https://unpkg.com/vue-router@3.5.1/dist/vue-router.js", "vue-router.js"
            ),
            fetch_vue_cli_js_file(
                "https://raw.githubusercontent.com/vuejs/vue-router/dev/LICENSE",
                "LICENSE_VUE_ROUTER",
            ),
        ]
    },
    entry_points={
        "console_scripts": ["vue-cli=vuecli.cli:main"],
        "vuecli.provider": [
            "static=vuecli.provider.static:Static",
            "flask=vuecli.provider.flask:Flask",
        ],
    },
    zip_safe=False,
)
