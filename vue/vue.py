from browser import window
import javascript


def vue_function(fn):
    def fn_(*args, **kwargs):
        return fn(Vue(javascript.this()), *args, **kwargs)
    return fn_


def method(fn):
    fn = vue_function(fn)
    fn.vue_method = True
    return fn


def computed(fn):
    fn = vue_function(fn)
    fn.vue_computed = True
    return fn


class Vue:
    def __init__(self, this):
        self._vue = this

    def __getattr__(self, item):
        return getattr(self._vue, item)

    def __setattr__(self, key, value):
        if key not in ["_vue"]:
            setattr(self._vue, key, value)
        object.__setattr__(self, key, value)


class Data:
    def __init__(self, value):
        self.vue_data = True
        self.value = value


class VueComponent:
    @classmethod
    def _vue_init_dict(cls):
        return {
            "data": cls._get_init_data(),
            "methods": cls._get_vue_object("method")
        }

    @classmethod
    def _get_vue_object(cls, function_type):
        return {
            m: getattr(cls, m)
            for m in dir(cls)
            if hasattr(getattr(cls, m), "vue_" + function_type)
        }

    @classmethod
    def _get_init_data(cls):
        return {
            k: v.value for k, v in cls._get_vue_object("data").items()
        }

    def __new__(cls, el, **data):
        init_dict = cls._vue_init_dict()
        init_dict.update({
            "el": el,
        })
        return window.Vue.new(init_dict)
