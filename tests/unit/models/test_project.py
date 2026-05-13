# Copyright 2025 Alex Lowe
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
"""Tests for the flatcraft project model."""

import pytest
from pydantic import ValidationError

from flatcraft.models.project import (
    BuildOptions,
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

    def test_module_with_cleanup_field(self):
        module = Module(
            name="my-app",
            cleanup=["*.a", "*.la", "include"],
        )
        assert module.cleanup == ["*.a", "*.la", "include"]

    def test_module_with_build_options(self):
        module = Module(
            name="my-lib",
            **{
                "build-options": {
                    "env": {"CFLAGS": "-O2"},
                    "cflags": "-O3",
                    "build-args": ["-j4"],
                }
            },
        )
        assert module.build_options == BuildOptions(
            env={"CFLAGS": "-O2"},
            cflags="-O3",
            build_args=["-j4"],
        )

    def test_module_with_rename_field(self):
        module = Module(
            name="my-app",
            rename={"old-name": "new-name", "bin/old": "bin/new"},
        )
        assert module.rename == {"old-name": "new-name", "bin/old": "bin/new"}

    def test_nested_modules(self):
        """Test that modules can have nested modules."""
        inner_module = Module(
            name="inner-lib",
            buildsystem=BuildSystem.AUTOTOOLS,
            sources=[
                Source(
                    type=SourceType.GIT,
                    url="https://github.com/example/inner.git",
                    tag="v1.0",
                )
            ],
        )
        outer_module = Module(
            name="outer-app",
            buildsystem=BuildSystem.MESON,
            modules=[inner_module],
            sources=[
                Source(
                    type=SourceType.GIT,
                    url="https://github.com/example/outer.git",
                    tag="v2.0",
                )
            ],
        )
        assert len(outer_module.modules) == 1
        assert outer_module.modules[0].name == "inner-lib"

    def test_all_buildsystems_supported(self):
        """Test that all BuildSystem enum values can be used."""
        for buildsystem in BuildSystem:
            module = Module(name="test", buildsystem=buildsystem)
            assert module.buildsystem == buildsystem


class TestProject:
    """Tests for the Project model."""

    def test_valid_app_id_basic(self):
        """Test that valid app_id values are accepted."""
        valid_app_ids = [
            "org.example.App",
            "com.example.MyApp",
            "io.github.user.app",
            "org.gnome.Calendar",
            "org.example_app.MyApp",
        ]
        for app_id in valid_app_ids:
            project = Project(
                name="test",
                app_id=app_id,
                runtime="org.freedesktop.Platform",
                runtime_version="23.08",
                sdk="org.freedesktop.Sdk",
                command="myapp",
                modules=[],
                platforms={"amd64": {}},
                parts={},
            )
            assert project.app_id == app_id

    def test_invalid_app_id_too_few_segments(self):
        """Test that app_id with fewer than 3 segments is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            Project(
                name="test",
                app_id="org.example",
                runtime="org.freedesktop.Platform",
                runtime_version="23.08",
                sdk="org.freedesktop.Sdk",
                command="myapp",
                modules=[],
                platforms={"amd64": {}},
                parts={},
            )
        assert "at least 3 segments" in str(exc_info.value)

    def test_invalid_app_id_invalid_segment(self):
        """Test that app_id with invalid segments is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            Project(
                name="test",
                app_id="org..example",
                runtime="org.freedesktop.Platform",
                runtime_version="23.08",
                sdk="org.freedesktop.Sdk",
                command="myapp",
                modules=[],
                platforms={"amd64": {}},
                parts={},
            )
        assert "cannot be empty" in str(exc_info.value)

    def test_invalid_app_id_starts_with_number(self):
        """Test that app_id segments starting with a number are rejected."""
        with pytest.raises(ValidationError) as exc_info:
            Project(
                name="test",
                app_id="org.9example.App",
                runtime="org.freedesktop.Platform",
                runtime_version="23.08",
                sdk="org.freedesktop.Sdk",
                command="myapp",
                modules=[],
                platforms={"amd64": {}},
                parts={},
            )
        assert "not a valid identifier" in str(exc_info.value)

    def test_valid_runtime_version(self):
        """Test that valid runtime_version values are accepted."""
        valid_versions = ["23.08", "1.0", "45.0", "3.38"]
        for version in valid_versions:
            project = Project(
                name="test",
                app_id="org.example.App",
                runtime="org.freedesktop.Platform",
                runtime_version=version,
                sdk="org.freedesktop.Sdk",
                command="myapp",
                modules=[],
                platforms={"amd64": {}},
                parts={},
            )
            assert project.runtime_version == version

    def test_invalid_runtime_version(self):
        """Test that invalid runtime_version values are rejected."""
        invalid_versions = ["not-a-version", "1.2.3.4.5", "v1.0", "1.0-beta"]
        for version in invalid_versions:
            with pytest.raises(ValidationError):
                Project(
                    name="test",
                    app_id="org.example.App",
                    runtime="org.freedesktop.Platform",
                    runtime_version=version,
                    sdk="org.freedesktop.Sdk",
                    command="myapp",
                    modules=[],
                    platforms={"amd64": {}},
                    parts={},
                )

    def test_app_id_with_alias(self):
        """Test that app_id can be populated using the 'app-id' alias."""
        project = Project(
            name="test",
            **{
                "app-id": "org.example.App",
                "runtime": "org.freedesktop.Platform",
                "runtime-version": "23.08",
                "sdk": "org.freedesktop.Sdk",
                "command": "myapp",
                "modules": [],
                "platforms": {"amd64": {}},
                "parts": {},
            },
        )
        assert project.app_id == "org.example.App"

    def test_runtime_version_with_alias(self):
        """Test that runtime_version can be populated using the 'runtime-version' alias."""
        project = Project(
            name="test",
            app_id="org.example.App",
            runtime="org.freedesktop.Platform",
            **{
                "runtime-version": "23.08",
                "sdk": "org.freedesktop.Sdk",
                "command": "myapp",
                "modules": [],
                "platforms": {"amd64": {}},
                "parts": {},
            },
        )
        assert project.runtime_version == "23.08"

