from vue import *


def app(el):
    class Store(VueStore):
        message = "Message"

    class ComponentUsingStore(VueComponent):
        @computed
        def message(self):
            return self.store.message

        template = "<div id='content'>{{ message }}</div>"

    return ComponentUsingStore(el, store=Store())


app = app("#app")
