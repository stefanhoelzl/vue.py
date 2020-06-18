import math

from vue import VueComponent, computed


stats = [
    {"label": "A", "value": 100},
    {"label": "B", "value": 100},
    {"label": "C", "value": 100},
    {"label": "D", "value": 100},
    {"label": "E", "value": 100},
    {"label": "F", "value": 100},
]


def value_to_point(value, index, total):
    x = 0
    y = -value * 0.8
    angle = math.pi * 2 / total * index
    cos = math.cos(angle)
    sin = math.sin(angle)
    tx = x * cos - y * sin + 100
    ty = x * sin + y * cos + 100
    return tx, ty


class AxisLabel(VueComponent):
    template = '<text :x="point[0]" :y="point[1]">{{stat.label}}</text>'

    stat: dict
    index: int
    total: int

    @computed
    def point(self):
        return value_to_point(+int(self.stat["value"]) + 10, self.index, self.total)


AxisLabel.register()


class Polygraph(VueComponent):
    template = "#polygraph-template"
    stats: list

    @computed
    def points(self):
        return " ".join(
            map(
                lambda e: ",".join(
                    str(p)
                    for p in value_to_point(int(e[1]["value"]), e[0], len(self.stats))
                ),
                enumerate(self.stats),
            )
        )


Polygraph.register()


class App(VueComponent):
    template = "#app-template"
    new_label = ""
    stats = stats

    @computed
    def disable_remove(self):
        return len(self.stats) <= 3

    def add(self, event):
        event.preventDefault()
        if self.new_label:
            self.stats.append({"label": self.new_label, "value": 100})
            self.new_label = ""

    def remove(self, stat):
        del self.stats[self.stats.index(stat)]


App("#app")
