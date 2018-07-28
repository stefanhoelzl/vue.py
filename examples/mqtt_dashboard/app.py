import random

from browser import timer

from vue import VueComponent, Vue
from components import *

from vue.utils import js_lib


VueMqtt = js_lib("VueMqtt")
Vue.use(VueMqtt, 'mqtts://test.mosquitto.org:8081')


class App(VueComponent):
    loading = 0
    temperature = 22

    template = """
    <el-container>
        <el-main>
            <dbw-progress topic="vuepy/loading"></dbw-progress>
            <dbw-bar topic="vuepy/temperature"></dbw-bar>
            <dbw-button topic="vuepy/window"></dbw-button>
        </el-main>
    </el-container>
    """

    def publish_loading(self):
        if self.loading < 100:
            self.loading += 1
        else:
            self.loading = 0
        self.mqtt.publish("vuepy/loading", str(self.loading))

    def publish_temperature(self):
        self.temperature += random.randint(-1, 1)
        self.mqtt.publish("vuepy/temperature", str(self.temperature))

    def created(self):
        timer.set_interval(lambda: self.publish_loading(), 100)
        timer.set_interval(lambda: self.publish_temperature(), 1000)


app = App("#app")
