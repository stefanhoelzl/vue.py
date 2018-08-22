from vue import VueComponent, VueStore, computed, mutation


def test_state(selenium):
    def app(el):
        class Store(VueStore):
            message = "Message"

        class ComponentUsingStore(VueComponent):
            @computed
            def message(self):
                return self.store.state.message

            template = "<div id='content'>{{ message }}</div>"
        return ComponentUsingStore(el, store=Store())

    with selenium.app(app):
        assert selenium.element_has_text("content", "Message")


def test_mutation(selenium):
    def app(el):
        class Store(VueStore):
            message = ""

            @staticmethod
            @mutation
            def mutate_message(state, new_message):
                state["message"] = new_message

        class ComponentUsingStore(VueComponent):
            @computed
            def message(self):
                self.store.commit("mutate_message", "Message")
                return self.store.state.message

            template = "<div id='content'>{{ message }}</div>"
        return ComponentUsingStore(el, store=Store())

    with selenium.app(app):
        assert selenium.element_has_text("content", "Message")
