from vue import *


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


app = app("#app")
