from vue import *


def app(el):
    class ComponentWithRenderFunction(VueComponent):
        level = 3

        def render(self, create_element):
            return create_element(f"h{self.level}", "Title")

    return ComponentWithRenderFunction(el)


app = app("#app")
