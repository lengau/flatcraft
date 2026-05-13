# Contributing to Flatcraft

## Setting up a development environment

### Prerequisites

- Python 3.10 or later
- [uv](https://docs.astral.sh/uv/) package manager
- `flatpak-builder` (for integration testing)

### Quick Setup

```bash
make setup
```

This will install uv (if needed) and sync all development dependencies.

### Manual Setup

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync dependencies
uv sync --group=dev --group=types
```

## Development Workflow

### Running Tests

```bash
make test              # Run all tests
make test-coverage     # Run with coverage report
```

### Linting and Formatting

```bash
make lint      # Run all linters (ruff, mypy, pyright)
make format    # Auto-format code with ruff
```

### Building

```bash
make pack      # Build pip packages (sdist + wheel)
```

## Code Style

- We use [ruff](https://docs.astral.sh/ruff/) for linting and formatting
- Type annotations are required for all public APIs
- Docstrings follow PEP 257 conventions

## Submitting Changes

1. Fork the repository
2. Create a feature branch from `main`
3. Make your changes with tests
4. Ensure `make lint` and `make test` pass
5. Submit a pull request

## Reporting Issues

Report bugs and feature requests on the
[GitHub issue tracker](https://github.com/lengau/flatcraft/issues).
