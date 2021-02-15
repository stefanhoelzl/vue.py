import re
import subprocess
from collections import defaultdict

ChangelogCategories = {
    "Features": "feature",
    "Bugfixes": "bugfix",
}


def git(*args):
    return subprocess.check_output(["git", *args]).decode("utf-8").strip()


last_release_hash = git("log", "--pretty='%H'", "--grep=\\[release\\]", "-1").strip("'")
commits_since_last_release = git(
    "log", "--pretty='%s'", f"{last_release_hash}..HEAD"
).split("\n")
if commits_since_last_release == [""]:
    raise RuntimeError(f"no commits since last release")

messages_by_category = defaultdict(list)
for commit in commits_since_last_release:
    match = re.match("^\[(?P<category>[a-z]+)\] (?P<message>.+)", commit.strip("'"))
    if match:
        messages_by_category[match.group("category")].append(match.group("message"))
    else:
        raise RuntimeError(f"Invalid commit: {commit}")

for pretty, category in ChangelogCategories.items():
    if category in messages_by_category:
        print(f"* {pretty}")
        for message in messages_by_category[category]:
            print(f"  * {message}")
