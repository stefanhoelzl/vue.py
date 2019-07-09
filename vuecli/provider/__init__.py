from pkg_resources import iter_entry_points


from .provider import Provider


def _load(ep):
    try:
        return ep.load()
    except ModuleNotFoundError:
        return None


ProviderMap = {
    entry_point.name: _load(entry_point)
    for entry_point in iter_entry_points("vuecli.provider")
}
