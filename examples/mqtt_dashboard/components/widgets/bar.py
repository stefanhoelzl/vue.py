from vue import computed
from .widget import Widget


class Bar(Widget):
    topic: str = ""

    template = Widget.template.format("""
    <el-slider 
        :min="0"
        :max="40"
        show-input
        :show-input-controls="false"
        v-model="int_value" 
        disabled>
    </el-slider>
    """)


Bar.register("dbw-bar")
