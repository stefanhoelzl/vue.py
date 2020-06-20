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

        class FooTop(VueComponent):
            template = '<div id="header">foo top</div>'

        class FooBottom(VueComponent):
            template = '<div id="body">foo bottom</div>'

        class BarTop(VueComponent):
            template = '<div id="header">bar top</div>'

        class BarBottom(VueComponent):
            template = '<div id="body">bar bottom</div>'

        class Router(VueRouter):
            routes = [
                VueRoute("/foo", components={"default": FooBottom, "top": FooTop}),
                VueRoute("/bar", components={"default": BarBottom, "top": BarTop}),
            ]

        class ComponentUsingRouter(VueComponent):
            template = """
                <div>
                    <p>
                        <router-link to="/foo" id="foo">Go to Foo</router-link>
                        <router-link to="/bar" id="bar">Go to Bar</router-link>
                    </p>
                    <router-view name="top"></router-view>
                    <hr>
                    <router-view></router-view>
                </div>
            """

        return ComponentUsingRouter(el, router=Router())

    with selenium.app(app, config=VueRouterConfig):
        assert selenium.element_present("foo")
        selenium.find_element_by_id("foo").click()
        assert selenium.element_has_text("header", "foo top")
        assert selenium.element_has_text("body", "foo bottom")

        assert selenium.element_present("bar")
        selenium.find_element_by_id("bar").click()
        assert selenium.element_has_text("header", "bar top")
        assert selenium.element_has_text("body", "bar bottom")


def test_nested_routes_and_redirect(selenium):
    def app(el):
        from vue import VueComponent, VueRouter, VueRoute

        class UserHome(VueComponent):
            template = '<div id="home">Home</div>'

        class UserProfile(VueComponent):
            template = '<div id="profile">Profile</div>'

        class UserPosts(VueComponent):
            template = '<div id="posts">Posts</div>'

        class ComponentUsingRouter(VueComponent):
            template = """
                <div>
                    <p>
                        <router-link to="/user/foo" id="link-home">/user/foo</router-link>
                        <router-link to="/user/foo/profile" id="link-profile">/user/foo/profile</router-link>
                        <router-link to="/user/foo/posts" id="link-posts">/user/foo/posts</router-link>
                    </p>
                    <h2>User {{ $route.params.id }}</h2>
                    <router-view></router-view>
                </div>
            """

        class Router(VueRouter):
            routes = [
                VueRoute("/", redirect="/user/foo"),
                VueRoute(
                    "/user/:id",
                    ComponentUsingRouter,
                    children=[
                        VueRoute("", UserHome),
                        VueRoute("profile", UserProfile),
                        VueRoute("posts", UserPosts),
                    ],
                ),
            ]

        return ComponentUsingRouter(el, router=Router())

    with selenium.app(app, config=VueRouterConfig):
        assert selenium.element_present("link-home")
        selenium.find_element_by_id("link-home").click()
        assert selenium.element_has_text("home", "Home")

        assert selenium.element_present("link-profile")
        selenium.find_element_by_id("link-profile").click()
        assert selenium.element_has_text("profile", "Profile")

        assert selenium.element_present("link-posts")
        selenium.find_element_by_id("link-posts").click()
        assert selenium.element_has_text("posts", "Posts")
