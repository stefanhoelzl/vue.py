from vue import *


def app(el):
    class Plugin(VueStorePlugin):
        def initialize(self, store):
            store.message = "Message"

        def subscribe(self, state, mut, *args, **kwargs):
            print(state.message, mut, args, kwargs)

    class Store(VueStore):
        plugins = [Plugin().install]
        message = ""

        @mutation
        def msg(self, prefix, postfix=""):
            pass

    class ComponentUsingGetter(VueComponent):
        @computed
        def message(self):
            return self.store.message

        def created(self):
            self.store.commit("msg", "Hallo", postfix="!")

        template = "<div id='content'>{{ message }}</div>"

    return ComponentUsingGetter(el, store=Store())


app = app("#app")
