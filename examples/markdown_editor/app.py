from vue import VueComponent, computed
from vue.utils import js_lib

marked = js_lib("marked")


class App(VueComponent):
    template = "#editor-template"

    input = "# Editor"

    @computed
    def compiled_markdown(self):
        return marked(self.input, {"sanitize": True})

    def update(self, event):
        self.input = event.target.value


App("#app")
