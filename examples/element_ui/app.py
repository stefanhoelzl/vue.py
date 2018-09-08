from vue import VueComponent
from .components import navigation


navigation.register()


class App(VueComponent):
    template = "#navigation"

    navigation_menu = [
        {"id": "one", "title": "Navigation One", "icon": "el-icon-location",
         "children": [
             {"group": "Group One"},
             {"id": "one.one", "title": "Item One"},
             {"id": "one.two", "title": "Item Two"},
             {"group": "Group Two"},
             {"id": "one.hree", "title": "Item Three"},
             {"id": "one.four", "title": "Item Four", "children": [
                 {"id": "one.four.five", "title": "Item Five"}
             ]},
         ]
         },
        {"id": "two", "title": "Navigation Two", "icon": "el-icon-menu"},
        {"id": "three", "title": "Navigation Three", "icon": "el-icon-document",
         "disabled": True},
        {"id": "four", "title": "Navigation Four", "icon": "el-icon-setting"},
    ]

    def clicked(self, item):
        print(item)
        self.notify.info({
            "title": "Navigation",
            "message": item.get("title", "NO TITLE")
        })


App("#app")
