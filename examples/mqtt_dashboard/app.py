import random

from browser import timer

from vue import VueComponent
from vue.bridge import Object

from vue.utils import js_lib


TEMP_TOPIC = "vuepytemperature"
LOADING_TOPIC = "vuepyloading"
WINDOW_TOPIC = "vuepywindow"

mqtt = js_lib("mqtt")
client = mqtt.connect('mqtt://test.mosquitto.org:8080')


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

    def created(self):
        client.on("message", self.on_messsage)
        client.subscribe(LOADING_TOPIC)
        client.subscribe(TEMP_TOPIC)
        client.subscribe(WINDOW_TOPIC)

    def on_messsage(self, topic, message, packet):
        val = Object.to_js(message).toString()
        if topic == LOADING_TOPIC:
            self.loading = int(val)
        elif topic == TEMP_TOPIC:
            self.temperature = int(val)
        elif topic == WINDOW_TOPIC:
            self.window_open = bool(int(val))

    def tgl_window(self, ev=None):
        client.publish(WINDOW_TOPIC, str(int(not self.window_open)))


app = App("#app")


def loading():
    val = app.loading
    if val < 100:
        val += 1
    else:
        val = 0
    client.publish(LOADING_TOPIC, str(val))


def temperature():
    val = app.temperature
    val += random.randint(-1, 1)
    client.publish(TEMP_TOPIC, str(val))


timer.set_interval(loading, 100)
timer.set_interval(temperature, 1000)
