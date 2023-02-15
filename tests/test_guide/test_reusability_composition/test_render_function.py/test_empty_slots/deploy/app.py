from vue import *


def app(el):
    class WithSlots(VueComponent):
        def render(self, create_element):
            return create_element(f"div", self.slots.get("default"))

    WithSlots.register()

    class Component(VueComponent):
        template = "<with-slots />"

    return Component(el)


app = app("#app")
