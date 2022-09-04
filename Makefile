VENV_DIR=./.venv

AIRFLOW_VERSION=2.3.2
MAJOR_PYTHON_VER=3
MINOR_PYTHON_VER=7

# https://airflow.apache.org/docs/apache-airflow/2.3.2/installation/installing-from-pypi.html#constraints-files
AIRFLOW_CONSTRAINTS="https://raw.githubusercontent.com/apache/airflow/constraints-$(AIRFLOW_VERSION)/constraints-$(MAJOR_PYTHON_VER).$(MINOR_PYTHON_VER).txt"

start: ## start the dockerized airflow environment
	docker compose up airflow-init
	docker compose exec localstack  aws s3 --endpoint-url http://0.0.0.0:4566 mb s3://my-bucket

	docker compose up --detach airflow-webserver --wait
	@echo "Airflow has started. Go to http://0.0.0.0:8080. The password and user are 'airflow'"

docker-cleanup: ## stop all docker components and clean up the images and volumes
	docker compose down --volumes

install-requirements: ## Installs packages from requirements file
	$(VENV_DIR)/bin/pip install -r ./requirements.txt --constraint $(AIRFLOW_CONSTRAINTS)

create-venv: ## create a local virtual environment for python
	python3 -m venv "$(VENV_DIR)"

venv: create-venv install-requirements ## Create virtual environment + install packages

linting-test: ## run linting checks
	$(VENV_DIR)/bin/python -m black --check --diff --line-length 120 .

unit-test: ## run unit tests
	PYTHONPATH=./dags $(VENV_DIR)/bin/python -m pytest

test: unit-test linting-test ## run all tests
