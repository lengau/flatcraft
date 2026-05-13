# Flatcraft

A craft tool for creating [Flatpak](https://flatpak.org/) packages, following the
patterns established by [snapcraft](https://github.com/canonical/snapcraft),
[rockcraft](https://github.com/canonical/rockcraft), and other \*craft tools.

## Overview

Flatcraft simplifies the creation of Flatpak packages by providing a declarative
`flatcraft.yaml` project file and a familiar \*craft CLI interface. It leverages
[craft-application](https://github.com/canonical/craft-application) for lifecycle
management and integrates with `flatpak-builder` under the hood.

## Basic Usage

```bash
# Initialize a new project
flatcraft init

# Build and package your application
flatcraft pack

# Clean build artifacts
flatcraft clean
```

## Example flatcraft.yaml

```yaml
name: my-app
version: "1.0"
summary: My awesome application
description: |
  A longer description of my application.

app-id: org.example.MyApp
runtime: org.freedesktop.Platform
runtime-version: "24.08"
sdk: org.freedesktop.Sdk
command: my-app

finish-args:
  share:
    - ipc
    - network
  socket:
    - x11
    - wayland
    - pulseaudio

modules:
  - name: my-app
    buildsystem: meson
    sources:
      - type: git
        url: https://github.com/example/my-app.git
        tag: v1.0
```

## Installation

```bash
pip install flatcraft
```

### Prerequisites

- Python 3.10+
- `flatpak-builder` (install with `sudo apt install flatpak-builder`)
- Flatpak runtimes installed for your target platform

## Development

```bash
# Set up the development environment
make setup

# Run tests
make test

# Run linters
make lint

# Format code
make format
```

## License

Flatcraft is released under the [GPL-3.0 license](LICENSE).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and contribution guidelines.
