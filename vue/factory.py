from .decorators.base import VueDecorator
from .decorators.prop import Prop
from .decorators.data import Data
from .decorators.lifecycle_hook import LifecycleHook
from .decorators.method import Method


class VueComponentFactory:
    @classmethod
    def dict(cls, component, base):
        return cls(component, base).create_init_dict()

    def __init__(self, component, base):
        self.component = component
        self.base = base

    def create_init_dict(self):
        init_dict = self._get_vue_object_map()
        _data = init_dict["data"]

        def get_initialized_data(this):
            initialized_data = {}
            for name, date in _data.items():
                initialized_data[name] = date(this) if callable(
                    date) else date
            return initialized_data

        init_dict.update(data=get_initialized_data)
        return init_dict

    def _property_mixin(self, prop_name):
        if prop_name not in dir(self.component):
            return {"required": True}
        else:
            return {"default": getattr(self.component, prop_name)}

    def _vue_objects(self):
        all_objects = set(dir(self.component))
        all_objects.update(
            getattr(self.component, "__annotations__", {}).keys()
        )
        own_objects = all_objects - set(dir(self.base)) - {'__annotations__'}
        for obj_name in own_objects:
            yield obj_name, getattr(self.component, obj_name, None)

    def _auto_decorate(self, obj_name, obj):
        if obj_name in LifecycleHook.mapping:
            obj = LifecycleHook(obj_name, obj)
        elif callable(obj):
            obj = Method(obj)
        elif obj_name in getattr(self.component, "__annotations__", {}):
            obj = Prop(
                obj_name,
                self.component.__annotations__[obj_name],
                self._property_mixin(obj_name)
            )
        elif not isinstance(obj, VueDecorator):
            obj = Data(obj_name, obj)
        return obj

    def _get_vue_object_map(self):
        object_map = {
            "data": {},
            "template": self.component.template,
        }
        for obj_name, obj in self._vue_objects():
            obj = self._auto_decorate(obj_name, obj)
            if isinstance(obj, VueDecorator):
                obj.update(object_map)
        return object_map
