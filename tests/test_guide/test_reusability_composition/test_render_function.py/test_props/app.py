from vue import *


def app(el):
    class ComponentWithProps(VueComponent):
        prop: str = "p"
        template = "<div :id='prop'></div>"

    ComponentWithProps.register()

    class ComponentRendersWithAttrs(VueComponent):
        def render(self, create_element):
            return create_element("ComponentWithProps", {"props": {"prop": "p"}})

    return ComponentRendersWithAttrs(el)


app = app("#app")
