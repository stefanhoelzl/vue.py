class VuexInstance:
    def __init__(self,
                 state=None, getters=None,
                 root_state=None, root_getters=None,
                 commit=None, dispatch=None):
        self.__state__ = state if state else {}
        self.__getter__ = getters
        self.__root_getter__ = root_getters
        self.__root_state__ = root_state if root_state else {}
        self.__commit__ = commit
        self.__dispatch__ = dispatch

    def __getattr__(self, item):
        item = item.replace("$", "")
        if item in ["__state__", "__root_state__"]:
            return {}
        if item in self.__state__:
            return self.__state__[item]
        if hasattr(self.__getter__, item):
            return getattr(self.__getter__, item)
        if item in self.__root_state__:
            return self.__root_state__[item]
        if hasattr(self.__root_getter__, item):
            return getattr(self.__root_getter__, item)
        return super().__getattribute__(item)

    def __setattr__(self, key, value):
        key = key.replace("$", "")
        if key in self.__state__:
            self.__state__[key] = value
        elif key in self.__root_state__:
            self.__root_state__[key] = value
        else:
            super().__setattr__(key, value)

    def commit(self, mutation_name, *args, **kwargs):
        self.__commit__(mutation_name, {"args": args, "kwargs": kwargs})

    def dispatch(self, mutation_name, *args, **kwargs):
        self.__dispatch__(mutation_name, {"args": args, "kwargs": kwargs})
