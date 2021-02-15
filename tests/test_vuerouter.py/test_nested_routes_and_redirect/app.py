from vue import *


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


app = app("#app")
