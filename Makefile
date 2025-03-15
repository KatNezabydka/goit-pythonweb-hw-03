.PHONY: setup \
		lint \
		mypy \
		test \
		coverage \
		help

venv/bin/activate: ## Alias for virtual environment
	python3 -m venv venv

setup: venv/bin/activate ## Project setup
	. venv/bin/activate; pip install --upgrade pip
	. venv/bin/activate; pip install poetry
	. venv/bin/activate; poetry install


lint: ## Run linter
	. venv/bin/activate; ruff format --config ./pyproject.toml . && ruff check --fix --config ./pyproject.toml .

mypy: venv/bin/activate ## Run mypy
	. venv/bin/activate; mypy ./

test: ## Run tests check
	. venv/bin/activate; poetry run pytest $(filter-out $@,$(MAKECMDGOALS)) -s

coverage: ## Run tests coverage
	. venv/bin/activate; poetry run coverage run --source="." -m pytest -vv
	. venv/bin/activate; poetry run coverage xml
	. venv/bin/activate; poetry run coverage report -m --fail-under=5.00

# Just help
help: ## Display help screen
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
