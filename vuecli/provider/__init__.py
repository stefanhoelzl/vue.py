from pkg_resources import iter_entry_points


def _load(ep):
    try:
        return ep.load()
    except ModuleNotFoundError:
        return None


RegisteredProvider = {
    entry_point.name: _load(entry_point)
    for entry_point in iter_entry_points("vuecli.provider")
}
