from vue import VueComponent, watch, computed


def mqtt_match(flt, topic):
    for f, t in zip(flt.split("/"), topic.split("/")):
        if f == "#":
            return True
        if f != "+" and f != t:
            return False
    return len(flt) == len(topic)


class Widget(VueComponent):
    topic: str = ""
    value = ""

    template = """
    <div>
       {}
    </div> 
    """


    @computed
    def int_value(self):
        try:
            return int(self.value)
        except ValueError:
            return 0

    @int_value.setter
    def int_value(self, value):
        self.mqtt.publish(self.topic, str(self.value))

    def subscribe(self):
        if self.topic:
            self.mqtt.subscribe(self.topic)

    @watch("topic")
    def topic_changed(self, new, old):
        self.subscribe()

    def created(self):
        self.subscribe()
        self.mqtt.on("message", self.on_message)

    def on_message(self, topic, message, packet):
        if mqtt_match(self.topic, topic):
            self.value = str(message)
