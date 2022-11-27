.PHONY: format help

# Help system from https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Establish local environment with dependencies installed
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt
	mkdir -p data/uploads

build: ## Build containers
	docker-compose build

up: ## Start containers
	docker-compose up -d

down: ## Stop containers
	docker-compose down

dbshell:
	docker-compose exec db psql -U nerochan

shell: ## Start Flask CLI shell
	./manage.sh shell

init: ## Initialize SQLite DB
	./manage.sh init

dev: ## Start Flask development web server
	./manage.sh run
