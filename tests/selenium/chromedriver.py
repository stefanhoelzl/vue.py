import re
from subprocess import run

import pyderman

# https://chromedriver.chromium.org/downloads
Versions = {
    "88": "88.0.4324.96",
    "83": "83.0.4103.39",
    "96": "96.0.4664.45",
    "98": "98.0.4758.102",
}

chrome_version = (
    run(["google-chrome", "--version"], capture_output=True)
    .stdout.decode("utf-8")
    .strip()
)
print(chrome_version)
major = re.search("Google Chrome (\d+)", chrome_version).group(1)

pyderman.install(
    browser=pyderman.chrome,
    file_directory="tests/selenium",
    filename="chromedriver",
    overwrite=True,
    version=Versions[major],
)
