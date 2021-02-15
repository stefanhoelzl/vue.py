from vue import *


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


app = app("#app")
