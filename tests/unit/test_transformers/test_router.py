from unittest.mock import Mock
from vue import *


class TestVueRoute:
    def test_path_and_component(self):
        route = VueRoute("/path", VueComponent)
        assert route == {"path": "/path", "component": VueComponent.init_dict()}

    def test_path_and_components(self):
        route = VueRoute(
            "/path", components={"default": VueComponent, "named": VueComponent}
        )
        assert route == {
            "path": "/path",
            "components": {
                "default": VueComponent.init_dict(),
                "named": VueComponent.init_dict(),
            },
        }

    def test_path_and_components_and_children(self):
        route = VueRoute(
            "/path",
            VueComponent,
            children=[
                VueRoute("/path", VueComponent),
                VueRoute("/path2", VueComponent),
            ],
        )
        assert route == {
            "path": "/path",
            "component": VueComponent.init_dict(),
            "children": [
                {"path": "/path", "component": VueComponent.init_dict()},
                {"path": "/path2", "component": VueComponent.init_dict()},
            ],
        }

    def test_path_and_redirect(self):
        route = VueRoute("/path", redirect="/path2")
        assert route == {"path": "/path", "redirect": "/path2"}


class TestVueRouter:
    def test_routes(self):
        class Router(VueRouter):
            routes = [VueRoute("/path", VueComponent)]

        routes = Router.init_dict()["routes"]
        assert routes == [{"path": "/path", "component": VueComponent.init_dict()}]

    def test_custom_router(self):
        router_class_mock = Mock()
        router_class_mock.new.return_value = "CustomRouter"

        class Router(VueRouter):
            RouterClass = router_class_mock

        router = Router()
        assert router == "CustomRouter"
        router_class_mock.new.assert_called_with(Router.init_dict())
