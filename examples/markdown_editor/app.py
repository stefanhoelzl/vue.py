from vue import VueComponent, computed
from browser import window as js


class App(VueComponent):
    input = "# hello"

    @computed
    def compiled_markdown(self):
        return js.marked(self.input, {'sanitize': True})

    def update(self, event):
        self.input = event.target.value


App("#editor")
