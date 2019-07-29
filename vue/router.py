from browser import window
from .factory import Wrapper, VueRouterFactory


class VueRouter(Wrapper):
    @classmethod
    def init_dict(cls):
        return VueRouterFactory.get_item(cls)

    def __new__(cls):
        return window.VueRouter.new(cls.init_dict())


class VueRoute:
    def __new__(cls, path, component):
        return {"path": path, "component": component}
