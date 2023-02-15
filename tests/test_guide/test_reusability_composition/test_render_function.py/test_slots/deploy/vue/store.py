from browser import window
from .transformers import Transformable, VueStoreTransformer
from .bridge import Object
from .bridge.vuex_instance import VuexInstance


class VueStore(Transformable):
    @classmethod
    def init_dict(cls):
        return VueStoreTransformer.transform(cls)

    def __new__(cls):
        return Object.from_js(window.Vuex.Store.new(cls.init_dict()))


class VueStorePlugin:
    def initialize(self, store):
        raise NotImplementedError()

    def subscribe(self, state, mutation, *args, **kwargs):
        raise NotImplementedError()

    def __subscribe__(self, muation_info, state):
        self.subscribe(
            VuexInstance(state=state),
            muation_info["type"],
            *muation_info["payload"]["args"],
            **muation_info["payload"]["kwargs"],
        )

    def install(self, store):
        self.initialize(
            VuexInstance(
                state=store.state,
                getters=store.getters,
                commit=store.commit,
                dispatch=store.dispatch,
            )
        )
        store.subscribe(self.__subscribe__)
