from vue import VueComponent, VueStore, computed


def test_init_with_store(selenium):
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
