from .__version__ import __version__

try:
    from .vue import VueComponent, VueMixin, Vue, VueDirective, VuePlugin
    from .store import VueStore, VueStorePlugin
    from .router import VueRouter, VueRoute
    from .decorators import computed, validator, directive, filters, watch, \
        data, Model, custom, mutation, action, getter
except ModuleNotFoundError:
    pass
