import re
from subprocess import run

import pyderman
import requests

LatestReleaseUrl = (
    "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{version}"
)

chrome_version_output = (
    run(["google-chrome", "--version"], capture_output=True)
    .stdout.decode("utf-8")
    .strip()
)

print(chrome_version_output)
chrome_major_version = re.search("Google Chrome (\d+)", chrome_version_output).group(1)
chromedriver_version = requests.get(
    LatestReleaseUrl.format(version=chrome_major_version)
).text.strip()
print(f"Chromedriver Version {chromedriver_version}")

pyderman.install(
    browser=pyderman.chrome,
    file_directory="tests/selenium",
    filename="chromedriver",
    overwrite=True,
    version=chromedriver_version,
)
