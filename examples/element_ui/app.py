from vue import VueComponent


class App(VueComponent):
    template = """
    <div>
        <navigation-menu 
            @click="clicked"
            :content="navigation_menu">
        </navigation-menu>
    </div>
    """

    navigation_menu = [
        {"id": "One", "title": "Navigation One", "icon": "el-icon-location",
         "children": [
             {"group": "Group One"},
             {"id": "One", "title": "Item One"},
             {"id": "Two", "title": "Item Two"},
             {"group": "Group Two"},
             {"id": "Three", "title": "Item Three"},
             {"id": "Four", "title": "Item Four", "children": [
                 {"id": "Five", "title": "Item Five"}
             ]},
         ]
         },
        {"id": "Two", "title": "Navigation Two", "icon": "el-icon-menu"},
        {"id": "Three", "title": "Navigation Three", "icon": "el-icon-document",
         "disabled": True},
        {"id": "Four", "title": "Navigation Four", "icon": "el-icon-setting"},
    ]

    def clicked(self, item):
        print(item)
        self.notify.info({
            "title": "Navigation",
            "message": item.get("title", "NO TITLE")
        })


App("#app")
