import json

from vue import VueComponent, filters, watch

from browser import window, ajax

url = "https://api.github.com/repos/stefanhoelzl/vue.py/commits?per_page=10&sha={}"

if window.location.hash == "#testing":
    url = "data.json"


class App(VueComponent):
    template = "#commits"

    branches = ["master", "2948e6b"]
    current_branch = "master"
    commits = []

    def created(self):
        self.fetch_data()

    @watch("current_branch")
    def fetch_data_on_current_branch_change(self, new, old):
        self.fetch_data()

    @staticmethod
    @filters
    def truncate(value):
        return value.split("\n", 1)[0]

    @staticmethod
    @filters
    def format_date(value):
        return value.replace("T", " ").replace("Z", "")

    def fetch_data(self):
        self.commits = []

        req = ajax.ajax()
        req.open("GET", url.format(self.current_branch), True)
        req.bind("complete", self.loaded)
        req.send()

    def loaded(self, ev):
        self.commits = json.loads(ev.text)


App("#app")
