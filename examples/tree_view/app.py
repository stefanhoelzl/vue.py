from vue import VueComponent, computed

demo_data = {
    "name": "My Tree",
    "children": [
        {"name": "hello"},
        {"name": "wat"},
        {
            "name": "child folder",
            "children": [
                {
                    "name": "child folder",
                    "children": [{"name": "hello"}, {"name": "wat"}],
                },
                {"name": "hello"},
                {"name": "wat"},
                {
                    "name": "child folder",
                    "children": [{"name": "hello"}, {"name": "wat"}],
                },
            ],
        },
    ],
}


class Tree(VueComponent):
    template = "#tree-template"
    model: dict
    open = False

    @computed
    def is_folder(self):
        return len(self.model.get("children", ())) > 0

    def toggle(self, ev=None):
        if self.is_folder:
            self.open = not self.open

    def change_type(self, ev=None):
        if not self.is_folder:
            self.model["children"] = []
            self.add_child()
            self.open = True

    def add_child(self, ev=None):
        self.model["children"].append({"name": "new stuff"})


Tree.register()


class App(VueComponent):
    template = "#app-template"
    tree_data = demo_data


App("#app")
