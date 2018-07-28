from .widget import Widget


class Progress(Widget):
    topic: str = ""

    template = Widget.template.format("""
    <el-progress type="circle" :percentage="int_value"></el-progress>
    """)


Progress.register("dbw-progress")
