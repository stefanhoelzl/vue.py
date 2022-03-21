from vue import *

from selenium.webdriver.common.by import By


def test_customize_v_model(selenium):
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

    with selenium.app(app):
        assert selenium.element_has_text("instance", "false")
        assert selenium.element_has_text("component", "false")
        selenium.find_element(by=By.ID, value="c").click()
        assert selenium.element_has_text("component", "true")
        assert selenium.element_has_text("instance", "true")
