from browser import timer, window

from vue import VueComponent
from components import *

from vue.utils import js_lib


LOADING_TOPIC = "vuepy/loading"

VueMqtt = js_lib("VueMqtt")
window.Vue.use(VueMqtt, 'mqtts://test.mosquitto.org:8081')


class App(VueComponent):
    loading = 0

    template = """
    <el-container>
        <el-main>
            <dbw-progress></dbw-progress>
        </el-main>
    </el-container>
    """

    def publish_loading(self):
        if self.loading < 100:
            self.loading += 1
        else:
            self.loading = 0
        self.mqtt.publish(LOADING_TOPIC, str(self.loading))

    def created(self):
        timer.set_interval(lambda: self.publish_loading(), 100)


app = App("#app")
