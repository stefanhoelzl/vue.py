from browser import window
from .factory import Wrapper, VueRouterFactory


def init_dict(component):
    return component.init_dict()


class VueRouter(Wrapper):
    @classmethod
    def init_dict(cls):
        return VueRouterFactory.get_item(cls)

    def __new__(cls, VueRouterObject=window.VueRouter):
        window.Vue.use(VueRouterObject)
        return VueRouterObject.new(cls.init_dict())


class VueRoute:
    def __new__(cls, path, component=None, components=None, **kwargs):
        route = {"path": path}
        route.update(kwargs)
        
        if component is not None:
            route["component"] = component.init_dict()
        elif components is not None:
            route["components"] = {k: init_dict(v) for k, v in components.items()}
        
        return route
