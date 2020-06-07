VueRouterConfig = {"scripts": {"vue-router": True}}


def test_routes(selenium):
    def app(el):
        from vue import VueComponent, VueRouter, VueRoute

        class Foo(VueComponent):
            template = '<div id="content">foo</div>'

        class Bar(VueComponent):
            text = "bar"
            template = '<div id="content">{{ text }}</div>'

        class Router(VueRouter):
            routes = [VueRoute("/foo", Foo), VueRoute("/bar", Bar)]

        class ComponentUsingRouter(VueComponent):
            template = """
                <div>
                    <p>
                        <router-link to="/foo" id="foo">Go to Foo</router-link>
                        <router-link to="/bar" id="bar">Go to Bar</router-link>
                    </p>
                    <router-view></router-view>
                </div>
            """

        return ComponentUsingRouter(el, router=Router())

    with selenium.app(app, config=VueRouterConfig):
        assert selenium.element_present("foo")
        selenium.find_element_by_id("foo").click()
        assert selenium.element_has_text("content", "foo")

        assert selenium.element_present("bar")
        selenium.find_element_by_id("bar").click()
        assert selenium.element_has_text("content", "bar")


def test_dynamic_route_matching(selenium):
    def app(el):
        from vue import VueComponent, VueRouter, VueRoute

        class User(VueComponent):
            template = '<div id="user">{{ $route.params.id }}</div>'

        class Router(VueRouter):
            routes = [VueRoute("/user/:id", User)]

        class ComponentUsingRouter(VueComponent):
            template = """
                <div>
                    <p>
                        <router-link to="/user/123" id="link">User</router-link>
                    </p>
                    <router-view></router-view>
                </div>
            """

        return ComponentUsingRouter(el, router=Router())

    with selenium.app(app, config=VueRouterConfig):
        assert selenium.element_present("link")
        selenium.find_element_by_id("link").click()
        assert selenium.element_has_text("user", "123")
