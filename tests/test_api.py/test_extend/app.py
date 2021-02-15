from vue import *


def extended_component(el):
    class Base(VueComponent):
        template = "<div id='comps'>{{ components_string }}</div>"
        comps = []

        def created(self):
            self.comps.append("BASE")

        @computed
        def components_string(self):
            return " ".join(self.comps)

    class Sub(Base):
        extends = True

        def created(self):
            self.comps.append("SUB")

    return Sub(el)


app = extended_component("#app")
