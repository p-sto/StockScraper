
PYTHON_VER=/usr/local/bin/python3.5
PWD:=$(shell pwd)
PYTHONPATH=$(PWD)
PIP=venv/bin/pip3
PIP_FLAGS=--trusted-host=http://pypi.python.org/simple/

.PHONY: all venv clean test

all: venv test clean

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || virtualenv -p $(PYTHON_VER) venv
	$(PIP) $(PIP_FLAGS) install -Ur requirements.txt
	touch venv/bin/activate

test:
	py.test -s --cov=StockScraper --cov-report html --cov-config .coveragerc --tb=short tests/
	coverage report

clean:
	rm -rf htmlcov
	rm -rf */__pycache__
	rm -rf */__init__.pyc
	rm -rf */*/__pycache__
	rm -rf .coverage
	rm -rf .cache

