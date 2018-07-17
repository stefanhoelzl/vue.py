from vue import VueComponent, data, computed, filters


class GridComponent(VueComponent):
    content: list
    columns: list
    filter_key: str

    template = "#grid-template"

    @data
    def sort_key(self):
        return self.columns[0]

    @data
    def sort_orders(self):
        return {key: False for key in self.columns}

    @computed
    def filtered_data(self):
        return list(
            sorted(
                filter(lambda f: self.filter_key.lower() in f['name'].lower(),
                       self.content),
                reverse=self.sort_orders[self.sort_key],
                key=lambda c: c[self.sort_key]
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
    search_query = ""
    grid_columns = ["name", "power"]
    grid_data = [
      {"name": 'Chuck Norris', "power": float('inf')},
      {"name": 'Bruce Lee', "power": 9000},
      {"name": 'Jackie Chan', "power": 7000},
      {"name": 'Jet Li', "power": 8000}
    ]


App("#demo")
