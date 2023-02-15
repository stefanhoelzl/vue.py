from vue import *


def app(el):
    class Store(VueStore):
        message = "Message"

        @getter
        def msg(self, prefix):
            return prefix + self.message

    class ComponentUsingGetter(VueComponent):
        @computed
        def message(self):
            return self.store.msg("pre")

        template = "<div id='content'>{{ message }}</div>"

    return ComponentUsingGetter(el, store=Store())


app = app("#app")
