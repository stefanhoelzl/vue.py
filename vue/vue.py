from browser import window


class Vue:
    def __init__(self, app_id, **data):
        window.Vue.new({
            "el": app_id,
            "data": data
        })
