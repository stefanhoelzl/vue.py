import pkg_resources as _pkgres


def _load(ep):
    try:
        return ep.load()
    except ModuleNotFoundError:
        return None


RegisteredProvider = {
    entry_point.name: _load(entry_point)
    for entry_point in _pkgres.iter_entry_points("vuecli.provider")
}
