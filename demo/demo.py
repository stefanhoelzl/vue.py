from vue import VueComponent, Data, method, Property


class TodoItem(VueComponent):
    todo = Property()

    template = """
    <li>
        <input type="checkbox" v-model="todo.done"></input>
        <s v-if="todo.done">{{ todo.text }}</s>
        <span v-else>{{ todo.text }}</span>
    </li>
    """
TodoItem.register()


class DemoApp(VueComponent):
    new_todo = Data("")
    todos = Data([{"id": 1, "text": "Like Vue.js", "done": True},
                  {"id": 0, "text": "Try out vue.py", "done": False}])
    next_id = Data(len(todos.value))

    @method
    def add(self, event):
        self.todos.push({"id": self.next_id, "text":  self.new_todo})
        self.new_todo = ""
        self.next_id += 1

    template = """
    <div>
        <input type="text" placeholder="new todo" v-model="new_todo"></input>
        <button @click="add">add</button>
        <ol>
            <todo-item v-for="todo in todos" :todo="todo" :key="todo.id">
            </todo-item>
        </ol>
    </div>
    """


DemoApp("#app")
