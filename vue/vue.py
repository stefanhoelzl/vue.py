from browser import window
from .factory import VueComponentFactory, Wrapper, \
    VueDirectiveFactory
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

        window.Vue.directive(name, VueDirectiveFactory.get_item(directive))

    @staticmethod
    def filter(method_or_name, method=None):
        if not method:
            method = method_or_name
            name = method_or_name.__name__
        else:
            method = method
            name = method_or_name
        flt = Filter(method, name)
        window.Vue.filter(flt.__id__, flt.__value__)

    @staticmethod
    def mixin(mixin):
        window.Vue.mixin(VueComponentFactory.get_item(mixin))

    @staticmethod
    def use(plugin, *args, **kwargs):
        window.Vue.use(plugin, *args, kwargs)

    @staticmethod
    def component(name, component):
        window.Vue.component(name, component)


class VueComponent(Wrapper):
    @classmethod
    def init_dict(cls):
        return VueComponentFactory.get_item(cls)

    def __new__(cls, el, **data):
        init_dict = cls.init_dict()
        init_dict.update(el=el)
        init_dict.update(propsData=data)
        return Object.from_js(window.Vue.new(init_dict))

    @classmethod
    def register(cls, name=None):
        name = name if name else cls.__name__
        window.Vue.component(name, cls.init_dict())


class VueMixin(Wrapper):
    pass


class VueDirective(Wrapper):
    name = None


class VuePlugin:
    @staticmethod
    def install(*args, **kwargs):
        raise NotImplementedError()
