from browser.local_storage import storage
from browser import window
import json
from vue import VueComponent, computed, filters, watch, directive
from vue.bridge import Object

STORAGE_KEY = "todos-vue.py"


class ToDoStorage:
    NEXT_UID = 0

    @classmethod
    def next_uid(cls):
        uid = cls.NEXT_UID
        cls.NEXT_UID += 1
        return uid

    @classmethod
    def fetch(cls):
        cls.NEXT_UID = 0
        todos = json.loads(storage.get(STORAGE_KEY, "[]"))
        return [{"id": cls.next_uid(), **todo} for todo in todos]

    @staticmethod
    def save(todos):
        storage[STORAGE_KEY] = json.dumps(todos)


class VisibilityFilters:
    def __new__(cls, visibility):
        try:
            return getattr(VisibilityFilters, visibility)
        except AttributeError:
            return False

    @staticmethod
    def all(todos):
        return [todo for todo in todos]

    @staticmethod
    def active(todos):
        return [todo for todo in todos if not todo.get("completed", False)]

    @staticmethod
    def completed(todos):
        return [todo for todo in todos if todo.get("completed", False)]


class App(VueComponent):
    template = "#app-template"
    todos = ToDoStorage.fetch()
    new_todo = ""
    edited_todo = None
    edit_cache = ""
    visibility = "all"

    @watch("todos", deep=True)
    def save_todos(self, new, old):
        ToDoStorage.save(Object.to_py(new))

    @computed
    def filtered_todos(self):
        return VisibilityFilters(self.visibility)(self.todos)

    @computed
    def remaining(self):
        return len(VisibilityFilters.active(self.todos))

    @computed
    def all_done(self):
        return self.remaining == 0

    @all_done.setter
    def all_done(self, value):
        for todo in self.todos:
            todo["completed"] = value

    @staticmethod
    @filters
    def pluralize(n):
        return "item" if n == 1 else "items"

    def add_todo(self, ev=None):
        value = self.new_todo.strip()
        if not value:
            return
        self.todos.append(
            {"id": ToDoStorage.next_uid(), "title": value, "completed": False}
        )
        self.new_todo = ""

    def remove_todo(self, todo):
        del self.todos[self.todos.index(todo)]

    def edit_todo(self, todo):
        self.edit_cache = todo["title"]
        self.edited_todo = todo

    def done_edit(self, todo):
        if not self.edited_todo:
            return

        self.edited_todo = None
        todo["title"] = todo["title"].strip()
        if not todo["title"]:
            self.remove_todo(todo)

    def cancel_edit(self, todo):
        self.edited_todo = None
        todo.title = self.edit_cache

    def remove_completed(self, ev=None):
        self.todos = VisibilityFilters.active(self.todos)

    @staticmethod
    @directive
    def todo_focus(el, binding, vnode, old_vnode, *args):
        if binding.value:
            el.focus()


app = App("#app")


def on_hash_change(ev):
    visibility = window.location.hash.replace("#", "").replace("/", "")
    if VisibilityFilters(visibility):
        app.visibility = visibility
    else:
        window.location.hash = ""
        app.visibility = "all"


window.bind("hashchange", on_hash_change)
