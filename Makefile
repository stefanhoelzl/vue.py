PYTHONPATH=.:stubs

.PHONY: env.brython
env.brython:
	mkdir -p vuemanager/js
	rm -Rf vuemanager/js/brython
	cd vuemanager/js; git clone https://github.com/brython-dev/brython.git brython
	cd vuemanager/js/brython; git checkout 7e9a7d901acc6f2112ab8e570a0d560aafb616d2
	cp vuemanager/js/brython/www/src/brython_dist.js vuemanager/js
	cp vuemanager/js/brython/LICENCE.txt vuemanager/js/LICENSE_BRYTHON

.PHONY: env.vuejs
env.vuejs:
	mkdir -p vuemanager/js
	rm -Rf vuemanager/js/vuejs
	cd vuemanager/js; git clone https://github.com/vuejs/vue.git vuejs
	cd vuemanager/js/vuejs; git checkout v2.5.16
	cp vuemanager/js/vuejs/dist/vue.js vuemanager/js
	cp vuemanager/js/vuejs/LICENSE vuemanager/js/VUEJS_LICENSE

.PHONY: env.vuex
env.vuex:
	mkdir -p vuemanager/js
	rm -Rf vuemanager/js/vuex
	cd vuemanager/js; git clone https://github.com/vuejs/vuex.git vuex
	cd vuemanager/js/vuex; git checkout v3.0.1
	cp vuemanager/js/vuex/dist/vuex.js vuemanager/js
	cp vuemanager/js/vuex/LICENSE vuemanager/js/VUEX_LICENSE

.PHONY: env.pip
env.pip:
	pip install -r requirements.txt

.PHONY: env.chrome
env.chrome:
	python -c "import chromedriver_install as cdi;cdi.install(file_directory='tests/selenium', overwrite=True)"

.PHONY: env.up
env.up: env.pip env.brython env.vuejs env.vuex env.chrome

.PHONY: env.clean
env.clean:
	git clean -xdf --exclude .idea --exclude venv --exclude vuemanager/js

.PHONY: env.down
env.down:
	git clean -xdf --exclude .idea --exclude venv --exclude debug
	pip freeze | xargs pip uninstall -y

.PHONY: serve
serve:
	python -m http.server 8000

.PHONY: tests.selenium
tests.selenium:
	PYTHONPATH=$(PYTHONPATH) pytest tests/selenium

.PHONY: tests.unit
tests.unit:
	PYTHONPATH=$(PYTHONPATH) pytest tests/unit

.PHONY: tests
tests:
	PYTHONPATH=$(PYTHONPATH) pytest tests

.PHONY: ci.docs
ci.docs:
	rm -Rf gh-pages-build
	mkdir gh-pages-build

	cp -Rf docs/* README.md vue gh-pages-build
	cp -Rf examples_static gh-pages-build/examples

	mkdir gh-pages-build/js
	cp vuemanager/js/vue.js gh-pages-build/js
	cp vuemanager/js/brython_dist.js gh-pages-build/js

	mkdir gh-pages-build/tests
	cp -R tests/selenium/_html/* gh-pages-build/tests

.PHONY: ci
ci: tests ci.docs
