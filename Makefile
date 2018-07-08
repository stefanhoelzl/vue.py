PYTHONPATH=.:stubs

.PHONY: env.brython
env.brython:
	mkdir -p js
	cd js; git clone https://github.com/brython-dev/brython.git

.PHONY: env.vuejs
env.vuejs:
	mkdir -p js
	cd js; git clone https://github.com/vuejs/vue.git vuejs

.PHONY: env.pip
env.pip:
	pip install -r requirements.txt

.PHONY: env.chrome
env.chrome:
	python -c "import chromedriver_install as cdi;cdi.install(file_directory='tests/selenium', overwrite=False)"

.PHONY: env.up
env.up: env.pip env.brython env.vuejs env.chrome

.PHONY: env.clean
env.clean:
	git clean -xdf --exclude .idea --exclude venv --exclude js

.PHONY: env.down
env.down:
	git clean -xdf --exclude .idea --exclude venv
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
