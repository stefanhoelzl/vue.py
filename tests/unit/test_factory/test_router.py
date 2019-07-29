from vue import *


class TestVueRoute:
    def test_path_and_component(self):
        route = VueRoute("/path", VueComponent)
        assert route == {"path": "/path", "component": VueComponent}


class TestVueRouter:
    def test_routes(self):
        class Router(VueRouter):
            routes = [VueRoute("/path", VueComponent)]

        routes = Router.init_dict()["routes"]
        assert routes == [{"path": "/path", "component": VueComponent}]
