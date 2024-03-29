from browser import window
from .transformers import Transformable, VueRouterTransformer


class VueRouter(Transformable):
    RouterClass = None

    @classmethod
    def init_dict(cls):
        return VueRouterTransformer.transform(cls)

    def __new__(cls):
        router_class = cls.RouterClass or window.VueRouter
        return router_class.new(cls.init_dict())


class VueRoute:
    def __new__(cls, path, component=None, components=None, **kwargs):
        route = {"path": path, **kwargs}

        if component is not None:
            route["component"] = component.init_dict()
        elif components is not None:
            route["components"] = {
                name: component.init_dict() for name, component in components.items()
            }

        return route
