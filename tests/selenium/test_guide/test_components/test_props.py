from vue import *


def test_prop_types(selenium):
    def app(el):
        class SubComponent(VueComponent):
            prop = Property(type=int)
            template = "<div></div>"

            def created(self):
                assert isinstance(self.prop, int)

        SubComponent.register()
        class App(VueComponent):
            template = """
            <sub-component id="component" :prop="100"></sub-component>
            """

        return App(el)

    with selenium.app(app):
        pass
