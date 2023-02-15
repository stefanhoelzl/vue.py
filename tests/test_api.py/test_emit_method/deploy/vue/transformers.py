"""
Transformers are used to create dictionaries to initialize Vue-Objects from Python classes.

e.g.
```python
class Component(VueComponent):
    prop: str

    def method(self):
        ...

    @computed
    def computed_value(self):
        ...
```

will be transformed into

```javascript
{
    props: {
        prop: {
            type: window.String,
        }
    },
    method: // wrapper calling Component.method,
    computed: {
        computed_value: {
            get: // wrapper calling Component.computed_value
        }
    }
}
```
"""

from .decorators.base import VueDecorator
from .decorators.prop import Prop
from .decorators.data import Data
from .decorators.computed import Computed
from .decorators.lifecycle_hook import LifecycleHook
from .decorators.method import Method
from .decorators.render import Render
from .decorators.mixins import Mixins
from .decorators.template import Template
from .decorators.directive import DirectiveHook
from .decorators.extends import Extends
from .decorators.components import Components
from .decorators.state import State
from .decorators.plugin import Plugin
from .decorators.routes import Routes


def _merge_templates(sub):
    def get_template_slots(cls):
        template_slots = getattr(cls, "template_slots", {})
        if isinstance(template_slots, str):
            template_slots = {"default": template_slots}
        return template_slots

    base = sub.__bases__[0]
    template_merging = hasattr(base, "template") and getattr(
        sub, "template_slots", False
    )
    if template_merging:
        base_template = _merge_templates(base)
        base_slots = get_template_slots(base)
        sub_slots = get_template_slots(sub)
        slots = dict(tuple(base_slots.items()) + tuple(sub_slots.items()))
        default = slots.get("default")
        return base_template.format(default, **slots)
    return getattr(sub, "template", "{}")


class _TransformableType(type):
    pass


class Transformable(metaclass=_TransformableType):
    pass


class ClassAttributeDictTransformer:
    """
    Takes all attributes of a class and creates a dictionary out of it.

    For each attribute a decorator is retrieved.
    The decorator is given by the `decorate` method wich should be overriden by sub-classes.
    The decorator has a `__key__` attribute to determine where in the resulting dictionary
    the value given by the `__value__` attribute should be stored.

    The resulting dictionaries can be used to be passed to Vue as initializers.
    """

    @classmethod
    def transform(cls, transformable):
        if not isinstance(transformable, _TransformableType):
            return transformable

        result = {}
        for attribute_name, attribute_value in cls._iter_attributes(transformable):
            decorator = cls.decorate(transformable, attribute_name, attribute_value)
            if decorator is not None:
                cls._inject_into(result, decorator.__key__, decorator.__value__)
        return result

    @classmethod
    def decorate(cls, transformable, attribute_name, attribute_value):
        if isinstance(attribute_value, VueDecorator):
            return attribute_value
        return None

    @classmethod
    def _iter_attributes(cls, transformable):
        all_objects = set(dir(transformable))
        all_objects.update(getattr(transformable, "__annotations__", {}).keys())
        own_objects = (
            all_objects - set(dir(cls._get_base(transformable))) - {"__annotations__"}
        )
        for attribute_name in own_objects:
            yield attribute_name, getattr(transformable, attribute_name, None)

    @classmethod
    def _get_base(cls, transformable):
        base = transformable.__bases__[0]
        if base is Transformable:
            return transformable
        return cls._get_base(base)

    @classmethod
    def _inject_into(cls, destination, key, value):
        keys = key.split(".")
        value_key = keys.pop()

        for key in keys:
            destination = destination.setdefault(key, {})

        if isinstance(destination.get(value_key), dict):
            destination[value_key].update(value)
        else:
            destination[value_key] = value


class VueComponentTransformer(ClassAttributeDictTransformer):
    """
    Takes a VueComponent-class and transforms it into a dictionary
    which can be passed to e.g. window.Vue.new or window.Vue.component
    """

    @classmethod
    def transform(cls, transformable):
        init_dict = super().transform(transformable)
        _data = init_dict.get("data", None)

        if not _data:
            return init_dict

        def get_initialized_data(this):
            initialized_data = {}
            for name, date in _data.items():
                initialized_data[name] = date(this) if callable(date) else date
            return initialized_data

        init_dict.update(data=get_initialized_data)
        return init_dict

    @classmethod
    def decorate(cls, transformable, attribute_name, attribute_value):
        decorated = super().decorate(transformable, attribute_name, attribute_value)
        if decorated is not None:
            return decorated

        if attribute_name in LifecycleHook.mapping:
            return LifecycleHook(attribute_name, attribute_value)
        if attribute_name == "template":
            return Template(_merge_templates(transformable))
        if attribute_name == "extends" and attribute_value:
            if not attribute_value:
                return None
            extends = (
                transformable.__bases__[0]
                if isinstance(attribute_value, bool)
                else attribute_value
            )
            return Extends(VueComponentTransformer.transform(extends))
        if attribute_name == "mixins":
            return Mixins(
                *(VueComponentTransformer.transform(m) for m in attribute_value)
            )
        if attribute_name == "components":
            return Components(
                *(VueComponentTransformer.transform(m) for m in attribute_value)
            )
        if attribute_name == "render":
            return Render(attribute_value)
        if callable(attribute_value):
            return Method(attribute_value)
        if attribute_name in getattr(transformable, "__annotations__", {}):
            mixin = {"required": True}
            if attribute_name in dir(transformable):
                mixin = {"default": getattr(transformable, attribute_name)}

            return Prop(
                attribute_name,
                transformable.__annotations__[attribute_name],
                mixin,
            )
        return Data(attribute_name, attribute_value)


class VueDirectiveTransformer(ClassAttributeDictTransformer):
    """
    Takes a VueDirective-class and transforms it into a dictionary
    which can be passed to window.Vue.directive
    """

    @classmethod
    def transform(cls, transformable):
        default = {transformable.name: {}}
        dct = super().transform(transformable)
        return dct.get("directives", default).popitem()[1]

    @classmethod
    def decorate(cls, transformable, attribute_name, attribute_value):
        if callable(attribute_value):
            attribute_value = DirectiveHook(
                attribute_value, hooks=(attribute_name,), name=transformable.name
            )
        return super().decorate(transformable, attribute_name, attribute_value)


class VueStoreTransformer(ClassAttributeDictTransformer):
    """
    Takes a VueStore-class and transforms it into a dictionary
    which can be passed to window.Vuex.Store.new
    """

    @classmethod
    def decorate(cls, transformable, attribute_name, attribute_value):
        if attribute_name == "plugins":
            return Plugin(attribute_value)
        decorated = super().decorate(transformable, attribute_name, attribute_value)
        if decorated is None:
            return State(attribute_name, attribute_value)
        return decorated


class VueRouterTransformer(ClassAttributeDictTransformer):
    """
    Takes a VueStore-class and transforms it into a dictionary
    which can be passed to window.VueRouter
    """

    @classmethod
    def decorate(cls, transformable, attribute_name, attribute_value):
        if attribute_name == "routes":
            return Routes(attribute_value)
        return super().decorate(transformable, attribute_name, attribute_value)
