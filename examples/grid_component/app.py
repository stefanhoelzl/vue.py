from vue import VueComponent, data, computed, filters


class GridComponent(VueComponent):
    template = "#grid"

    content: list
    columns: list
    filter_key: str

    sort_key = ""

    @data
    def sort_orders(self):
        return {key: False for key in self.columns}

    @computed
    def filtered_data(self):
        return list(
            sorted(
                filter(
                    lambda f: self.filter_key.lower() in f["name"].lower(), self.content
                ),
                reverse=self.sort_orders.get(self.sort_key, False),
                key=lambda c: c.get(self.sort_key, self.columns[0]),
            )
        )

    @staticmethod
    @filters
    def capitalize(value):
        return value.capitalize()

    def sort_by(self, key):
        self.sort_key = key
        self.sort_orders[key] = not self.sort_orders[key]


GridComponent.register("demo-grid")


class App(VueComponent):
    template = "#form"

    search_query = ""
    grid_columns = ["name", "power"]
    grid_data = [
        {"name": "Chuck Norris", "power": float("inf")},
        {"name": "Bruce Lee", "power": 9000},
        {"name": "Jackie Chan", "power": 7000},
        {"name": "Jet Li", "power": 8000},
    ]


App("#app")
