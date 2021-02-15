import sys
import json
import urllib.request

ref = sys.argv[1]
url = f"https://api.github.com/repos/stefanhoelzl/vue.py/commits/{ref}/check-runs"

with urllib.request.urlopen(url) as response:
    checks = json.loads(response.read())

assert checks["total_count"]
for check in checks["check_runs"]:
    assert check["status"] == "completed", f"{check['name']} still running"
    assert check["conclusion"] == "success", f"{check['name']} failed"
