from browser import window
import javascript

from .wrapper import Vue, Object


def _inject_vue_instance(fn, first_arg_is_this=False):
    def fn_(*args, **kwargs):
        args = list(args)
        vue_instance = javascript.this() if not first_arg_is_this \
            else args.pop(0)
        return Object.to_js(fn(Vue(vue_instance), *args, **kwargs))
    return fn_


def _wrap_coroutine(coroutine):
    def wrapper(*args, **kwargs):
        import asyncio
        return asyncio.ensure_future(coroutine(*args, **kwargs))
    return wrapper


def _wrap_method(method):
    if hasattr(method, "__coroutinefunction__"):
        method = _wrap_coroutine(method)
    return _inject_vue_instance(method)


class Model:
    def __init__(self, prop="value", event="input"):
        self.prop = prop
        self.event = event

    def to_vue_object(self):
        return {
            "prop": self.prop,
            "event": self.event,
        }


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


class Validator:
    def __init__(self, prop, fn):
        self.prop = prop
        self.fn = fn


def validator(prop):
    def decorator(fn):
        return Validator(prop, fn)
    return decorator


def watch(name):
    def decorator(fn):
        fn = _inject_vue_instance(fn)
        fn.vue_watch = True
        fn.watch_name = name
        return fn
    return decorator


def filters(fn):
    fn.vue_filter = True
    return fn


class DataInitializer:
    def __init__(self, fn):
        self.fn = _inject_vue_instance(fn, first_arg_is_this=True)

    def eval(self, this):
        return self.fn(this)


def data(fn):
    return DataInitializer(fn)


class VueComponent:
    template = ""

    @classmethod
    def _vue_init_dict(cls):
        init_dict = cls._get_vue_object_map()
        init_dict.update(data=cls._get_init_data)
        return init_dict

    @classmethod
    def _vue_property(cls, name, typ, validator):
        type_map = {
            int: window.Number,
            float: window.Number,
            str: window.String,
            bool: window.Boolean,
            list: window.Array,
            object: window.Object,
            dict: window.Object,
            None: None
        }
        prop = {
            "type": type_map[typ],
        }
        if name not in dir(cls):
            prop.update(required=True)
        else:
            prop.update(default=getattr(cls, name))
        if validator is not None:
            prop.update(validator=validator)
        return prop

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
            "filters": {},
            "template": cls.template,
        }
        validators = {}
        for obj_name in set(dir(cls))-set(dir(VueComponent)):
            obj = getattr(cls, obj_name)
            if obj_name in lifecycle_hooks:
                hook = _inject_vue_instance(obj)
                object_map[lifecycle_hooks[obj_name]] = hook
            elif hasattr(obj, "vue_computed"):
                object_map["computed"][obj_name] = obj.to_vue_object()
            elif hasattr(obj, "vue_watch"):
                object_map["watch"][obj.watch_name] = obj
            elif hasattr(obj, "vue_filter"):
                object_map["filters"][obj_name] = obj
            elif callable(obj):
                object_map["methods"][obj_name] = _wrap_method(obj)
            elif obj_name in getattr(cls, "__annotations__", {}):
                pass
            elif isinstance(obj, Validator):
                validators[obj.prop] = _inject_vue_instance(obj.fn)
            elif isinstance(obj, Model):
                object_map["model"] = obj.to_vue_object()
            else:
                object_map["data"][obj_name] = obj
        for obj_name, typ in getattr(cls, "__annotations__", {}).items():
            object_map["props"][obj_name] = cls._vue_property(
                obj_name, typ, validators.get(obj_name, None)
            )
        return object_map

    @classmethod
    def _get_init_data(cls, this):
        data_ = cls._get_vue_object_map()["data"]
        for name, date in data_.items():
            if isinstance(date, DataInitializer):
                data_[name] = date.eval(this)
        return data_

    def __new__(cls, el, **data):
        init_dict = cls._vue_init_dict()
        init_dict.update(el=el)
        init_dict.update(propsData=data)
        return window.Vue.new(init_dict)

    @classmethod
    def register(cls, name=None):
        name = name if name else cls.__name__
        window.Vue.component(name, cls._vue_init_dict())
