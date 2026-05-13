# Copyright 2025 Alex Lowe
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
"""Tests for the flatcraft project model."""

import pytest

from flatcraft.models.project import (
    BuildSystem,
    Module,
    Project,
    Source,
    SourceType,
)


class TestSource:
    """Tests for the Source model."""

    def test_git_source(self):
        source = Source(
            type=SourceType.GIT,
            url="https://github.com/example/app.git",
            tag="v1.0",
        )
        assert source.type == SourceType.GIT
        assert source.url == "https://github.com/example/app.git"
        assert source.tag == "v1.0"

    def test_archive_source(self):
        source = Source(
            type=SourceType.ARCHIVE,
            url="https://example.com/app-1.0.tar.gz",
            sha256="abc123",
        )
        assert source.type == SourceType.ARCHIVE
        assert source.sha256 == "abc123"


class TestModule:
    """Tests for the Module model."""

    def test_simple_module(self):
        module = Module(
            name="my-app",
            buildsystem=BuildSystem.MESON,
            sources=[
                Source(
                    type=SourceType.GIT,
                    url="https://github.com/example/app.git",
                    tag="v1.0",
                )
            ],
        )
        assert module.name == "my-app"
        assert module.buildsystem == BuildSystem.MESON
        assert len(module.sources) == 1

    def test_module_default_buildsystem(self):
        module = Module(name="lib")
        assert module.buildsystem == BuildSystem.AUTOTOOLS

    def test_module_with_config_opts(self):
        module = Module(
            name="my-lib",
            buildsystem=BuildSystem.CMAKE,
            **{"config-opts": ["-DCMAKE_BUILD_TYPE=Release"]},
        )
        assert module.config_opts == ["-DCMAKE_BUILD_TYPE=Release"]
