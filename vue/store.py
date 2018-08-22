from browser import window
from .factory import Wrapper, VueStoreFactory
from .bridge import Object


class VueStore(Wrapper):
    @classmethod
    def init_dict(cls):
        return VueStoreFactory.get_item(cls)

    def __new__(cls):
        return Object.from_js(window.Vuex.Store.new(cls.init_dict()))
