import os

from cico import TravisCI, GitHub
from cico.results import Directory

TravisCI(
    repo=GitHub('stefanhoelzl', 'ci-results', os.environ.get("GH_TOKEN", "")),
    branch="vue.py",
    results=[
        Directory("tests/selenium/_html", rename="html"),
        Directory("tests/selenium/_screenshots", rename="examples"),
    ]
).commit()
