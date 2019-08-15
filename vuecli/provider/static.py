import os
import sys
import shutil
import tempfile
import subprocess
from pathlib import Path

from .provider import Provider


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


class Static(Provider):
    Arguments = {
        "destination": "Path where the application should be deployed to",
        "--modules": {
            "help": "Create brython_stdlib.js"
                    " with all the modules used by the application",
            "action": "store_true",
        },
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tempdir = tempfile.TemporaryDirectory()

    @property
    def temppath(self):
        return self._tempdir.name

    def content(self, endpoint, route, content):
        path = self.temppath / Path(route).relative_to("/")
        if path.is_dir():
            path = path / "index.html"

        content = content()
        mode = "w+" if isinstance(content, str) else "wb+"
        with open(path, mode) as dest_file:
            dest_file.write(content)

    def directory(self, endpoint, route, path, deep=False):
        dest = self.temppath / Path(route).relative_to("/")
        copytree(Path(path), dest, deep=deep)

    def deploy(self, destination, modules=False):
        try:
            rel_depolypath = Path(destination).absolute().relative_to(
                Path(self.path).absolute()
            )
        except ValueError:
            pass
        else:
            shutil.rmtree(
                str(Path(self.temppath) / rel_depolypath),
                ignore_errors=True
            )
        if modules:
            self._make_modules()
        shutil.rmtree(destination, ignore_errors=True)
        shutil.copytree(self.temppath, Path(destination))
        self._tempdir.cleanup()

    def _make_modules(self):
        completed_process = subprocess.run(
            [sys.executable, "-m", "brython", "--modules"], cwd=self.temppath
        )
        if completed_process.returncode:
            raise RuntimeError(completed_process.returncode)
        shutil.move(
            str(Path(self.temppath, "brython_modules.js")),
            str(Path(self.temppath, "brython_stdlib.js"))
        )
