import random

from browser import timer, window

from vue import VueComponent, custom

from vue.utils import js_lib


TEMP_TOPIC = "vuepy/temperature"
LOADING_TOPIC = "vuepy/loading"
WINDOW_TOPIC = "vuepy/window"

VueMqtt = js_lib("VueMqtt")
window.Vue.use(VueMqtt, 'mqtts://test.mosquitto.org:8081')


class App(VueComponent):
    loading = 50
    temperature = 22
    window_open = True

    template = """
    <el-container>
        <el-main>
            <el-progress type="circle" :percentage="loading"></el-progress>
            <el-slider 
                :min="0"
                :max="40"
                show-input
                :show-input-controls="false"
                v-model="temperature" 
                disabled>
            </el-slider>
            
            <el-button type="success" @click="tgl_window" round 
                id="btn"
                v-if="window_open">
                OPEN
            </el-button>
            <el-button type="primary" @click="tgl_window" round 
                id="btn"
                v-else>
                CLOSED
            </el-button>
        </el-main>
    </el-container>
    """

    def publish_loading(self):
        val = self.loading
        if val < 100:
            val += 1
        else:
            val = 0
        self.mqtt.publish(LOADING_TOPIC, str(val))

    def publish_temperature(self):
        val = self.temperature
        val += random.randint(-1, 1)
        self.mqtt.publish(TEMP_TOPIC, str(val))

    def created(self):
        self.mqtt.subscribe(LOADING_TOPIC)
        self.mqtt.subscribe(TEMP_TOPIC)
        self.mqtt.subscribe(WINDOW_TOPIC)
        timer.set_interval(lambda: self.publish_loading(), 100)
        timer.set_interval(lambda: self.publish_temperature(), 1000)

    @custom("mqtt", name=LOADING_TOPIC)
    def on_loading_changed(self, data, topic):
        self.loading = int(str(data))

    @custom("mqtt", name=TEMP_TOPIC)
    def on_temperature_changed(self, data, topic):
        self.temperature = int(str(data))

    @custom("mqtt", name=WINDOW_TOPIC)
    def on_window_open_changed(self, data, topic):
        self.window_open = bool(int(str(data)))

    def tgl_window(self, ev=None):
        self.mqtt.publish(WINDOW_TOPIC, str(int(not self.window_open)))


app = App("#app")
