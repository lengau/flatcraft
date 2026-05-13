# Common Makefile items adapted from canonical/starbase

SOURCES=$(wildcard *.py) $(PROJECT) tests

ifneq ($(OS),Windows_NT)
	OS := $(shell uname)
endif
ifdef CI
	APT := apt-get --yes
else
	APT := apt-get
endif

# By default we should not update the uv lock file here.
export UV_FROZEN := true

.DEFAULT_GOAL := help

.ONESHELL:

.SHELLFLAGS = -ec

.PHONY: help
help: ## Show this help.
	@printf "\e[1m%-30s\e[0m | \e[1m%s\e[0m\n" "Target" "Description"
	printf "\e[2m%-30s + %-41s\e[0m\n" "------------------------------" "------------------------------------------------"
	egrep '^[^:]+\: [^#]*##' $$(echo $(MAKEFILE_LIST) | tac --separator=' ') | sed -e 's/:[^#]*/ /' | sort -V | awk -F '[: ]*' \
	'{
		if ($$2 == "##")
		{
			$$1=sprintf(" %-28s", $$1);
			$$2=" | ";
			print $$0;
		}
		else
		{
			$$1=sprintf("  └ %-25s", $$1);
			$$2=" | ";
			$$3=sprintf(" └ %s", $$3);
			print $$0;
		}
	}' | uniq

.PHONY: setup
setup: install-uv  ## Set up a development environment
	uv sync $(UV_TEST_GROUPS) $(UV_LINT_GROUPS)

.PHONY: clean
clean:  ## Clean up the development environment
	rm -rf dist build *.egg-info .coverage* .venv results/

.PHONY: format-ruff
format-ruff: install-ruff  ##- Automatically format with ruff
	success=true
	ruff check --fix $(SOURCES) || success=false
	ruff format $(SOURCES)
	$$success || exit 1

.PHONY: lint-ruff
lint-ruff: install-ruff  ##- Lint with ruff
ifneq ($(CI),)
	@echo ::group::$@
endif
	ruff check $(SOURCES)
	ruff format --diff $(SOURCES)
ifneq ($(CI),)
	@echo ::endgroup::
endif

.PHONY: lint-mypy
lint-mypy:  ##- Check types with mypy
ifneq ($(CI),)
	@echo ::group::$@
endif
	uv run mypy --show-traceback --show-error-codes $(PROJECT)
ifneq ($(CI),)
	@echo ::endgroup::
endif

.PHONY: lint-pyright
lint-pyright:  ##- Check types with pyright
ifneq ($(CI),)
	@echo ::group::$@
endif
ifneq ($(shell which pyright),)
	pyright --pythonpath .venv/bin/python
else
	uv tool run pyright --pythonpath .venv/bin/python
endif
ifneq ($(CI),)
	@echo ::endgroup::
endif

.PHONY: test
test:  ## Run all tests
	uv run pytest

.PHONY: test-coverage
test-coverage:  ## Generate coverage report
	uv run coverage run --source $(PROJECT),tests -m pytest
	uv run coverage xml -o results/coverage.xml
	uv run coverage report -m
	uv run coverage html

.PHONY: pack-pip
pack-pip:  ##- Build packages for pip (sdist, wheel)
ifneq ($(CI),)
	@echo ::group::$@
endif
	uv build --quiet .
ifneq ($(CI),)
	@echo ::endgroup::
endif

.PHONY: install-uv
install-uv:
ifneq ($(shell which uv),)
else ifneq ($(shell which snap),)
	sudo snap install --classic astral-uv
else ifneq ($(shell which brew),)
	brew install uv
else
	curl -LsSf https://astral.sh/uv/install.sh | sh
endif

.PHONY: install-ruff
install-ruff:
ifneq ($(shell which ruff),)
else ifneq ($(shell which snap),)
	sudo snap install ruff
else
	make install-uv
	uv tool install ruff
endif
