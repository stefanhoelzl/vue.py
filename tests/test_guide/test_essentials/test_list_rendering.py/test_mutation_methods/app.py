from vue import *


class MutationMethods(VueComponent):
    array = [1, 2, 3]

    template = "<div id='done' />"

    def created(self):
        print(self.array)  # 1,2,3
        print(self.array.pop())  # 3
        print(self.array)  # 1,2
        self.array.append(4)
        print(self.array)  # 1,2,4
        print(self.array.pop(0))  # 1
        print(self.array)  # 2,4
        self.array[0:0] = [6, 4]
        print(self.array)  # 6,4,2,4
        self.array.insert(2, 8)
        print(self.array)  # 6,4,8,2,4
        del self.array[3]
        print(self.array)  # 6,4,8,4
        self.array.sort(key=lambda a: 0 - a)
        print(self.array)  # 8,6,4,4
        self.array.reverse()
        print(self.array)  # 4,4,6,8


app = MutationMethods("#app")
