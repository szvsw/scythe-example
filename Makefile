.PHONY: install
install: ## Install the poetry environment and install the pre-commit hooks
	@echo "🚀 Creating virtual environment using uv"
	@uv sync --all-groups --all-extras

.PHONY: worker
worker: ## Start the worker
	@uv run --env-file .env main.py

.PHONY: allocate
allocate: ## Allocate the experiments
	@uv run --env-file .env allocate.py

