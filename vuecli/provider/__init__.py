import importlib

from .provider import Provider



def _import(cls, mod):
    try:
        return getattr(importlib.import_module(mod, __name__), cls)
    except ModuleNotFoundError:
        return None


ProviderMap = {
    "static": _import("Static", ".static"),
    "flask": _import("Flask", ".flask"),
}
