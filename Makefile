PYTHONPATH=.:stubs

.PHONY: env.vuejs
env.vuejs:
	mkdir -p vuecli/js
	curl https://unpkg.com/vue@2.6.11/dist/vue.js > vuecli/js/vue.js
	curl https://raw.githubusercontent.com/vuejs/vue/dev/LICENSE > vuecli/js/LICENSE_VUE

.PHONY: env.vuex
env.vuex:
	mkdir -p vuecli/js
	curl https://unpkg.com/vuex@3.4.0/dist/vuex.js > vuecli/js/vuex.js
	curl https://raw.githubusercontent.com/vuejs/vuex/master/LICENSE > vuecli/js/LICENSE_VUEX

.PHONY: env.vue-router
env.vue-router:
	mkdir -p vuecli/js
	curl https://unpkg.com/vue-router@3.3.2/dist/vue-router.js > vuecli/js/vue-router.js
	curl https://raw.githubusercontent.com/vuejs/vue-router/dev/LICENSE > vuecli/js/LICENSE_VUE_ROUTER

.PHONY: env.pip
env.pip:
	pip install -r requirements.txt
	pip install -e .

.PHONY: env.chrome
env.chrome:
	python tests/selenium/chromedriver.py

.PHONY: env.up
env.up: env.pip env.vuejs env.vuex env.vue-router env.chrome

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

.PHONY: run
run:
	cd ${APP} && vue-cli deploy flask

.PHONY: tests.selenium
tests.selenium:
	PYTHONPATH=$(PYTHONPATH) pytest tests/selenium

.PHONY: tests.unit
tests.unit:
	PYTHONPATH=$(PYTHONPATH) pytest tests/unit

.PHONY: tests.cli
tests.cli:
	PYTHONPATH=$(PYTHONPATH) pytest tests/cli

.PHONY: tests
tests:
	PYTHONPATH=$(PYTHONPATH) pytest tests/${TEST}

.PHONY: format
format:
	black --target-version py38 .

.PHONY: lint
lint:
	black --target-version py38 --check .

.PHONY: build
build:
	python setup.py sdist bdist_wheel

.PHONY: docs
docs:
	rm -Rf gh-pages-build
	mkdir gh-pages-build

	cp -Rf docs/* README.md vue gh-pages-build
	cp -Rf examples_static gh-pages-build/examples
	cp examples/index.md gh-pages-build/examples

	mkdir gh-pages-build/tests
	cp -R tests/selenium/_html/* gh-pages-build/tests

	mkdir gh-pages-build/js
	vue-cli package gh-pages-build/js

.PHONY: ci
ci: lint tests build docs

NEXT_VERSION=`python release/next_version.py`
CHANGELOG=`python release/changelog.py`
COMMIT_MSG_FILE=/tmp/vue-release-commit-message
VERSION_FILE=vue/__version__.py
CURRENT_COMMIT=`git log --pretty="%H" -1`
LAST_RELEASE_COMMIT=`git log --pretty="%H" --grep="\[release\]" -1`

.PHONY: release.prepare
release.prepare:
	git checkout master
	git pull

.PHONY: release.check
release.check:
	git diff HEAD --exit-code --no-patch
	python release/check_ci.py ${CURRENT_COMMIT}

.PHONY: release.commit.prepare
release.commit.prepare:
	echo "[release] v${NEXT_VERSION}\n\n${CHANGELOG}" > ${COMMIT_MSG_FILE}
	cat ${COMMIT_MSG_FILE}
	read -p "Press enter for release commit!" var
	echo "__version__ = '${NEXT_VERSION}'" > ${VERSION_FILE}

.PHONY: release.commit
release.commit: release.commit.prepare format
	git add ${VERSION_FILE}
	git commit --file=${COMMIT_MSG_FILE}
	git tag v`python -c "import vue; print(vue.__version__)"`

.PHONY: release.push
release.push:
	git push
	git push --tags
	git fetch
	git checkout release
	git merge master
	git push --set-upstream origin release
	git checkout master

.PHONY: release
release: release.prepare release.check release.commit release.push
