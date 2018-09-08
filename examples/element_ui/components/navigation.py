from vue import VueComponent, computed


class NavigationItem(VueComponent):
    item: dict
    template = """
    <el-menu-item-group v-if="is_group_header">
        <span slot="title">{{ item.group }}</span>
    </el-menu-item-group>
    <component v-else
        @click="$emit('click', item)"
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
                @click="$emit('click', $event)"
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


class NavigationMenu(VueComponent):
    content: list
    template = """
    <div>
        <el-menu
            class="navigation-menu">
            <navigation-item 
                @click="$emit('click', $event)"
                v-for="item in content"
                :key="item.id"
                :item="item"
                >
            </navigation-item>
        </el-menu>
    </div>
    """


def register():
    NavigationItem.register()
    NavigationMenu.register()
