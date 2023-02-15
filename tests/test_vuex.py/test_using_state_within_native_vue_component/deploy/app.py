from vue import *


def app(el):
    class Store(VueStore):
        message = "Message"

    class ComponentUsingNativeComponent(VueComponent):
        template = "<native />"

    return ComponentUsingNativeComponent(el, store=Store())


app = app("#app")
