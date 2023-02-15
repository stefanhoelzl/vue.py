from vue.bridge import Object
import javascript


class VueDecorator:
    __key__ = None
    __value__ = None


def pyjs_bridge(fn, inject_vue_instance=False):
    def wrapper(*args, **kwargs):
        args = (javascript.this(), *args) if inject_vue_instance else args
        args = tuple(Object.from_js(arg) for arg in args)
        kwargs = {k: Object.from_js(v) for k, v in kwargs.items()}
        return Object.to_js(fn(*args, **kwargs))

    wrapper.__name__ = fn.__name__
    return wrapper
