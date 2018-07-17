import json
from browser import ajax
from vue import VueComponent, filters, watch


url = 'https://api.github.com/repos/stefanhoelzl/vue.py/commits?per_page=10&sha={}'


class App(VueComponent):
    branches = ['master', '2948e6b']
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
        def update_commits(r):
            self.commits = json.loads(r.text)

        self.commits = []
        req = ajax.ajax()
        req.bind('complete', update_commits)
        req.open('GET', url.format(self.current_branch), True)
        req.send()


App("#commits")
