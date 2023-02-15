from vue import *


def app(el):
    class Store(VueStore):
        message = ""

        @mutation
        def mutate_message(self):
            self.message = "Message"

    class ComponentUsingMutation(VueComponent):
        @computed
        def message(self):
            self.store.commit("mutate_message")
            return self.store.message

        template = "<div id='content'>{{ message }}</div>"

    return ComponentUsingMutation(el, store=Store())


app = app("#app")
