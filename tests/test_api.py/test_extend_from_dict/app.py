from vue import *


class Component(VueComponent):
    template = "<div id='done'>{{ done }}</div>"
    done = "NO"
    extends = {"created": lambda: print("CREATED BASE")}

    def created(self):
        print("CREATED SUB")
        self.done = "YES"


app = Component("#app")
