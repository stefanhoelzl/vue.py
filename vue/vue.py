from browser import window
from .factory import VueComponentFactory
from .bridge import Object


class VueComponent:
    template = ""

    def __new__(cls, el, **data):
        init_dict = VueComponentFactory.dict(cls, VueComponent)
        init_dict.update(el=el)
        init_dict.update(propsData=data)
        return Object.from_js(window.Vue.new(init_dict))

    @classmethod
    def register(cls, name=None):
        name = name if name else cls.__name__
        window.Vue.component(name, VueComponentFactory.dict(cls, VueComponent))
