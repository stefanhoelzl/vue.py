import json
import subprocess
import urllib.request
import time
from contextlib import contextmanager

import pytest

from tools.release import version


def _raise_failed_process(proc, error_msg):
    stdout = proc.stdout if isinstance(proc.stdout, bytes) else proc.stdout.read()
    stderr = proc.stderr if isinstance(proc.stderr, bytes) else proc.stderr.read()
    print(f"return-code: {proc.returncode}")
    print("stdout")
    print(stdout.decode("utf-8"))
    print("stderr")
    print(stderr.decode("utf-8"))
    raise RuntimeError(error_msg)


def shell(*args, env=None, cwd=None):
    proc = subprocess.run(args, env=env, cwd=cwd, capture_output=True)
    if proc.returncode:
        _raise_failed_process(proc, str(args))


@pytest.fixture
def wheel(scope="session"):
    shell("make", "build")
    return f"dist/vuepy-{version()}-py3-none-any.whl"


@pytest.fixture
def venv(tmp_path):
    path = tmp_path / "venv"
    shell("python", "-m", "venv", str(path))
    return path


@pytest.fixture
def install(wheel, venv):
    def _install(extra=None):
        extra = f"[{extra}]" if extra else ""
        shell(
            "pip",
            "install",
            f"{wheel}{extra}",
            env={"PATH": str(venv / "bin"), "PIP_USER": "no"},
        )

    return _install


@contextmanager
def background_task(*args, env=None, cwd=None):
    proc = subprocess.Popen(
        args, env=env, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    try:
        yield
    finally:
        if proc.poll() is not None:
            _raise_failed_process(proc, "background task finished early")
        proc.kill()
        proc.communicate()


def request(url, retries=0, retry_delay=0):
    for retry in range(1 + retries):
        try:
            with urllib.request.urlopen(url) as response:
                return response
        except urllib.request.URLError:
            if retry >= retries:
                raise
        time.sleep(retry_delay)


@pytest.fixture
def app(tmp_path):
    app_path = tmp_path / "app"
    app_path.mkdir()
    return app_path


@pytest.fixture
def config(app):
    def _config(values):
        app.joinpath("vuepy.yml").write_text(json.dumps(values, indent=2))

    return _config


def test_static(install, venv, tmp_path, app):
    destination = tmp_path / "destination"
    install()
    shell(
        "vue-cli",
        "deploy",
        "static",
        str(destination),
        env={"PATH": f"{venv / 'bin'}"},
        cwd=str(app),
    )
    assert (destination / "index.html").is_file()


def test_flask(install, venv, app):
    install(extra="flask")
    with background_task(
        "vue-cli", "deploy", "flask", env={"PATH": f"{venv / 'bin'}"}, cwd=str(app)
    ):
        assert (
            request("http://localhost:5000", retries=5, retry_delay=0.5).status == 200
        )


def test_flask_settings(install, config, venv, app):
    install(extra="flask")
    config({"provider": {"flask": {"PORT": 5001}}})
    with background_task(
        "vue-cli", "deploy", "flask", env={"PATH": f"{venv / 'bin'}"}, cwd=str(app)
    ):
        assert (
            request("http://localhost:5001", retries=5, retry_delay=0.5).status == 200
        )
