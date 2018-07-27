from browser import window
from .factory import VueComponentFactory, Wrapper, VueDirectiveFactory
from .bridge import Object
from .decorators.directive import DirectiveHook


class Vue:
    @staticmethod
    def directive(name_or_directive, function_directive=None):
        if isinstance(name_or_directive, str):
            if function_directive is None:
                return window.Vue.directive(name_or_directive)

            class FunctionDirective(VueDirective):
                name = name_or_directive
                d = DirectiveHook(function_directive)
            name_or_directive = FunctionDirective

        window.Vue.directive(*VueDirectiveFactory.get_item(name_or_directive))


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
