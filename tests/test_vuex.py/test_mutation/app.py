from vue import *


def app(el):
    class Store(VueStore):
        message = ""

        @mutation
        def mutate_message(self, new_message):
            self.message = new_message

    class ComponentUsingMutation(VueComponent):
        @computed
        def message(self):
            self.store.commit("mutate_message", "Message")
            return self.store.message

        template = "<div id='content'>{{ message }}</div>"

    return ComponentUsingMutation(el, store=Store())


app = app("#app")
