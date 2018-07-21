import json
import asyncio

from vue import VueComponent, filters, watch

from browser import window

url = 'https://api.github.com/repos/stefanhoelzl/vue.py/commits?per_page=10&sha={}'

if window.location.hash == "#testing":
    url = "data.json"


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

    @asyncio.coroutine
    def fetch_data(self):
        self.commits = []
        req = yield asyncio.HTTPRequest(url.format(self.current_branch))
        self.commits = json.loads(req.response)


App("#commits")
