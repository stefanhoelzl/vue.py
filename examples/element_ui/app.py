from vue import VueComponent, computed


class NavigationItem(VueComponent):
    item: dict
    template = """
    <el-menu-item-group v-if="is_group_header">
        <span slot="title">{{ item.group }}</span>
    </el-menu-item-group>
    <component v-else
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


NavigationItem.register()


class NavigationMenu(VueComponent):
    content: list
    template = """
    <div>
        <el-menu
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


NavigationMenu.register()


class App(VueComponent):
    template = """
    <div>
        <navigation-menu :content="navigation_menu"></navigation-menu>
    </div>
    """

    navigation_menu = content = [
        {"id": "One", "title": "Navigation One", "icon": "el-icon-location",
         "children": [
             {"group": "Group One"},
             {"id": "OneOneOne", "title": "Item One"},
             {"id": "OneOneTwo", "title": "Item Two"},
             {"group": "Group Two"},
             {"id": "OneTwoOne", "title": "Item Three"},
             {"id": "OneTwoTwo", "title": "Item Four", "children": [
                 {"id": "OneThree", "title": "Item Five"}
             ]},
         ]
         },
        {"id": "Two", "title": "Navigation Two", "icon": "el-icon-menu"},
        {"id": "Three", "title": "Navigation Three", "icon": "el-icon-document",
         "disabled": True},
        {"id": "Four", "title": "Navigation Four", "icon": "el-icon-setting"},
    ]


App("#app")
