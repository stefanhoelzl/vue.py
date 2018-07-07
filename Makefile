.PHONY: env.brython
env.brython:
	cd vue; git clone https://github.com/brython-dev/brython.git

.PHONY: env.vuejs
env.vuejs:
	cd vue; git clone https://github.com/vuejs/vue.git vuejs

.PHONY: env.pip
env.pip:
	pip install -r requirements.txt

.PHONY: env.chrome
env.chrome:
	python -c "import chromedriver_install as cdi;cdi.install(file_directory='tests/selenium', overwrite=False)"

.PHONY: env.install
env.install: env.pip env.brython env.vuejs env.chrome

.PHONY: env.clean
env.clean:
	git clean -xdf --exclude .idea --exclude venv
	pip freeze | xargs pip uninstall -y

.PHONY: env.serve
env.serve:
	python -m http.server 8000
