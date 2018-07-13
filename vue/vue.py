from browser import window
import javascript

from .wrapper import JSObjectWrapper


def _inject_vue_instance(fn, first_arg_is_this=False):
    def fn_(*args, **kwargs):
        args = list(args)
        vue_instance = javascript.this() if not first_arg_is_this \
            else args.pop(0)
        return fn(JSObjectWrapper(vue_instance), *args, **kwargs)
    return fn_


def method(fn):
    fn = _inject_vue_instance(fn)
    fn.vue_method = True
    return fn


class Computed:
    def __init__(self, fn):
        self._getter = _inject_vue_instance(fn, first_arg_is_this=True)
        self._setter = None
        self.vue_computed = True

    def setter(self, fn):
        self._setter = _inject_vue_instance(fn)
        return self

    def to_vue_object(self):
        vue_object = {"get": self._getter}
        if self._setter:
            vue_object["set"] = self._setter
        return vue_object


def computed(fn):
    return Computed(fn)


def watch(name):
    def decorator(fn):
        fn = _inject_vue_instance(fn)
        fn.vue_watch = True
        fn.watch_name = name
        return fn
    return decorator


class Data:
    def __init__(self, value):
        self.vue_data = True
        self.value = value


class Property:
    def __init__(self):
        self.vue_property = True


class VueComponent:
    template = ""

    @classmethod
    def _vue_init_dict(cls):
        init_dict = {
            "data": cls._get_init_data,
            "props": [p for p in cls._get_vue_object_map("property")],
            "methods": cls._get_vue_object_map("method"),
            "computed": {
                n: cmp.to_vue_object()
                for n, cmp in cls._get_vue_object_map("computed").items()
            },
            "watch": {fn.watch_name: fn
                      for fn in cls._get_vue_object_map("watch").values()}
        }
        if cls.template:
            init_dict.update(template=cls.template)
        init_dict.update(cls._get_lifecycle_hooks())
        return init_dict

    @classmethod
    def _get_vue_object_map(cls, function_type):
        return {
            m: getattr(cls, m)
            for m in dir(cls)
            if hasattr(getattr(cls, m), "vue_" + function_type)
        }

    @classmethod
    def _get_init_data(cls, this=None):
        return {
            k: v.value for k, v in cls._get_vue_object_map("data").items()
        }

    @classmethod
    def _get_lifecycle_hooks(cls):
        lifecycle_hooks = {"beforeCreate": "before_create",
                           "created": "created",
                           "beforeMount": "before_mount",
                           "mounted": "mounted",
                           "beforeUpdate": "before_update",
                           "updated": "updated",
                           "beforeDestroy": "before_destroy",
                           "destroyed": "destroyed"}
        return {
            vue_hook: _inject_vue_instance(getattr(cls, py_hook))
            for vue_hook, py_hook in lifecycle_hooks.items()
            if hasattr(cls, py_hook)
        }

    def __new__(cls, el, **data):
        init_dict = cls._vue_init_dict()
        init_dict["data"] = init_dict["data"]()
        init_dict.update(el=el)
        init_dict.update(propsData=data)
        return window.Vue.new(init_dict)

    @classmethod
    def register(cls, name=None):
        name = name if name else cls.__name__
        window.Vue.component(name, cls._vue_init_dict())
