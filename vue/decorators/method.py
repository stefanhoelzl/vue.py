from .base import pyjs_bridge, VueDecorator


class Method(VueDecorator):
    __key__ = "methods"

    def __init__(self, fn):
        if hasattr(fn, "__coroutinefunction__"):
            fn = coroutine(fn)
        self.__value__ = pyjs_bridge(fn, inject_vue_instance=True)
        self.__id__ = fn.__name__


def coroutine(_coroutine):
    def wrapper(*args, **kwargs):
        import asyncio
        return asyncio.ensure_future(_coroutine(*args, **kwargs))
    wrapper.__name__ = _coroutine.__name__
    return wrapper


def method(_method):
    if hasattr(_method, "__coroutinefunction__"):
        _method = coroutine(_method)
    return Method(_method)
