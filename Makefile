# basic:
PROJECT_NAME=StockScraper
PWD:=$(shell pwd)
PYTHONPATH=$(PWD)
TEST_DIR=tests
VENV=venv/bin
PIP=$(VENV)/pip3
PIP_FLAGS=--trusted-host=http://pypi.python.org/simple/
PYTEST=$(VENV)/py.test
PYLINT=$(VENV)/pylint
COVERAGE=$(VENV)/coverage
MYPY=$(VENV)/mypy
MYPYFLAGS=--ignore-missing-imports --follow-imports=skip
PYTHON_VERSION=python3.5
HOST_PYTHON_VER=$(shell echo which $(PYTHON_VERSION))
VENV_PYTHOM_VER=$(VENV)/python3
CODE_COV=codecov

# git settings:
GIT_COMMIT = $(shell git log -1 "--pretty=format:%H")
GIT_STATUS = $(shell git status -sb --untracked=no | wc -l | awk '{ if($$1 == 1){ print "clean" } else { print "pending" } }')
GIT_BRANCH = $(shell git describe --contains --all HEAD)


.PHONY: all venv clean test test_pytest test_gen_coverage_rep test_pylint test_mypy git-status commit-id

all: venv test clean

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || virtualenv -p $(PYTHON_VERSION) venv
	$(PIP) $(PIP_FLAGS) install -Ur requirements.txt
	touch venv/bin/activate

test_pytest:
	$(PYTEST) --verbose --color=yes --cov=$(PROJECT_NAME) --cov-report html --cov-config .coveragerc --tb=short $(TEST_DIR)

test_pylint:
	find $(PROJECT_NAME) -name '*.py' | xargs $(PYLINT) --rcfile=$(PWD)/.pylintrc

test_gen_coverage_rep:
	$(COVERAGE) report

test_mypy:
	find $(PROJECT_NAME) -name '*.py' | xargs $(MYPY) $(MYPYFLAGS)

test_codecov:
	$(CODE_COV) --token=$(SCRAPERTOKEN)

test: test_pytest test_pylint test_mypy test_gen_coverage_rep


clean:
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf .cache
	rm -rf .mypy_cache
	find -name '$(PROJECT_NAME).log' | xargs rm -rf
	find $(PROJECT_NAME) -name '*.pyc' | xargs rm -rf
	find $(PROJECT_NAME) -name '__pycache__' -type d | xargs rm -rf
	find $(TEST_DIR) -name '__pycache__' -type d | xargs rm -rf

git-status:
	test "${GIT_STATUS}" == "clean" || (echo "GIT STATUS NOT CLEAN"; exit 1) >&2

commit-id:
	test ${GIT_COMMIT}