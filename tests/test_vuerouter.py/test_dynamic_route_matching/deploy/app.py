from vue import *


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


app = app("#app")
