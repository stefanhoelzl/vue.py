from vue import *


def app(el):
    class Store(VueStore):
        message = ""

        @mutation
        def mutate_message(self, new_message):
            self.message = new_message

        @action
        def change_message(self, new_message, postfix=""):
            self.commit("mutate_message", new_message + postfix)

    class ComponentUsingAction(VueComponent):
        def created(self):
            self.store.dispatch("change_message", "Message", postfix="!")

        @computed
        def message(self):
            return self.store.message

        template = "<div id='content'>{{ message }}</div>"

    return ComponentUsingAction(el, store=Store())


app = app("#app")
