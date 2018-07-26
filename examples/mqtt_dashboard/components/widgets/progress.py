from vue import computed
from .widget import Widget


class Progress(Widget):
    template = Widget.template.format("""
    <el-progress type="circle" :percentage="loading"></el-progress>
    """)

    @computed
    def loading(self):
        try:
            return int(self.value)
        except ValueError:
            return 0


Progress.register("dbw-progress")
