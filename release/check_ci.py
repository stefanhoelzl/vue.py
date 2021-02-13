import sys
import json
import urllib.request

ref = sys.argv[1]
url = f"https://api.github.com/repos/stefanhoelzl/vue.py/commits/{ref}/check-runs"

with urllib.request.urlopen(url) as response:
    checks = json.loads(response.read())

assert checks["total_count"] == 1
assert checks["check_runs"][0]["status"] == "completed"
assert checks["check_runs"][0]["conclusion"] == "success"
assert checks["check_runs"][0]["name"] == "Travis CI - Branch"
