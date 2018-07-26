from vue import VueComponent, watch


class Widget(VueComponent):
    topic: str = None
    value = ""
    template = """
    <div>
       {}
    </div> 
    """

    @watch("topic")
    def topic_changed(self, new, old):
        self.mqtt.subscribe(new)

    def created(self):
        self.mqtt.on("message", self.on_message)
        self.topic = "vuepy/loading"

    def on_message(self, topic, message, packet):
        self.value = str(message)
