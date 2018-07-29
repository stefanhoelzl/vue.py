from .decorators.base import VueDecorator
from .decorators.prop import Prop
from .decorators.data import Data
from .decorators.lifecycle_hook import LifecycleHook
from .decorators.method import Method
from .decorators.mixins import Mixins
from .decorators.template import Template
from .decorators.directive import DirectiveHook
from .decorators.extends import Extends


def merge_templates(base, sub):
    if getattr(sub, "template_merging", False):
        base_template = merge_templates(base.__bases__[0], base)
        base_slots = getattr(base, "template_slots", {})
        sub_slots = getattr(sub, "template_slots", {})
        templates = dict(tuple(base_slots.items())
                         + tuple(sub_slots.items()))
        return base_template.format(sub.template, **templates)
    return getattr(sub, "template", "{}")


class BrythonObjectWorkarounds(type):
    """
    Fixes the following Brython bugs:
    * https://github.com/brython-dev/brython/issues/905
    * https://github.com/brython-dev/brython/issues/904
    """
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bases = cls.__bases__
        cls.__bases__ = bases if bases else (object,)
        if not hasattr(cls, "__annotations__"):
            cls.__annotations__ = {}
        cls.__annotations__.update(getattr(cls.__base__,
                                           "__annotations__",
                                           {}))

    @property
    def __base__(cls):
        return cls.__bases__[0]


class Wrapper(metaclass=BrythonObjectWorkarounds):
    pass


class AttributeDictFactory:
    @classmethod
    def get_item(cls, wrapper):
        if isinstance(wrapper, dict):
            return wrapper
        return cls(wrapper).generate_item()

    @classmethod
    def get_wrapper_base(cls, wrapper):
        base = wrapper.__base__
        if base is Wrapper:
            return wrapper
        return cls.get_wrapper_base(base)

    def __init__(self, wrapper):
        self.wrapper = wrapper
        self.parent = self.wrapper.__base__
        self.base = self.get_wrapper_base(wrapper)

    def __attributes__(self):
        all_objects = set(dir(self.wrapper))
        all_objects.update(
            getattr(self.wrapper, "__annotations__", {}).keys()
        )
        own_objects = all_objects - set(dir(self.base)) - {'__annotations__'}
        for obj_name in own_objects:
            yield obj_name, getattr(self.wrapper, obj_name, None)

    def auto_decorate(self, obj_name, obj):
        return obj

    def generate_item(self):
        object_map = {}
        for obj_name, obj in self.__attributes__():
            obj = self.auto_decorate(obj_name, obj)
            if isinstance(obj, VueDecorator):
                obj.update(object_map)
        return object_map


class VueComponentFactory(AttributeDictFactory):
    def _property_mixin(self, prop_name):
        if prop_name not in dir(self.wrapper):
            return {"required": True}
        else:
            return {"default": getattr(self.wrapper, prop_name)}

    def auto_decorate(self, obj_name, obj):
        if obj_name in LifecycleHook.mapping:
            obj = LifecycleHook(obj_name, obj)
        elif obj_name == "template":
            obj = Template(merge_templates(self.parent, self.wrapper))
        elif obj_name == "extends":
            if obj:
                extends = self.parent if isinstance(obj, bool) else obj
                obj = Extends(VueComponentFactory.get_item(extends))
        elif obj_name == "mixins":
            obj = Mixins(*(VueComponentFactory.get_item(m) for m in obj))
        elif callable(obj):
            obj = Method(obj)
        elif obj_name in getattr(self.wrapper, "__annotations__", {}):
            obj = Prop(
                obj_name,
                self.wrapper.__annotations__[obj_name],
                self._property_mixin(obj_name)
            )
        elif not isinstance(obj, VueDecorator):
            obj = Data(obj_name, obj)
        return super().auto_decorate(obj_name, obj)

    def generate_item(self):
        init_dict = super().generate_item()
        _data = init_dict.get("data", None)

        if not _data:
            return init_dict

        def get_initialized_data(this):
            initialized_data = {}
            for name, date in _data.items():
                initialized_data[name] = date(this) if callable(
                    date) else date
            return initialized_data

        init_dict.update(data=get_initialized_data)
        return init_dict


class VueDirectiveFactory(AttributeDictFactory):
    def auto_decorate(self, obj_name, obj):
        if callable(obj):
            obj = DirectiveHook(obj, hooks=(obj_name,), name=self.wrapper.name)
        return super().auto_decorate(obj_name, obj)

    @classmethod
    def get_item(cls, wrapper):
        default = {wrapper.name: {}}
        dct = super().get_item(wrapper)
        return dct.get("directives", default).popitem()[1]
