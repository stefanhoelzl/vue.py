from vue import VueComponent, data, computed
from vue.bridge import Object
from vue.utils import js_lib


dynamics = js_lib("dynamics")


class DraggableHeaderView(VueComponent):
    template = "#header-view"

    dragging = False

    @data
    def c(self):
        return {"x": 160, "y": 160}

    @data
    def start(self):
        return {"x": 0, "y": 0}

    @computed
    def header_path(self):
        return f'M0,0 L320,0 320,160Q{self.c["x"]},{self.c["y"]} 0,160'

    @computed
    def content_position(self):
        dy = self.c["y"] - 160
        dampen = 2 if dy > 0 else 4
        return {"transform": f"translate3d(0,{dy / dampen}px,0)"}

    def start_drag(self, e):
        e = e["changedTouches"][0] if "changedTouches" in e else e
        self.dragging = True
        self.start["x"] = e.pageX
        self.start["y"] = e.pageY

    def on_drag(self, e):
        e = e["changedTouches"][0] if "changedTouches" in e else e
        if self.dragging:
            self.c["x"] = 160 + (e.pageX - self.start["x"])
            dy = e.pageY - self.start["y"]
            dampen = 1.5 if dy > 0 else 4
            self.c["y"] = int(160 + dy / dampen)

    def stop_drag(self, _):
        if self.dragging:
            self.dragging = False
            dynamics.animate(
                Object.to_js(self.c),
                {"x": 160, "y": 160},
                {"type": dynamics.spring, "duration": 700, "friction": 280},
            )


DraggableHeaderView.register()


class App(VueComponent):
    template = "#main"


App("#app")
