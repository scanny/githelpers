PYTHON      = $(shell test -x bin/python && echo bin/python || \
                      echo `which python`)
SETUP       = $(PYTHON) ./setup.py

.PHONY: clean coverage sdist

help:
	@echo "Please use \`make <target>' where <target> is one or more of"
	@echo "  clean     delete intermediate work product and start fresh"
	@echo "  coverage  run nosetests with coverage"
	@echo "  sdist     generate a source distribution into dist/"
	@echo "  test      run the full test suite"

clean:
	find . -type f -name \*.pyc -exec rm {} \;
	find . -type f -name .DS_Store -exec rm {} \;
	rm -rf dist *.egg-info .coverage

coverage:
	py.test --cov-report term-missing

sdist:
	$(SETUP) sdist

test: clean
	flake8 githelpers tests
	py.test -x
	behave -s --stop

test-wip: clean
	flake8 githelpers tests
	py.test -x
	behave -s --stop --tags=-wip
