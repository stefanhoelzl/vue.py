import os
import semver
import vue

old_version = semver.VersionInfo.parse(vue.__version__)
mode = os.environ.get("MODE", "minor")

if mode == "major":
    new_version = old_version.bump_major()
elif mode == "minor":
    new_version = old_version.bump_minor()
elif mode == "patch":
    new_version = old_version.bump_patch()
else:
    raise RuntimeError("Unkown release mode")

print(new_version)
