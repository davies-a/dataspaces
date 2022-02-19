PYTHON_MODULE_NAME=dspace

fmt:
	isort --profile black .
	black .

lint:
	pylint $(PYTHON_MODULE_NAME) --rcfile=pyproject.toml

install:
	pip install .

install-dev:
	pip install -e ".[tests]"

requirements:
	pip install \
		-r requirements.txt \
		--ignore-installed

