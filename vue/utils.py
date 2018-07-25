from browser import window, load

CACHE = {}


def js_load(path):
    if path in CACHE:
        return CACHE[path]
    before = dir(window)
    load(path)
    after = dir(window)
    diff = set(after) - set(before)
    mods = {module: getattr(window, module)
            for module in diff
            if "$" not in module}
    if len(mods) == 0:
        mods = None
    elif len(mods) == 1:
        mods = mods.popitem()[1]
    CACHE[path] = mods
    return mods


def js_lib(name):
    attr = getattr(window, name)
    if dir(attr) == ["default"]:
        return attr.default
    return attr
