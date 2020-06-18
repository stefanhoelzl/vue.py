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


def test_named_routes(selenium):
    def app(el):
        from vue import VueComponent, VueRouter, VueRoute

        class FooHeader(VueComponent):
            template = '<div id="header">foo header</div>'

        class FooBody(VueComponent):
            template = '<div id="body">foo body</div>'
        
        class BarHeader(VueComponent):
            template = '<div id="header">bar header</div>'

        class BarBody(VueComponent):
            template = '<div id="body">bar body</div>'
        
        class Router(VueRouter):
            routes = [
                VueRoute("/foo", components={
                    "default": FooBody,
                    "header": FooHeader
                }),
                VueRoute("/bar", components={
                    "default": BarBody,
                    "header": BarHeader
                }),
            ]

        class ComponentUsingRouter(VueComponent):
            template = """
                <div>
                    <p>
                        <router-link to="/foo" id="foo">Go to Foo</router-link>
                        <router-link to="/bar" id="bar">Go to Bar</router-link>
                    </p>
                    <router-view name="header"></router-view>
                    <hr>
                    <router-view></router-view>
                </div>
            """
        return ComponentUsingRouter(el, router=Router())

    with selenium.app(app, config=VueRouterConfig):
        assert selenium.element_present("foo")
        selenium.find_element_by_id("foo").click()
        assert selenium.element_has_text("header", "foo header")
        assert selenium.element_has_text("body", "foo body")

        assert selenium.element_present("bar")
        selenium.find_element_by_id("bar").click()
        assert selenium.element_has_text("header", "bar header")
        assert selenium.element_has_text("body", "bar body")


def test_nested_routes(selenium):
    def app(el):
        from vue import VueComponent, VueRouter, VueRoute

        class Admins(VueComponent):
            template = '''
                <ol>
                    <li><router-link to="/admin/1" id="admin-1">Parvana Chantrea</router-link></li>
                </ol>
            '''

        class Users(VueComponent):
            template = '''
                <ol>
                    <li><router-link to="/user/1" id="user-1">Isa Shiro</router-link></li>
                </ol>
            '''
    
        class Admin(VueComponent):
            template = '<div id="admin">{{ $route.params.id }}</div>'

        class User(VueComponent):
            template = '<div id="user">{{ $route.params.id }}</div>'

        class Router(VueRouter):
            routes = [
                VueRoute("/admin", Admins, children=[
                    VueRoute(":id", Admin)
                ]),
                VueRoute("/user", Users, children=[
                    VueRoute(":id", User)
                ]),
            ]

        class ComponentUsingRouter(VueComponent):
            template = """
                <div>
                    <p>
                        <router-link to="/admin" id="admin-link">Admins</router-link>
                        <router-link to="/user" id="user-link">Users</router-link>
                    </p>
                    <router-view></router-view>
                </div>
            """
        return ComponentUsingRouter(el, router=Router())

    with selenium.app(app, config=VueRouterConfig):
        assert selenium.element_present("admin-link")
        selenium.find_element_by_id("admin-link").click()
        selenium.find_element_by_id("admin-1").click()
        assert selenium.element_has_text("admin", "1")

        assert selenium.element_present("user-link")
        selenium.find_element_by_id("user-link").click()
        selenium.find_element_by_id("user-1").click()
        assert selenium.element_has_text("user", "1")


def test_route_redirect(selenium):
    def app(el):
        from vue import VueComponent, VueRouter, VueRoute

        class Foo(VueComponent):
            template = '<div id="content">foo</div>'

        class Router(VueRouter):
            routes = [
                VueRoute("/foo", Foo),
                VueRoute("/bar", redirect="/foo"),
            ]

        class ComponentUsingRouter(VueComponent):
            template = """
                <div>
                    <p>
                        <router-link to="/foo" id="foo">Direct</router-link>
                        <router-link to="/bar" id="bar">Redirect</router-link>
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
        assert selenium.element_has_text("content", "foo")
