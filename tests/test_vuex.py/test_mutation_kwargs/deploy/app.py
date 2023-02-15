from vue import *


def app(el):
    class Store(VueStore):
        message = ""

        @mutation
        def mutate_message(self, new_message, postfix=""):
            self.message = new_message + postfix

    class ComponentUsingMutation(VueComponent):
        @computed
        def message(self):
            self.store.commit("mutate_message", "Message", postfix="!")
            return self.store.message

        template = "<div id='content'>{{ message }}</div>"

    return ComponentUsingMutation(el, store=Store())


app = app("#app")
