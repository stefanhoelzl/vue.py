__BRYTHON__.use_VFS = true;
var scripts = {"$timestamp": 1613426335769, "__entry_point__": [".py", "import app\n", ["app"]], "app": [".py", "from vue import VueComponent,data,computed,filters\n\n\nclass GridComponent(VueComponent):\n template=\"#grid\"\n \n content:list\n columns:list\n filter_key:str\n \n sort_key=\"\"\n \n @data\n def sort_orders(self):\n  return {key:False for key in self.columns}\n  \n @computed\n def filtered_data(self):\n  return list(\n  sorted(\n  filter(\n  lambda f:self.filter_key.lower()in f[\"name\"].lower(),self.content\n  ),\n  reverse=self.sort_orders.get(self.sort_key,False ),\n  key=lambda c:c.get(self.sort_key,self.columns[0]),\n  )\n  )\n  \n @staticmethod\n @filters\n def capitalize(value):\n  return value.capitalize()\n  \n def sort_by(self,key):\n  self.sort_key=key\n  self.sort_orders[key]=not self.sort_orders[key]\n  \n  \nGridComponent.register(\"demo-grid\")\n\n\nclass App(VueComponent):\n template=\"#form\"\n \n search_query=\"\"\n grid_columns=[\"name\",\"power\"]\n grid_data=[\n {\"name\":\"Chuck Norris\",\"power\":float(\"inf\")},\n {\"name\":\"Bruce Lee\",\"power\":9000},\n {\"name\":\"Jackie Chan\",\"power\":7000},\n {\"name\":\"Jet Li\",\"power\":8000},\n ]\n \n \nApp(\"#app\")\n", ["vue"]], "vue.router": [".py", "from browser import window\nfrom .factory import Wrapper,VueRouterFactory\n\n\nclass VueRouter(Wrapper):\n RouterClass=None\n \n @classmethod\n def init_dict(cls):\n  return VueRouterFactory.get_item(cls)\n  \n def __new__(cls):\n  router_class=cls.RouterClass or window.VueRouter\n  return router_class.new(cls.init_dict())\n  \n  \nclass VueRoute:\n def __new__(cls,path,component=None ,components=None ,**kwargs):\n  route={\"path\":path,**kwargs}\n  \n  if component is not None :\n   route[\"component\"]=component.init_dict()\n  elif components is not None :\n   route[\"components\"]={\n   name:component.init_dict()for name,component in components.items()\n   }\n   \n  return route\n", ["browser", "vue.factory"]], "vue.__version__": [".py", "__version__=\"0.3.0\"\n", []], "vue": [".py", "from .__version__ import __version__\n\ntry :\n from .vue import VueComponent,VueMixin,Vue,VueDirective,VuePlugin\n from .store import VueStore,VueStorePlugin\n from .router import VueRouter,VueRoute\n from .decorators import (\n computed,\n validator,\n directive,\n filters,\n watch,\n data,\n Model,\n custom,\n mutation,\n action,\n getter,\n )\nexcept ModuleNotFoundError:\n pass\n", ["vue.__version__", "vue.decorators", "vue.decorators.action", "vue.decorators.computed", "vue.decorators.custom", "vue.decorators.data", "vue.decorators.directive", "vue.decorators.filters", "vue.decorators.getter", "vue.decorators.mutation", "vue.router", "vue.store", "vue.vue"], 1], "vue.store": [".py", "from browser import window\nfrom .factory import Wrapper,VueStoreFactory\nfrom .bridge import Object\nfrom .bridge.vuex_instance import VuexInstance\n\n\nclass VueStore(Wrapper):\n @classmethod\n def init_dict(cls):\n  return VueStoreFactory.get_item(cls)\n  \n def __new__(cls):\n  return Object.from_js(window.Vuex.Store.new(cls.init_dict()))\n  \n  \nclass VueStorePlugin:\n def initialize(self,store):\n  raise NotImplementedError()\n  \n def subscribe(self,state,mutation,*args,**kwargs):\n  raise NotImplementedError()\n  \n def __subscribe__(self,muation_info,state):\n  self.subscribe(\n  VuexInstance(state=state),\n  muation_info[\"type\"],\n  *muation_info[\"payload\"][\"args\"],\n  **muation_info[\"payload\"][\"kwargs\"],\n  )\n  \n def install(self,store):\n  self.initialize(\n  VuexInstance(\n  state=store.state,\n  getters=store.getters,\n  commit=store.commit,\n  dispatch=store.dispatch,\n  )\n  )\n  store.subscribe(self.__subscribe__)\n", ["browser", "vue.bridge", "vue.bridge.vuex_instance", "vue.factory"]], "vue.utils": [".py", "from browser import window,load\n\nCACHE={}\n\n\ndef js_load(path):\n if path in CACHE:\n  return CACHE[path]\n before=dir(window)\n load(path)\n after=dir(window)\n diff=set(after)-set(before)\n mods={module:getattr(window,module)for module in diff if \"$\"not in module}\n if len(mods)==0:\n  mods=None\n elif len(mods)==1:\n  mods=mods.popitem()[1]\n CACHE[path]=mods\n return mods\n \n \ndef js_lib(name):\n attr=getattr(window,name)\n if dir(attr)==[\"default\"]:\n  return attr.default\n return attr\n", ["browser"]], "vue.vue": [".py", "from browser import window\nfrom .factory import VueComponentFactory,Wrapper,VueDirectiveFactory\nfrom .bridge import Object\nfrom .decorators.directive import DirectiveHook\nfrom .decorators.filters import Filter\n\n\nclass Vue:\n @staticmethod\n def directive(name,directive=None ):\n  if directive is None and isinstance(name,str):\n   return window.Vue.directive(name)\n   \n  if directive is None :\n   directive=name\n   name=directive.__name__.lower()\n   \n  if not isinstance(directive,type):\n  \n   class FunctionDirective(VueDirective):\n    d=DirectiveHook(directive)\n    \n   directive=FunctionDirective\n   \n  window.Vue.directive(name,VueDirectiveFactory.get_item(directive))\n  \n @staticmethod\n def filter(method_or_name,method=None ):\n  if not method:\n   method=method_or_name\n   name=method_or_name.__name__\n  else :\n   method=method\n   name=method_or_name\n  flt=Filter(method,name)\n  window.Vue.filter(flt.__id__,flt.__value__)\n  \n @staticmethod\n def mixin(mixin):\n  window.Vue.mixin(VueComponentFactory.get_item(mixin))\n  \n @staticmethod\n def use(plugin,*args,**kwargs):\n  window.Vue.use(plugin,*args,kwargs)\n  \n @staticmethod\n def component(component_or_name,component=None ):\n  if isinstance(component_or_name,str)and component is None :\n   return window.Vue.component(component_or_name)\n  if component is not None :\n   name=component_or_name\n  else :\n   component=component_or_name\n   name=component.__name__\n  window.Vue.component(name,VueComponentFactory.get_item(component))\n  \n  \nclass VueComponent(Wrapper):\n @classmethod\n def init_dict(cls):\n  return VueComponentFactory.get_item(cls)\n  \n def __new__(cls,el,**kwargs):\n  init_dict=cls.init_dict()\n  init_dict.update(el=el)\n  for key,value in kwargs.items():\n   if key ==\"props_data\":\n    key=\"propsData\"\n   init_dict.update({key:value})\n  return Object.from_js(window.Vue.new(Object.to_js(init_dict)))\n  \n @classmethod\n def register(cls,name=None ):\n  if name:\n   Vue.component(name,cls)\n  else :\n   Vue.component(cls)\n   \n   \nclass VueMixin(Wrapper):\n pass\n \n \nclass VueDirective(Wrapper):\n name=None\n \n \nclass VuePlugin:\n @staticmethod\n def install(*args,**kwargs):\n  raise NotImplementedError()\n", ["browser", "vue.bridge", "vue.decorators.directive", "vue.decorators.filters", "vue.factory"]], "vue.factory": [".py", "from .decorators.base import VueDecorator\nfrom .decorators.prop import Prop\nfrom .decorators.data import Data\nfrom .decorators.lifecycle_hook import LifecycleHook\nfrom .decorators.method import Method\nfrom .decorators.render import Render\nfrom .decorators.mixins import Mixins\nfrom .decorators.template import Template\nfrom .decorators.directive import DirectiveHook\nfrom .decorators.extends import Extends\nfrom .decorators.components import Components\nfrom .decorators.state import State\nfrom .decorators.plugin import Plugin\nfrom .decorators.routes import Routes\n\n\ndef merge_templates(sub):\n def get_template_slots(cls):\n  template_slots=getattr(cls,\"template_slots\",{})\n  if isinstance(template_slots,str):\n   template_slots={\"default\":template_slots}\n  return template_slots\n  \n base=sub.__base__\n template_merging=hasattr(base,\"template\")and getattr(\n sub,\"template_slots\",False\n )\n if template_merging:\n  base_template=merge_templates(base)\n  base_slots=get_template_slots(base)\n  sub_slots=get_template_slots(sub)\n  slots=dict(tuple(base_slots.items())+tuple(sub_slots.items()))\n  default=slots.get(\"default\")\n  return base_template.format(default,**slots)\n return getattr(sub,\"template\",\"{}\")\n \n \nclass BrythonObjectWorkarounds(type):\n ''\n\n\n \n \n @property\n def __base__(cls):\n  return cls.__bases__[0]\n  \n  \nclass Wrapper(metaclass=BrythonObjectWorkarounds):\n pass\n \n \nclass AttributeDictFactory:\n @classmethod\n def get_item(cls,wrapper):\n  if isinstance(wrapper,BrythonObjectWorkarounds):\n   return cls(wrapper).generate_item()\n  return wrapper\n  \n @classmethod\n def get_wrapper_base(cls,wrapper):\n  base=wrapper.__base__\n  if base is Wrapper:\n   return wrapper\n  return cls.get_wrapper_base(base)\n  \n def __init__(self,wrapper):\n  self.wrapper=wrapper\n  self.base=self.get_wrapper_base(wrapper)\n  \n def __attributes__(self):\n  all_objects=set(dir(self.wrapper))\n  all_objects.update(getattr(self.wrapper,\"__annotations__\",{}).keys())\n  own_objects=all_objects -set(dir(self.base))-{\"__annotations__\"}\n  for obj_name in own_objects:\n   yield obj_name,getattr(self.wrapper,obj_name,None )\n   \n def auto_decorate(self,obj_name,obj):\n  return obj\n  \n def generate_item(self):\n  object_map={}\n  for obj_name,obj in self.__attributes__():\n   obj=self.auto_decorate(obj_name,obj)\n   if isinstance(obj,VueDecorator):\n    obj.update(object_map)\n  return object_map\n  \n  \nclass VueComponentFactory(AttributeDictFactory):\n def _property_mixin(self,prop_name):\n  if prop_name not in dir(self.wrapper):\n   return {\"required\":True }\n  else :\n   return {\"default\":getattr(self.wrapper,prop_name)}\n   \n def auto_decorate(self,obj_name,obj):\n  if obj_name in LifecycleHook.mapping:\n   obj=LifecycleHook(obj_name,obj)\n  elif obj_name ==\"template\":\n   obj=Template(merge_templates(self.wrapper))\n  elif obj_name ==\"extends\":\n   if obj:\n    extends=self.wrapper.__base__ if isinstance(obj,bool)else obj\n    obj=Extends(VueComponentFactory.get_item(extends))\n  elif obj_name ==\"mixins\":\n   obj=Mixins(*(VueComponentFactory.get_item(m)for m in obj))\n  elif obj_name ==\"components\":\n   obj=Components(*(VueComponentFactory.get_item(m)for m in obj))\n  elif obj_name ==\"render\":\n   obj=Render(obj)\n  elif callable(obj):\n   obj=Method(obj)\n  elif obj_name in getattr(self.wrapper,\"__annotations__\",{}):\n   obj=Prop(\n   obj_name,\n   self.wrapper.__annotations__[obj_name],\n   self._property_mixin(obj_name),\n   )\n  elif not isinstance(obj,VueDecorator):\n   obj=Data(obj_name,obj)\n  return super().auto_decorate(obj_name,obj)\n  \n def generate_item(self):\n  init_dict=super().generate_item()\n  _data=init_dict.get(\"data\",None )\n  \n  if not _data:\n   return init_dict\n   \n  def get_initialized_data(this):\n   initialized_data={}\n   for name,date in _data.items():\n    initialized_data[name]=date(this)if callable(date)else date\n   return initialized_data\n   \n  init_dict.update(data=get_initialized_data)\n  return init_dict\n  \n  \nclass VueDirectiveFactory(AttributeDictFactory):\n def auto_decorate(self,obj_name,obj):\n  if callable(obj):\n   obj=DirectiveHook(obj,hooks=(obj_name,),name=self.wrapper.name)\n  return super().auto_decorate(obj_name,obj)\n  \n @classmethod\n def get_item(cls,wrapper):\n  default={wrapper.name:{}}\n  dct=super().get_item(wrapper)\n  return dct.get(\"directives\",default).popitem()[1]\n  \n  \nclass VueStoreFactory(AttributeDictFactory):\n def auto_decorate(self,obj_name,obj):\n  if obj_name ==\"plugins\":\n   obj=Plugin(obj)\n  elif not isinstance(obj,VueDecorator):\n   obj=State(obj_name,obj)\n  return super().auto_decorate(obj_name,obj)\n  \n  \nclass VueRouterFactory(AttributeDictFactory):\n def auto_decorate(self,obj_name,obj):\n  if obj_name ==\"routes\":\n   obj=Routes(obj)\n  return super().auto_decorate(obj_name,obj)\n", ["vue.decorators.base", "vue.decorators.components", "vue.decorators.data", "vue.decorators.directive", "vue.decorators.extends", "vue.decorators.lifecycle_hook", "vue.decorators.method", "vue.decorators.mixins", "vue.decorators.plugin", "vue.decorators.prop", "vue.decorators.render", "vue.decorators.routes", "vue.decorators.state", "vue.decorators.template"]], "vue.decorators.getter": [".py", "from .base import pyjs_bridge,VueDecorator\nfrom vue.bridge import VuexInstance\n\n\nclass Getter(VueDecorator):\n __key__=\"getters\"\n \n def __init__(self,name,value):\n  self.__id__=name\n  self.__value__=value\n  \n  \ndef getter(fn):\n def wrapper(state,getters,*args):\n  if fn.__code__.co_argcount ==1:\n   return fn(VuexInstance(state=state,getters=getters))\n  else :\n  \n   def getter_method(*args_,**kwargs):\n    return fn(VuexInstance(state=state,getters=getters),*args_,**kwargs)\n    \n   return getter_method\n   \n return Getter(fn.__name__,pyjs_bridge(wrapper))\n", ["vue.bridge", "vue.decorators.base"]], "vue.decorators.prop": [".py", "from browser import window\nfrom .base import pyjs_bridge,VueDecorator\n\n\nclass Prop(VueDecorator):\n __key__=\"props\"\n \n type_map={\n int:window.Number,\n float:window.Number,\n str:window.String,\n bool:window.Boolean,\n list:window.Array,\n object:window.Object,\n dict:window.Object,\n None :None ,\n }\n \n def __init__(self,name,typ,mixin=None ):\n  mixin=mixin if mixin else {}\n  self.__id__=name\n  self.__value__={\"type\":self.type_map[typ],**mixin}\n  \n  \nclass Validator(VueDecorator):\n __parents__=(\"props\",)\n __id__=\"validator\"\n \n def __init__(self,prop,fn):\n  self.__key__=prop\n  self.__value__=pyjs_bridge(fn,inject_vue_instance=True )\n  \n  \ndef validator(prop):\n def decorator(fn):\n  return Validator(prop,fn)\n  \n return decorator\n", ["browser", "vue.decorators.base"]], "vue.decorators": [".py", "from .computed import computed\nfrom .prop import validator\nfrom .directive import directive,DirectiveHook\nfrom .filters import filters\nfrom .watcher import watch\nfrom .data import data\nfrom .model import Model\nfrom .custom import custom\nfrom .mutation import mutation\nfrom .action import action\nfrom .getter import getter\n", ["vue.decorators.action", "vue.decorators.computed", "vue.decorators.custom", "vue.decorators.data", "vue.decorators.directive", "vue.decorators.filters", "vue.decorators.getter", "vue.decorators.model", "vue.decorators.mutation", "vue.decorators.prop", "vue.decorators.watcher"], 1], "vue.decorators.extends": [".py", "from .base import VueDecorator\n\n\nclass Extends(VueDecorator):\n __key__=\"extends\"\n \n def __init__(self,init_dict):\n  self.__value__=init_dict\n", ["vue.decorators.base"]], "vue.decorators.filters": [".py", "from .base import pyjs_bridge,VueDecorator\n\n\nclass Filter(VueDecorator):\n __key__=\"filters\"\n \n def __init__(self,fn,name):\n  self.__value__=pyjs_bridge(fn)\n  self.__id__=name\n  \n  \ndef filters(fn):\n return Filter(fn,fn.__name__)\n", ["vue.decorators.base"]], "vue.decorators.base": [".py", "from vue.bridge import Object\nimport javascript\n\n\nclass VueDecorator:\n __key__=None\n __parents__=()\n __id__=None\n __value__=None\n \n def update(self,vue_dict):\n  base=vue_dict\n  for parent in self.__parents__:\n   base=vue_dict.setdefault(parent,{})\n   \n  if self.__id__ is None :\n   base[self.__key__]=self.__value__\n  else :\n   base=base.setdefault(self.__key__,{})\n   value=self.__value__\n   if isinstance(base.get(self.__id__),dict):\n    base[self.__id__].update(value)\n   else :\n    base[self.__id__]=value\n    \n    \ndef pyjs_bridge(fn,inject_vue_instance=False ):\n def wrapper(*args,**kwargs):\n  args=(javascript.this(),*args)if inject_vue_instance else args\n  args=tuple(Object.from_js(arg)for arg in args)\n  kwargs={k:Object.from_js(v)for k,v in kwargs.items()}\n  return Object.to_js(fn(*args,**kwargs))\n  \n wrapper.__name__=fn.__name__\n return wrapper\n", ["javascript", "vue.bridge"]], "vue.decorators.action": [".py", "from .base import pyjs_bridge,VueDecorator\nfrom vue.bridge import VuexInstance\n\n\nclass Action(VueDecorator):\n __key__=\"actions\"\n \n def __init__(self,name,value):\n  self.__id__=name\n  self.__value__=value\n  \n  \ndef action(fn):\n def wrapper(context,*payload):\n  payload=payload[0]if payload else {\"args\":(),\"kwargs\":{}}\n  return fn(\n  VuexInstance(\n  state=context.state,\n  getters=context.getters,\n  root_state=context.rootState,\n  root_getters=context.rootGetters,\n  commit=context.commit,\n  dispatch=context.dispatch,\n  ),\n  *payload.get(\"args\",()),\n  **payload.get(\"kwargs\",{}),\n  )\n  \n return Action(fn.__name__,pyjs_bridge(wrapper))\n", ["vue.bridge", "vue.decorators.base"]], "vue.decorators.plugin": [".py", "from .base import VueDecorator\n\n\nclass Plugin(VueDecorator):\n __key__=\"plugins\"\n \n def __init__(self,plugins):\n  self.__value__=list(plugins)\n", ["vue.decorators.base"]], "vue.decorators.directive": [".py", "from .base import pyjs_bridge,VueDecorator\n\n\ndef map_hook(hook_name):\n if hook_name ==\"component_updated\":\n  return \"componentUpdated\"\n return hook_name\n \n \nclass DirectiveHook(VueDecorator):\n def __init__(self,fn,hooks=(),name=None ):\n  name=name if name else fn.__name__\n  self.__key__=\"directives\"\n  self.__id__=name.replace(\"_\",\"-\")\n  self.__value__=pyjs_bridge(fn)\n  \n  if hooks:\n   self.__value__={map_hook(hook):self.__value__ for hook in hooks}\n   \n   \ndef _directive_hook(name,hooks):\n def wrapper(fn):\n  _hooks=(fn.__name__,)if not hooks else hooks\n  return DirectiveHook(fn,hooks=_hooks,name=name)\n  \n return wrapper\n \n \ndef directive(fn,*hooks):\n if callable(fn):\n  return DirectiveHook(fn)\n return _directive_hook(fn,hooks)\n", ["vue.decorators.base"]], "vue.decorators.mixins": [".py", "from .base import VueDecorator\n\n\nclass Mixins(VueDecorator):\n __key__=\"mixins\"\n \n def __init__(self,*mixins):\n  self.__value__=list(mixins)\n", ["vue.decorators.base"]], "vue.decorators.method": [".py", "from .base import pyjs_bridge,VueDecorator\n\n\nclass Method(VueDecorator):\n __key__=\"methods\"\n \n def __init__(self,fn):\n  if hasattr(fn,\"__coroutinefunction__\"):\n   fn=coroutine(fn)\n  self.__value__=pyjs_bridge(fn,inject_vue_instance=True )\n  self.__id__=fn.__name__\n  \n  \ndef coroutine(_coroutine):\n def wrapper(*args,**kwargs):\n  import asyncio\n  \n  return asyncio.ensure_future(_coroutine(*args,**kwargs))\n  \n wrapper.__name__=_coroutine.__name__\n return wrapper\n \n \ndef method(_method):\n if hasattr(_method,\"__coroutinefunction__\"):\n  _method=coroutine(_method)\n return Method(_method)\n", ["asyncio", "vue.decorators.base"]], "vue.decorators.watcher": [".py", "from .base import pyjs_bridge,VueDecorator\n\n\nclass Watcher(VueDecorator):\n __key__=\"watch\"\n \n def __init__(self,name,fn,deep=False ,immediate=False ):\n  self.__id__=name\n  self._fn=pyjs_bridge(fn,inject_vue_instance=True )\n  self._deep=deep\n  self._immediate=immediate\n  \n @property\n def __value__(self):\n  return {\"handler\":self._fn,\"deep\":self._deep,\"immediate\":self._immediate}\n  \n  \ndef watch(name,deep=False ,immediate=False ):\n def decorator(fn):\n  return Watcher(name,fn,deep,immediate)\n  \n return decorator\n", ["vue.decorators.base"]], "vue.decorators.template": [".py", "from .base import VueDecorator\n\n\nclass Template(VueDecorator):\n __key__=\"template\"\n \n def __init__(self,template):\n  self.__value__=template\n", ["vue.decorators.base"]], "vue.decorators.lifecycle_hook": [".py", "from .base import pyjs_bridge,VueDecorator\n\n\nclass LifecycleHook(VueDecorator):\n mapping={\n \"before_create\":\"beforeCreate\",\n \"created\":\"created\",\n \"before_mount\":\"beforeMount\",\n \"mounted\":\"mounted\",\n \"before_update\":\"beforeUpdate\",\n \"updated\":\"updated\",\n \"before_destroy\":\"beforeDestroy\",\n \"destroyed\":\"destroyed\",\n }\n \n def __init__(self,name,fn):\n  self.__key__=self.mapping[name]\n  self.__value__=pyjs_bridge(fn,inject_vue_instance=True )\n  \n  \ndef lifecycle_hook(name):\n def wrapper(fn):\n  return LifecycleHook(name,fn)\n  \n return wrapper\n", ["vue.decorators.base"]], "vue.decorators.custom": [".py", "from .base import pyjs_bridge,VueDecorator\n\n\nclass Custom(VueDecorator):\n def __init__(self,fn,key,name=None ,static=False ):\n  self.__key__=key\n  self.__value__=pyjs_bridge(fn,inject_vue_instance=not static)\n  self.__id__=name if name is not None else fn.__name__\n  \n  \ndef custom(key,name=None ,static=False ):\n def wrapper(fn):\n  return Custom(fn,key,name,static)\n  \n return wrapper\n", ["vue.decorators.base"]], "vue.decorators.routes": [".py", "from .base import VueDecorator\n\n\nclass Routes(VueDecorator):\n __key__=\"routes\"\n \n def __init__(self,routes):\n  self.__value__=list(routes)\n", ["vue.decorators.base"]], "vue.decorators.components": [".py", "from .base import VueDecorator\n\n\nclass Components(VueDecorator):\n __key__=\"components\"\n \n def __init__(self,*mixins):\n  self.__value__=list(mixins)\n", ["vue.decorators.base"]], "vue.decorators.mutation": [".py", "from vue.bridge import VuexInstance\nfrom .base import pyjs_bridge,VueDecorator\n\n\nclass Mutation(VueDecorator):\n __key__=\"mutations\"\n \n def __init__(self,name,value):\n  self.__id__=name\n  self.__value__=value\n  \n  \ndef mutation(fn):\n def wrapper(state,payload):\n  return fn(\n  VuexInstance(state=state),\n  *payload.get(\"args\",()),\n  **payload.get(\"kwargs\",{}),\n  )\n  \n return Mutation(fn.__name__,pyjs_bridge(wrapper))\n", ["vue.bridge", "vue.decorators.base"]], "vue.decorators.computed": [".py", "from .base import pyjs_bridge,VueDecorator\n\n\nclass Computed(VueDecorator):\n __key__=\"computed\"\n \n def __init__(self,fn):\n  self.__id__=fn.__name__\n  self._getter=pyjs_bridge(fn)\n  self._setter=None\n  \n def setter(self,fn):\n  self._setter=pyjs_bridge(fn,inject_vue_instance=True )\n  return self\n  \n @property\n def __value__(self):\n  vue_object={\"get\":self._getter}\n  if self._setter:\n   vue_object[\"set\"]=self._setter\n  return vue_object\n  \n  \ndef computed(fn):\n return Computed(fn)\n", ["vue.decorators.base"]], "vue.decorators.model": [".py", "from .base import VueDecorator\n\n\nclass Model(VueDecorator):\n __key__=\"model\"\n \n def __init__(self,prop=\"value\",event=\"input\"):\n  self.prop=prop\n  self.event=event\n  \n @property\n def __value__(self):\n  return {\"prop\":self.prop,\"event\":self.event}\n", ["vue.decorators.base"]], "vue.decorators.render": [".py", "from .base import pyjs_bridge,VueDecorator\n\n\nclass Render(VueDecorator):\n __key__=\"render\"\n \n def __init__(self,fn):\n  self.__value__=pyjs_bridge(fn,inject_vue_instance=True )\n", ["vue.decorators.base"]], "vue.decorators.state": [".py", "from .base import VueDecorator\n\n\nclass State(VueDecorator):\n __key__=\"state\"\n \n def __init__(self,name,value):\n  self.__id__=name\n  self.__value__=value\n", ["vue.decorators.base"]], "vue.decorators.data": [".py", "from .base import pyjs_bridge,VueDecorator\n\n\nclass Data(VueDecorator):\n __key__=\"data\"\n \n def __init__(self,name,value):\n  self.__id__=name\n  self.__value__=value\n  \n  \ndef data(fn):\n return Data(fn.__name__,pyjs_bridge(fn))\n", ["vue.decorators.base"]], "vue.bridge": [".py", "from .object import Object\nfrom .list import List\nfrom .dict import Dict\nfrom .vue_instance import VueInstance\nfrom .vuex_instance import VuexInstance\n", ["vue.bridge.dict", "vue.bridge.list", "vue.bridge.object", "vue.bridge.vue_instance", "vue.bridge.vuex_instance"], 1], "vue.bridge.dict": [".py", "from browser import window\nfrom .object import Object\n\n\nclass Dict(Object):\n @staticmethod\n def __unwraps__():\n  return dict\n  \n @staticmethod\n def __can_wrap__(obj):\n  return (str(type(obj))==\"<undefined>\")or (\n  obj.__class__.__name__ ==\"JSObject\"\n  and not callable(obj)\n  and not isinstance(obj,dict)\n  )\n  \n def __eq__(self,other):\n  return other =={k:v for k,v in self.items()}\n  \n def __getitem__(self,item):\n  return Object.from_js(getattr(self._js,item))\n  \n def __iter__(self):\n  return (k for k in self.keys())\n  \n def pop(self,k,default=...):\n  if k not in self and not isinstance(default,type(Ellipsis)):\n   return default\n  item=self[k]\n  del self[k]\n  return item\n  \n def popitem(self):\n  key=self.keys()[0]\n  return key,self.pop(key)\n  \n def setdefault(self,k,default=None ):\n  if k not in self:\n   self[k]=default\n  return self[k]\n  \n def __len__(self):\n  return len(self.items())\n  \n def __contains__(self,item):\n  return Object.to_js(item)in self.keys()\n  \n def __delitem__(self,key):\n  window.Vue.delete(self._js,Object.to_js(key))\n  \n def __setitem__(self,key,value):\n  if key not in self:\n   window.Vue.set(self._js,Object.to_js(key),Object.to_js(value))\n  else :\n   setattr(self._js,Object.to_js(key),Object.to_js(value))\n   \n def get(self,k,default=None ):\n  if k not in self:\n   return default\n  return self[k]\n  \n def values(self):\n  return tuple(self[key]for key in self)\n  \n def update(self,_m=None ,**kwargs):\n  if _m is None :\n   _m={}\n   _m.update(kwargs)\n  window.Object.assign(self._js,Object.to_js(_m))\n  \n def clear(self):\n  while len(self)>0:\n   self.popitem()\n   \n @classmethod\n def fromkeys(cls,seq):\n  raise NotImplementedError()\n  \n def copy(self):\n  raise NotImplementedError()\n  \n def items(self):\n  return tuple((key,self[key])for key in self)\n  \n def keys(self):\n  return tuple(Object.from_js(key)for key in window.Object.keys(self._js))\n  \n def __str__(self):\n  if hasattr(self,\"toString\")and callable(self.toString):\n   return self.toString()\n  return repr(self)\n  \n def __repr__(self):\n  return \"{{{}}}\".format(\n  \", \".join(\"{!r}: {!r}\".format(k,v)for k,v in self.items())\n  )\n  \n def __set__(self,new):\n  self.clear()\n  self.update(new)\n  \n def __bool__(self):\n  return len(self)>0\n  \n def __getattr__(self,item):\n  try :\n   return self[item]\n  except KeyError:\n   raise AttributeError(item)\n   \n def __setattr__(self,key,value):\n  if key in [\"_js\"]:\n   return super().__setattr__(key,value)\n  self[key]=value\n  \n def __py__(self):\n  return {Object.to_py(k):Object.to_py(v)for k,v in self.items()}\n  \n def __js__(self):\n  if isinstance(self,dict):\n   return window.Object(\n   {Object.to_js(k):Object.to_js(v)for k,v in self.items()}\n   )\n  return self._js\n  \n  \nObject.Default=Dict\n", ["browser", "vue.bridge.object"]], "vue.bridge.vue_instance": [".py", "from .object import Object\nfrom .vuex_instance import VuexInstance\n\n\nclass VueInstance(Object):\n @staticmethod\n def __can_wrap__(obj):\n  return hasattr(obj,\"_isVue\")and obj._isVue\n  \n @property\n def store(self):\n  store=self.__getattr__(\"store\")\n  return VuexInstance(\n  state=store.state,\n  getters=store.getters,\n  commit=store.commit,\n  dispatch=store.dispatch,\n  )\n  \n def __getattr__(self,item):\n  try :\n   return Object.from_js(getattr(self._js,item))\n  except AttributeError:\n   if not item.startswith(\"$\"):\n    return self.__getattr__(\"${}\".format(item))\n   raise\n   \n def __setattr__(self,key,value):\n  if key in [\"_js\"]:\n   object.__setattr__(self,key,value)\n  elif hasattr(getattr(self,key),\"__set__\"):\n   getattr(self,key).__set__(value)\n  else :\n   if key not in dir(getattr(self._js,\"$props\",[])):\n    setattr(self._js,key,value)\n    \n    \nObject.SubClasses.append(VueInstance)\n", ["vue.bridge.object", "vue.bridge.vuex_instance"]], "vue.bridge.object": [".py", "class Object:\n SubClasses=[]\n Default=None\n \n @classmethod\n def sub_classes(cls):\n  return cls.SubClasses+([cls.Default]if cls.Default else [])\n  \n @classmethod\n def from_js(cls,jsobj):\n  for sub_class in cls.sub_classes():\n   if sub_class.__can_wrap__(jsobj):\n    return sub_class(jsobj)\n  return jsobj\n  \n @classmethod\n def to_js(cls,obj):\n  if isinstance(obj,Object):\n   return obj.__js__()\n  for sub_class in cls.sub_classes():\n   if isinstance(obj,sub_class.__unwraps__()):\n    return sub_class.__js__(obj)\n  return obj\n  \n @classmethod\n def to_py(cls,obj):\n  obj=Object.from_js(obj)\n  if isinstance(obj,Object):\n   return obj.__py__()\n  for sub_class in cls.sub_classes():\n   if isinstance(obj,sub_class.__unwraps__()):\n    return sub_class.__py__(obj)\n  return obj\n  \n @staticmethod\n def __can_wrap__(obj):\n  return False\n  \n @staticmethod\n def __unwraps__():\n  return ()\n  \n def __init__(self,js):\n  self._js=js\n  \n def __js__(self):\n  return self._js\n  \n def __py__(self):\n  return self\n", []], "vue.bridge.vuex_instance": [".py", "class VuexInstance:\n def __init__(\n self,\n state=None ,\n getters=None ,\n root_state=None ,\n root_getters=None ,\n commit=None ,\n dispatch=None ,\n ):\n  self.__state__=state if state else {}\n  self.__getter__=getters\n  self.__root_getter__=root_getters\n  self.__root_state__=root_state if root_state else {}\n  self.__commit__=commit\n  self.__dispatch__=dispatch\n  \n def __getattr__(self,item):\n  item=item.replace(\"$\",\"\")\n  if item in [\"__state__\",\"__root_state__\"]:\n   return {}\n  if item in self.__state__:\n   return self.__state__[item]\n  if hasattr(self.__getter__,item):\n   return getattr(self.__getter__,item)\n  if item in self.__root_state__:\n   return self.__root_state__[item]\n  if hasattr(self.__root_getter__,item):\n   return getattr(self.__root_getter__,item)\n  return super().__getattribute__(item)\n  \n def __setattr__(self,key,value):\n  key=key.replace(\"$\",\"\")\n  if key in self.__state__:\n   self.__state__[key]=value\n  elif key in self.__root_state__:\n   self.__root_state__[key]=value\n  else :\n   super().__setattr__(key,value)\n   \n def commit(self,mutation_name,*args,**kwargs):\n  self.__commit__(mutation_name,{\"args\":args,\"kwargs\":kwargs})\n  \n def dispatch(self,mutation_name,*args,**kwargs):\n  self.__dispatch__(mutation_name,{\"args\":args,\"kwargs\":kwargs})\n", []], "vue.bridge.list": [".py", "from browser import window\nfrom .object import Object\n\n\nclass List(Object):\n @staticmethod\n def __unwraps__():\n  return list,tuple\n  \n @staticmethod\n def __can_wrap__(obj):\n  return window.Array.isArray(obj)and not isinstance(obj,list)\n  \n def _slice(self,slc):\n  if isinstance(slc,int):\n   if slc <0:\n    slc=len(self)+slc\n   return slc,slc+1\n  start=slc.start if slc.start is not None else 0\n  stop=slc.stop if slc.stop is not None else len(self)\n  return start,stop\n  \n def __eq__(self,other):\n  return other ==[i for i in self]\n  \n def __mul__(self,other):\n  return [i for i in self]*other\n  \n def index(self,obj,start=0,_stop=-1):\n  index=self._js.indexOf(Object.to_js(obj),start)\n  if index ==-1:\n   raise ValueError(\"{} not in list\".format(obj))\n  return index\n  \n def extend(self,iterable):\n  self._js.push(*(i for i in iterable))\n  \n def __len__(self):\n  return self._js.length\n  \n def __contains__(self,item):\n  try :\n   self.index(item)\n   return True\n  except ValueError:\n   return False\n   \n def __imul__(self,other):\n  raise NotImplementedError()\n  \n def count(self,obj):\n  return [i for i in self].count(obj)\n  \n def reverse(self):\n  self._js.reverse()\n  \n def __delitem__(self,key):\n  start,stop=self._slice(key)\n  self._js.splice(start,stop -start)\n  \n def __setitem__(self,key,value):\n  start,stop=self._slice(key)\n  value=value if isinstance(value,list)else [value]\n  self._js.splice(start,stop -start,*value)\n  \n def __getitem__(self,item):\n  start,stop=self._slice(item)\n  value=self._js.slice(start,stop)\n  if isinstance(item,int):\n   return Object.from_js(value[0])\n  return [Object.from_js(i)for i in value]\n  \n def __reversed__(self):\n  raise NotImplementedError()\n  \n def __rmul__(self,other):\n  raise NotImplemented()\n  \n def append(self,obj):\n  self._js.push(Object.to_js(obj))\n  \n def insert(self,index,obj):\n  self._js.splice(index,0,Object.to_js(obj))\n  \n def remove(self,obj):\n  index=self._js.indexOf(Object.to_js(obj))\n  while index !=-1:\n   del self[self._js.indexOf(Object.to_js(obj))]\n   index=self._js.indexOf(Object.to_js(obj))\n   \n def __iadd__(self,other):\n  raise NotImplemented()\n  \n def __iter__(self):\n  def _iter(lst):\n   for i in range(lst.__len__()):\n    yield lst[i]\n    \n  return _iter(self)\n  \n def pop(self,index=-1):\n  return Object.from_js(self._js.splice(index,1)[0])\n  \n def sort(self,key=None ,reverse=False ):\n  self[:]=sorted(self,key=key,reverse=reverse)\n  \n def __add__(self,other):\n  raise NotImplemented()\n  \n def clear(self):\n  raise NotImplemented()\n  \n def copy(self):\n  raise NotImplemented()\n  \n def __set__(self,new):\n  self[:]=new\n  \n def __repr__(self):\n  return \"[{}]\".format(\", \".join(repr(i)for i in self))\n  \n def __py__(self):\n  return [Object.to_py(item)for item in self]\n  \n def __js__(self):\n  if isinstance(self,(list,tuple)):\n   return window.Array(*[Object.to_js(item)for item in self])\n  return self._js\n  \n  \nObject.SubClasses.append(List)\n", ["browser", "vue.bridge.object"]]}
__BRYTHON__.update_VFS(scripts)
