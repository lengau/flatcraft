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

#### Running Individual Test Files

To run a specific test file or test suite:

```bash
# Run a single test file
uv run pytest tests/unit/test_models.py

# Run tests matching a pattern
uv run pytest tests/unit -k "test_project"

# Run with verbose output
uv run pytest tests/ -v

# Run with specific markers
uv run pytest tests/ -m "not slow"
```

For more pytest options, see the [pytest documentation](https://docs.pytest.org/).

### Linting and Formatting

```bash
make lint      # Run all linters (ruff, mypy, pyright)
make format    # Auto-format code with ruff
```

### Building

```bash
make pack      # Build pip packages (sdist + wheel)
```

## Project Architecture

Flatcraft is organized into the following core modules:

- **`flatcraft/cli.py`** - Command-line interface implementation using craft-application
- **`flatcraft/application.py`** - Main application class extending craft-application
- **`flatcraft/models/`** - Data models including:
  - `project.py` - Project configuration model (parsed from flatcraft.yaml)
- **`flatcraft/services/`** - Core services:
  - `lifecycle.py` - Build lifecycle management (init, pack, clean operations)
- **`flatcraft/errors.py`** - Custom exception types

The build pipeline works as follows:
1. Load and validate `flatcraft.yaml` via models
2. Generate Flatpak manifest using configuration
3. Invoke `flatpak-builder` with the generated manifest
4. Package and deliver the resulting Flatpak bundle

## Adding a New Build System

To add support for a new build system (e.g., `cargo` for Rust projects):

1. **Update the project model** (`flatcraft/models/project.py`):
   - Add the new build system to the `BuildSystem` enum or string validation

2. **Implement build logic** (in `flatcraft/services/lifecycle.py` or a new builder module):
   - Add a handler/builder class that generates the appropriate build commands
   - Ensure it respects common module fields (sources, build-commands, etc.)

3. **Add tests** (`tests/`):
   - Create unit tests for parsing flatcraft.yaml with your new build system
   - Add integration tests that verify the Flatpak manifest is generated correctly

4. **Update documentation**:
   - Add the build system to the README.md "Supported build systems" table
   - Add any specific configuration examples to the example flatcraft.yaml

5. **Testing**:
   - Run `make test` to ensure all tests pass
   - Verify the generated Flatpak manifest manually if needed

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
