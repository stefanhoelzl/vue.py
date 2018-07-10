from vue import *


def test_mutation_methods(selenium):
    class MutationMethods(VueComponent):
        array = Data([1, 2, 3])

        @method
        def log_array(self):
            print(",".join(str(self.array[i]) for i in range(len(self.array))))

        def created(self):
            cmp = lambda a,b: b-a
            self.log_array()                   # 1,2,3
            print(self.array.pop())            # 3
            self.log_array()                   # 1,2
            print(self.array.push(4))          # 3
            self.log_array()                   # 1,2,4
            print(self.array.shift())          # 1
            self.log_array()                   # 2,4
            print(self.array.unshift(6, 4))    # 4
            self.log_array()                   # 6,4,2,4
            print(self.array.splice(2, 1, 8))  # [2]
            self.log_array()                   # 6,4,8,4
            self.array.sort(cmp)
            self.log_array()                   # 8,6,4,4
            self.array.reverse()
            self.log_array()                   # 4,4,6,8

    with selenium.app(MutationMethods):
        logs = [l['message'].split(" ")[-1][:-3][1:]
                for l in selenium.get_logs()[-13:]]
        assert logs == ["1,2,3",
                        "3",
                        "1,2",
                        "3",
                        "1,2,4",
                        "1",
                        "2,4",
                        "4",
                        "6,4,2,4",
                        "[2]",
                        "6,4,8,4",
                        "8,6,4,4",
                        "4,4,6,8"]
