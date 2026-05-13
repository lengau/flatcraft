# Flatcraft

[![CI Status](https://github.com/lengau/flatcraft/actions/workflows/ci.yml/badge.svg)](https://github.com/lengau/flatcraft/actions)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL%203.0-blue.svg)](LICENSE)

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

## How it works

Flatcraft simplifies the Flatpak development workflow by:

1. **Reading `flatcraft.yaml`** - You define your application's metadata, modules, and build configuration in a simple YAML format
2. **Generating Flatpak manifest** - Flatcraft transforms your `flatcraft.yaml` into a complete Flatpak manifest that flatpak-builder understands
3. **Building with flatpak-builder** - The generated manifest is passed to `flatpak-builder`, which orchestrates the full build process and creates the Flatpak bundle
4. **Packaging** - The resulting Flatpak is ready for distribution

```
flatcraft.yaml → Flatcraft → Flatpak manifest → flatpak-builder → .flatpak
```

## Supported build systems

Flatcraft supports the following build systems through the `buildsystem` field in module definitions:

| Build System | Support | Notes |
|-------------|---------|-------|
| autotools | ✓ | Standard autotools (`./configure`, `make`, `make install`) |
| cmake | ✓ | CMake-based projects |
| cmake-ninja | ✓ | CMake projects configured to generate Ninja build files |
| meson | ✓ | Full support for Meson-based projects |
| qmake | ✓ | Qt projects using qmake |
| simple | ✓ | Manual build commands via `build-commands` |

For more details on module configuration, see the [Example flatcraft.yaml](#example-flatcraftyaml) section.

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
