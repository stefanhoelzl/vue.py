from vue import *


def app(el):
    class CustomVModel(VueComponent):
        model = Model(prop="checked", event="change")
        checked: bool
        template = """
        <div>
            <p id="component">{{ checked }}</p>
            <input
                id="c"
                type="checkbox"
                :checked="checked"
                @change="$emit('change', $event.target.checked)"
            >
        </div>
        """

    CustomVModel.register("custom-vmodel")

    class App(VueComponent):
        clicked = False
        template = """
        <div>
            <p id='instance'>{{ clicked }}</p>
            <custom-vmodel v-model="clicked"></custom-vmodel>
        </div>
        """

    return App(el)


app = app("#app")
