from .object import Object
from .vuex_instance import VuexInstance


class VueInstance(Object):
    @staticmethod
    def __can_wrap__(obj):
        return hasattr(obj, "_isVue") and obj._isVue

    @property
    def store(self):
        store = self.__getattr__("store")
        return VuexInstance(state=store.state,
                            getters=store.getters,
                            commit=store.commit,
                            dispatch=store.dispatch)

    def __getattr__(self, item):
        try:
            return Object.from_js(getattr(self._js, item))
        except AttributeError:
            if not item.startswith("$"):
                return self.__getattr__("${}".format(item))
            raise

    def __setattr__(self, key, value):
        if key in ["_js"]:
            object.__setattr__(self, key, value)
        elif hasattr(getattr(self, key), "__set__"):
            getattr(self, key).__set__(value)
        else:
            if key not in dir(getattr(self._js, "$props", [])):
                setattr(self._js, key, value)


Object.SubClasses.append(VueInstance)
