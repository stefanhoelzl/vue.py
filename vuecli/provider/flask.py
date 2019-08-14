import os
from pathlib import Path

from flask import Flask as FlaskApp, send_file, abort

from .provider import Provider


class Flask(Provider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = FlaskApp(__name__)

    def content(self, endpoint, route, content):
        self.app.add_url_rule(route, endpoint, content)

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
