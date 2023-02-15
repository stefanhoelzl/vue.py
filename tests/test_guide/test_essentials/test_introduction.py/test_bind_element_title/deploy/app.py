from vue import *


class BindElementTitle(VueComponent):
    title = "TITLE"
    template = "<div id='withtitle' v-bind:title='title'></div>"


app = BindElementTitle("#app")
