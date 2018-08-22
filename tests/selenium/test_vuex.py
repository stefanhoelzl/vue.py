from vue import *


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

        class ComponentUsingMutation(VueComponent):
            @computed
            def message(self):
                self.store.commit("mutate_message", "Message")
                return self.store.state.message

            template = "<div id='content'>{{ message }}</div>"
        return ComponentUsingMutation(el, store=Store())

    with selenium.app(app):
        assert selenium.element_has_text("content", "Message")


def test_action(selenium):
    def app(el):
        class Store(VueStore):
            message = ""

            @staticmethod
            @mutation
            def mutate_message(state, new_message):
                state["message"] = new_message

            @staticmethod
            @action
            def change_message(context, new_message):
                context.commit("mutate_message", new_message)

        class ComponentUsingAction(VueComponent):
            def created(self):
                self.store.dispatch("change_message", "Message")

            @computed
            def message(self):
                return self.store.state.message

            template = "<div id='content'>{{ message }}</div>"
        return ComponentUsingAction(el, store=Store())

    with selenium.app(app):
        assert selenium.element_has_text("content", "Message")


def test_getter(selenium):
    def app(el):
        class Store(VueStore):
            message = "Message"

            @staticmethod
            @getter
            def msg(state, getters):
                return state["message"]

        class ComponentUsingGetter(VueComponent):
            @computed
            def message(self):
                return self.store.getters.msg

            template = "<div id='content'>{{ message }}</div>"
        return ComponentUsingGetter(el, store=Store())

    with selenium.app(app):
        assert selenium.element_has_text("content", "Message")


def test_getter_method(selenium):
    def app(el):
        class Store(VueStore):
            message = "Message"

            @staticmethod
            @getter_method
            def msg(state, getters, prefix):
                return prefix + state["message"]

        class ComponentUsingGetter(VueComponent):
            @computed
            def message(self):
                return self.store.getters.msg("pre")

            template = "<div id='content'>{{ message }}</div>"
        return ComponentUsingGetter(el, store=Store())

    with selenium.app(app):
        assert selenium.element_has_text("content", "preMessage")
