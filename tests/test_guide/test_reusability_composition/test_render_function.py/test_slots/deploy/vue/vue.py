from browser import window
from .transformers import (
    VueComponentTransformer,
    Transformable,
    VueDirectiveTransformer,
)
from .bridge import Object
from .decorators.directive import DirectiveHook
from .decorators.filters import Filter


class Vue:
    @staticmethod
    def directive(name, directive=None):
        if directive is None and isinstance(name, str):
            return window.Vue.directive(name)

        if directive is None:
            directive = name
            name = directive.__name__.lower()

        if not isinstance(directive, type):

            class FunctionDirective(VueDirective):
                d = DirectiveHook(directive)

            directive = FunctionDirective

        window.Vue.directive(name, VueDirectiveTransformer.transform(directive))

    @staticmethod
    def filter(method_or_name, method=None):
        if not method:
            method = method_or_name
            name = method_or_name.__name__
        else:
            method = method
            name = method_or_name
        flt = Filter(method, name)
        window.Vue.filter(flt.name, flt.__value__)

    @staticmethod
    def mixin(mixin):
        window.Vue.mixin(VueComponentTransformer.transform(mixin))

    @staticmethod
    def use(plugin, *args, **kwargs):
        window.Vue.use(plugin, *args, kwargs)

    @staticmethod
    def component(component_or_name, component=None):
        if isinstance(component_or_name, str) and component is None:
            return window.Vue.component(component_or_name)
        if component is not None:
            name = component_or_name
        else:
            component = component_or_name
            name = component.__name__
        window.Vue.component(name, VueComponentTransformer.transform(component))


class VueComponent(Transformable):
    @classmethod
    def init_dict(cls):
        return VueComponentTransformer.transform(cls)

    def __new__(cls, el, **kwargs):
        init_dict = cls.init_dict()
        init_dict.update(el=el)
        for key, value in kwargs.items():
            if key == "props_data":
                key = "propsData"
            init_dict.update({key: value})
        return Object.from_js(window.Vue.new(Object.to_js(init_dict)))

    @classmethod
    def register(cls, name=None):
        if name:
            Vue.component(name, cls)
        else:
            Vue.component(cls)


class VueMixin(Transformable):
    pass


class VueDirective(Transformable):
    name = None


class VuePlugin:
    @staticmethod
    def install(*args, **kwargs):
        raise NotImplementedError()
