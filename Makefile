PYTHONPATH=.:stubs

.PHONY: env.brython
env.brython:
	mkdir -p js
	rm -Rf js/brython
	cd js; git clone https://github.com/brython-dev/brython.git
	cd js/brython; git checkout 34d9698afe922e3b0c802c9dab6128e256a8346c
	cp js/brython/www/src/brython_dist.js js

.PHONY: env.vuejs
env.vuejs:
	mkdir -p js
	rm -Rf js/vuejs
	cd js; git clone https://github.com/vuejs/vue.git vuejs
	cd js/vuejs; git checkout v2.5.16
	cp js/vuejs/dist/vue.js js

.PHONY: env.pip
env.pip:
	pip install -r requirements.txt

.PHONY: env.chrome
env.chrome:
	python -c "import chromedriver_install as cdi;cdi.install(file_directory='tests/selenium', overwrite=True)"

.PHONY: env.up
env.up: env.pip env.brython env.vuejs env.chrome

.PHONY: env.clean
env.clean:
	git clean -xdf --exclude .idea --exclude venv --exclude js

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
	rm -Rf gh-pages

	mkdir gh-pages
	cp -R README.md planning.md docs examples vue gh-pages
	cp jekyll.yml gh-pages/_config.yml

	mkdir gh-pages/js
	cp js/vue.js gh-pages/js
	cp js/brython_dist.js gh-pages/js

	mkdir gh-pages/tests
	cp -R tests/selenium/_html/* gh-pages/tests

.PHONY: ci
ci: tests ci.docs
