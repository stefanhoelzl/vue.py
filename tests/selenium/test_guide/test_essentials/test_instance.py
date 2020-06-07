from vue import *


def test_lifecycle_hooks(selenium):
    def lifecycle_hooks(el):
        class ComponentLifecycleHooks(VueComponent):
            text: str
            template = "<div>{{ text }}</div>"

            def before_create(self):
                print("lh: before_created", self)

            def created(self):
                print("lh: created", self)

            def before_mount(self):
                print("lh: before_mount", self)

            def mounted(self):
                print("lh: mounted", self)

            def before_update(self):
                print("lh: before_update", self)

            def updated(self):
                print("lh: updated", self)

            def before_destroy(self):
                print("lh: before_destroy", self)

            def destroyed(self):
                print("lh: destroyed", self)

        ComponentLifecycleHooks.register("clh")

        class App(VueComponent):
            show = True
            text = "created"

            def mounted(self):
                self.text = "mounted"

            def updated(self):
                self.show = False

            template = (
                "<clh v-if='show' :text='text'></clh>"
                "<div v-else id='after' :text='text'></div>"
            )

        return App(el)

    with selenium.app(lifecycle_hooks):
        selenium.element_present("after")
        logs = list(filter(lambda l: "lh: " in l["message"], selenium.get_logs()))
        for idx, log_message in enumerate(
            [
                "lh: before_create",
                "lh: created",
                "lh: before_mount",
                "lh: mounted",
                "lh: before_update",
                "lh: updated",
                "lh: before_destroy",
                "lh: destroyed",
            ]
        ):
            assert log_message in logs[idx]["message"]
