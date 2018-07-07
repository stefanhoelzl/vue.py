.PHONY: env.brython
env.brython:
	rm -Rf vue/brython
	mkdir vue/brython
	cd vue/brython; python -m brython --install

.PHONY: env.pip
env.pip:
	pip install -r requirements.txt

.PHONY: env.chrome
env.chrome:
	python -c "import chromedriver_install as cdi;cdi.install(file_directory='tests/selenium', overwrite=False)"

.PHONY: env.install
env.install: env.pip env.brython env.chrome

.PHONY: env.clean
env.clean:
	git clean -xdf --exclude .idea --exclude venv
	pip freeze | xargs pip uninstall -y

.PHONY: env.serve
env.serve:
	python -m http.server 8000
