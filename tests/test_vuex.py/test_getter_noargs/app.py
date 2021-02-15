from vue import *


def app(el):
    class Store(VueStore):
        message = "Message"

        @getter
        def msg(self):
            return self.message

    class ComponentUsingGetter(VueComponent):
        @computed
        def message(self):
            return self.store.msg

        template = "<div id='content'>{{ message }}</div>"

    return ComponentUsingGetter(el, store=Store())


app = app("#app")
