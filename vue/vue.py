from browser import window
import javascript

from .wrapper import Vue


def _inject_vue_instance(fn, first_arg_is_this=False):
    def fn_(*args, **kwargs):
        args = list(args)
        vue_instance = javascript.this() if not first_arg_is_this \
            else args.pop(0)
        return fn(Vue(vue_instance), *args, **kwargs)
    return fn_


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


class Property:
    TYPE_MAP = {
        int: window.Number,
        float: window.Number,
        str: window.String,
        bool: window.Boolean,
        list: window.Array,
        object: window.Object,
        dict: window.Object,
        None: None
    }

    def __init__(self, type=None):
        self.type = self.TYPE_MAP[type]
        self.vue_property = True

    def to_vue_object(self):
        return {
            "type": self.type,
        }


class VueComponent:
    template = ""

    @classmethod
    def _vue_init_dict(cls):
        init_dict = cls._get_vue_object_map()
        init_dict.update(data=cls._get_init_data)
        return init_dict

    @classmethod
    def _get_vue_object_map(cls):
        lifecycle_hooks = {"before_create": "beforeCreate",
                           "created": "created",
                           "before_mount": "beforeMount",
                           "mounted": "mounted",
                           "before_update": "beforeUpdate",
                           "updated": "updated",
                           "before_destroy": "beforeDestroy",
                           "destroyed": "destroyed"}
        object_map = {
            "methods": {},
            "props": {},
            "computed": {},
            "watch": {},
            "data": {},
            "template": cls.template,
        }
        for obj_name in set(dir(cls))-set(dir(VueComponent)):
            obj = getattr(cls, obj_name)
            if obj_name in lifecycle_hooks:
                hook = _inject_vue_instance(obj)
                object_map[lifecycle_hooks[obj_name]] = hook
            elif hasattr(obj, "vue_computed"):
                object_map["computed"][obj_name] = obj.to_vue_object()
            elif hasattr(obj, "vue_watch"):
                object_map["watch"][obj.watch_name] = obj
            elif callable(obj):
                method = _inject_vue_instance(obj)
                object_map["methods"][obj_name] = method
            elif isinstance(obj, Property):
                object_map["props"][obj_name] = obj.to_vue_object()
            else:
                object_map["data"][obj_name] = obj
        return object_map

    @classmethod
    def _get_init_data(cls, this=None):
        return cls._get_vue_object_map()["data"]

    def __new__(cls, el, **data):
        init_dict = cls._vue_init_dict()
        init_dict.update(el=el)
        init_dict.update(propsData=data)
        return window.Vue.new(init_dict)

    @classmethod
    def register(cls, name=None):
        name = name if name else cls.__name__
        window.Vue.component(name, cls._vue_init_dict())
