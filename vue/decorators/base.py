from vue.bridge import Object
import javascript


class VueDecorator:
    __key__ = None
    __parents__ = ()
    __id__ = None
    __value__ = None

    def update(self, vue_dict):
        base = vue_dict
        for parent in self.__parents__:
            base = vue_dict.setdefault(parent, {})

        if self.__id__ is None:
            base[self.__key__] = self.__value__
        else:
            base = base.setdefault(self.__key__, {})
            value = self.__value__
            if isinstance(base.get(self.__id__), dict):
                base[self.__id__].update(value)
            else:
                base[self.__id__] = value


def pyjs_bridge(fn, inject_vue_instance=False):
    def wrapper(*args, **kwargs):
        args = (javascript.this(), *args) if inject_vue_instance else args
        args = tuple(Object.from_js(arg) for arg in args)
        kwargs = {k: Object.from_js(v) for k, v in kwargs.items()}
        return Object.to_js(fn(*args, **kwargs))
    wrapper.__name__ = fn.__name__
    return wrapper
