from vue import VueComponent, computed


class NavigationItem(VueComponent):
    item: dict
    template = """
    <el-menu-item-group v-if="is_group_header">
        <span slot="title">{{ item.group }}</span>
    </el-menu-item-group>
    <component v-else
        @click="click()"
        :is="item_tag" 
        :disabled="item.disabled"
        :index="item.id">
        <template v-if="is_submenu">
            <template slot="title">
                <i :class="item.icon"></i>
                <span slot="title">{{ item.title }}</span>
            </template>
            <navigation-item 
                v-for="sub_item in item.children"
                :key="sub_item.id"
                :item="sub_item"
                >
            </navigation-item>
        </template>
        <template v-else>
            <i :class="item.icon"></i>
            {{ item.title }}
        </template>
    </component>
    """

    @computed
    def item_tag(self):
        if self.is_submenu:
            return "el-submenu"
        return "el-menu-item"

    @computed
    def is_menu_item(self):
        return not self.is_group_header and not self.is_submenu

    @computed
    def is_group_header(self):
        return "group" in self.item

    @computed
    def is_submenu(self):
        return "children" in self.item

    def click(self):
        self.notify.info({
            "title": "Navigation",
            "message": self.item.get("title", "NO TITLE")
        })


NavigationItem.register()


class NavigationMenu(VueComponent):
    content: list
    template = """
    <div>
        <el-menu
            @select="select"
            class="navigation-menu">
            <navigation-item 
                v-for="item in content"
                :key="item.id"
                :item="item"
                >
            </navigation-item>
        </el-menu>
    </div>
    """

    def select(self, index, path, *args):
        self.emit("select", index, path)


NavigationMenu.register()


class App(VueComponent):
    template = """
    <div>
        <navigation-menu 
            @select="selected"
            :content="navigation_menu">
        </navigation-menu>
    </div>
    """

    navigation_menu = content = [
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

    def selected(self, index, path):
        print(index, path)


App("#app")
