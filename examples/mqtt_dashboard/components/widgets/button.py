from vue import computed
from .widget import Widget


class Button(Widget):
    topic: str = ""

    states = {
        "open": {"type": "success", "text": "OPEN", "publish": "closed"},
        "closed": {"type": "primary", "text": "CLOSED", "publish": "open"},
    }
    default_state = states["open"]

    template = Widget.template.format("""
    <el-button 
        :type="current_state.type" 
        @click="click" 
        :disabled="current_state.disabled"
        round>
        {{ current_state.text }}
    </el-button>
    """)

    @computed
    def current_state(self):
        return self.states.get(self.value, self.default_state)

    def click(self, ev):
        self.mqtt.publish(self.topic, self.current_state["publish"])


Button.register("dbw-button")
