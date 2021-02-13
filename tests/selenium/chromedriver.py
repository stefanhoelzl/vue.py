import re
from subprocess import run

import chromedriver_install as cdi

# https://chromedriver.chromium.org/downloads
Versions = {"88": "88.0.4324.96", "83": "83.0.4103.39"}

chrome_version = (
    run(["google-chrome", "--version"], capture_output=True)
    .stdout.decode("utf-8")
    .strip()
)
print(chrome_version)
major = re.search("Google Chrome (\d+)", chrome_version).group(1)

cdi.install(file_directory="tests/selenium", overwrite=True, version=Versions[major])
