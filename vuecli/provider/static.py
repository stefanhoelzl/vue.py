import os
import shutil
import tempfile
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
