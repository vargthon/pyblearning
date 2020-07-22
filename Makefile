.PHONY: virtual install build-requirements black isort flake8

virtual: .venv/bin/pip # Creates an isolated python 3 environment

.venv/bin/pip:
	virtualenv -p /usr/bin/python3 .venv

install:
	.venv/bin/pip install -Ur requirements.txt

update-requirements: install
	.venv/bin/pip freeze > requirements.txt

run:
	.venv/bin/python3 /Users/vargthon/Documents/programacao/machine-learn/ml/src/test.py

project_name = Machine-Learning