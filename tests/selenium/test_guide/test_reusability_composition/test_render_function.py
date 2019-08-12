from vue import *


def test_basics(selenium):
    def app(el):
        class ComponentWithRenderFunction(VueComponent):
            level = 3

            def render(self, create_element):
                return create_element(f"h{self.level}", "Title")

        return ComponentWithRenderFunction(el)

    with selenium.app(app):
        assert selenium.element_with_tag_name_has_text("h3", "Title")


def test_slots(selenium):
    def app(el):
        class WithSlots(VueComponent):
            def render(self, create_element):
                return create_element(f"p", self.slots.get("default"))
        WithSlots.register()

        class Component(VueComponent):
            template = "<with-slots><p></p><p></p></with-slots>"

        return Component(el)

    with selenium.app(app):
        div = selenium.element_with_tag_name_present("p")
        assert len(div.find_elements_by_tag_name("p")) == 2


def test_empty_slots(selenium):
    def app(el):
        class WithSlots(VueComponent):
            def render(self, create_element):
                return create_element(f"div", self.slots.get("default"))
        WithSlots.register()

        class Component(VueComponent):
            template = "<with-slots />"

        return Component(el)

    with selenium.app(app):
        pass


def test_props(selenium):
    def app(el):
        class ComponentWithProps(VueComponent):
            prop: str = "p"
            template = "<div :id='prop'></div>"

        ComponentWithProps.register()

        class ComponentRendersWithAttrs(VueComponent):
            def render(self, create_element):
                return create_element(
                    "ComponentWithProps", {"props": {"prop": "p"}},
                )

        return ComponentRendersWithAttrs(el)

    with selenium.app(app):
        assert selenium.element_present("p")
