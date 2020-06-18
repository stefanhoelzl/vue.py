from vue import *

VuexConfig = {"scripts": {"vuex": True}}


def test_state(selenium):
    def app(el):
        class Store(VueStore):
            message = "Message"

        class ComponentUsingStore(VueComponent):
            @computed
            def message(self):
                return self.store.message

            template = "<div id='content'>{{ message }}</div>"

        return ComponentUsingStore(el, store=Store())

    with selenium.app(app, config=VuexConfig):
        assert selenium.element_has_text("content", "Message")


def test_mutation_noargs(selenium):
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

    with selenium.app(app, config=VuexConfig):
        assert selenium.element_has_text("content", "Message")


def test_mutation(selenium):
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

    with selenium.app(app, config=VuexConfig):
        assert selenium.element_has_text("content", "Message")


def test_mutation_kwargs(selenium):
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

    with selenium.app(app, config=VuexConfig):
        assert selenium.element_has_text("content", "Message!")


def test_action(selenium):
    def app(el):
        class Store(VueStore):
            message = ""

            @mutation
            def mutate_message(self, new_message):
                self.message = new_message

            @action
            def change_message(self, new_message):
                self.commit("mutate_message", new_message)

        class ComponentUsingAction(VueComponent):
            def created(self):
                self.store.dispatch("change_message", "Message")

            @computed
            def message(self):
                return self.store.message

            template = "<div id='content'>{{ message }}</div>"

        return ComponentUsingAction(el, store=Store())

    with selenium.app(app, config=VuexConfig):
        assert selenium.element_has_text("content", "Message")


def test_action_noargs(selenium):
    def app(el):
        class Store(VueStore):
            message = ""

            @mutation
            def mutate_message(self, new_message):
                self.message = new_message

            @action
            def change_message(self):
                self.commit("mutate_message", "Message")

        class ComponentUsingAction(VueComponent):
            def created(self):
                self.store.dispatch("change_message")

            @computed
            def message(self):
                return self.store.message

            template = "<div id='content'>{{ message }}</div>"

        return ComponentUsingAction(el, store=Store())

    with selenium.app(app, config=VuexConfig):
        assert selenium.element_has_text("content", "Message")


def test_action_kwargs(selenium):
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

    with selenium.app(app, config=VuexConfig):
        assert selenium.element_has_text("content", "Message!")


def test_getter_noargs(selenium):
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

    with selenium.app(app, config=VuexConfig):
        assert selenium.element_has_text("content", "Message")


def test_getter_method(selenium):
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

    with selenium.app(app, config=VuexConfig):
        assert selenium.element_has_text("content", "preMessage")


def test_getter_kwargs(selenium):
    def app(el):
        class Store(VueStore):
            message = "Message"

            @getter
            def msg(self, prefix, postfix):
                return prefix + self.message + postfix

        class ComponentUsingGetter(VueComponent):
            @computed
            def message(self):
                return self.store.msg("pre", "!")

            template = "<div id='content'>{{ message }}</div>"

        return ComponentUsingGetter(el, store=Store())

    with selenium.app(app, config=VuexConfig):
        assert selenium.element_has_text("content", "preMessage!")


def test_plugin(selenium):
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

    with selenium.app(app, config=VuexConfig):
        assert selenium.element_has_text("content", "Message")
        last_log_message = selenium.get_logs()[-1]["message"]
        expected_msg = "Message msg ('Hallo',) {'postfix': '!'}"
        assert expected_msg in last_log_message


def test_using_state_within_native_vue_component(selenium):
    def app(el):
        class Store(VueStore):
            message = "Message"

        class ComponentUsingNativeComponent(VueComponent):
            template = "<native />"

        return ComponentUsingNativeComponent(el, store=Store())

    config = {"scripts": {"vuex": True, "my": "my.js"}}
    myjs = """
        Vue.component('native', {
          template: '<div id="content">{{ message }}</div>',
          computed: {
            message () {
              return this.$store.state.message
            }
          }
        });
    """
    with selenium.app(app, config=config, files={"my.js": myjs}):
        assert selenium.element_has_text("content", "Message")
