PYTHONPATH=.:stubs

.PHONY: env.brython
env.brython:
	mkdir -p vuecli/js
	rm -Rf vuecli/js/brython
	cd vuecli/js; git clone https://github.com/brython-dev/brython.git brython
	cd vuecli/js/brython; git checkout e67795cda1e7ee28cf303feab6a2da91fbe2f048
	cp vuecli/js/brython/www/src/brython_dist.js vuecli/js
	cp vuecli/js/brython/LICENCE.txt vuecli/js/LICENSE_BRYTHON

.PHONY: env.vuejs
env.vuejs:
	mkdir -p vuecli/js
	rm -Rf vuecli/js/vuejs
	cd vuecli/js; git clone https://github.com/vuejs/vue.git vuejs
	cd vuecli/js/vuejs; git checkout v2.5.16
	cp vuecli/js/vuejs/dist/vue.js vuecli/js
	cp vuecli/js/vuejs/LICENSE vuecli/js/LICENSE_VUEJS

.PHONY: env.vuex
env.vuex:
	mkdir -p vuecli/js
	rm -Rf vuecli/js/vuex
	cd vuecli/js; git clone https://github.com/vuejs/vuex.git vuex
	cd vuecli/js/vuex; git checkout v3.0.1
	cp vuecli/js/vuex/dist/vuex.js vuecli/js
	cp vuecli/js/vuex/LICENSE vuecli/js/LICENSE_VUEX

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
	git clean -xdf --exclude .idea --exclude venv --exclude vuecli/js

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

.PHONY: release.build
release.build:
	python setup.py sdist bdist_wheel

.PHONY: ci.docs
ci.docs:
	rm -Rf gh-pages-build
	mkdir gh-pages-build

	cp -Rf docs/* README.md vue gh-pages-build
	cp -Rf examples_static gh-pages-build/examples
	cp examples/index.md gh-pages-build/examples

	mkdir gh-pages-build/js
	cp vuecli/js/vue.js gh-pages-build/js
	cp vuecli/js/brython_dist.js gh-pages-build/js

	mkdir gh-pages-build/tests
	cp -R tests/selenium/_html/* gh-pages-build/tests

.PHONY: ci
ci: tests release.build ci.docs
