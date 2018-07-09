from browser import window
import javascript


def _inject_vue_instance(fn, first_arg_is_this=False):
    def fn_(*args, **kwargs):
        args = list(args)
        vue_instance = javascript.this() if not first_arg_is_this \
            else args.pop(0)
        return fn(Vue(vue_instance), *args, **kwargs)
    return fn_


def method(fn):
    fn = _inject_vue_instance(fn)
    fn.vue_method = True
    return fn


def computed(fn):
    fn = _inject_vue_instance(fn, first_arg_is_this=True)
    fn.vue_computed = True
    return fn


def watch(name):
    def decorator(fn):
        fn = _inject_vue_instance(fn)
        fn.vue_watch = True
        fn.watch_name = name
        return fn
    return decorator


class Vue:
    def __init__(self, this):
        self._this = this

    def __getattr__(self, item):
        return getattr(self._this, item)

    def __setattr__(self, key, value):
        if key not in ["_this"]:
            setattr(self._this, key, value)
        object.__setattr__(self, key, value)


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
            "computed": cls._get_vue_object_map("computed"),
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
