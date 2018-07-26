from .base import VueDecorator


class Model(VueDecorator):
    __key__ = "model"

    def __init__(self, prop="value", event="input"):
        self.prop = prop
        self.event = event

    @property
    def __value__(self):
        return {
            "prop": self.prop,
            "event": self.event,
        }
