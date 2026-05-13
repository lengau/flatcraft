PROJECT=flatcraft
UV_TEST_GROUPS := "--group=dev"
UV_LINT_GROUPS := "--group=lint" "--group=types"

include common.mk

.PHONY: format
format: format-ruff  ## Run all automatic formatters

.PHONY: lint
lint: lint-ruff lint-mypy lint-pyright  ## Run all linters

.PHONY: pack
pack: pack-pip  ## Build all packages

.PHONY: setup-lint
setup-lint: install-uv  ## Set up the lint environment
	uv sync $(UV_TEST_GROUPS) $(UV_LINT_GROUPS)
