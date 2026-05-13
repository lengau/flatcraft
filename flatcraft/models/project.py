# This file is part of flatcraft.
#
# Copyright 2025 Alex Lowe
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Flatcraft project model - defines the flatcraft.yaml schema."""

from __future__ import annotations

import enum
import re
from typing import Annotated

import pydantic
from craft_application.models import CraftBaseModel
from craft_application.models import Project as CraftProject

MIN_APP_ID_SEGMENTS = 3


class BuildSystem(str, enum.Enum):
    """Supported Flatpak module build systems."""

    AUTOTOOLS = "autotools"
    CMAKE = "cmake"
    CMAKE_NINJA = "cmake-ninja"
    MESON = "meson"
    SIMPLE = "simple"
    QMAKE = "qmake"


class SourceType(str, enum.Enum):
    """Supported source types for Flatpak modules."""

    GIT = "git"
    ARCHIVE = "archive"
    FILE = "file"
    DIR = "dir"
    PATCH = "patch"


class Source(CraftBaseModel):
    """A source for a Flatpak module.

    Represents a source location for downloading or including source code
    and build artifacts for a Flatpak module.
    """

    type: SourceType
    url: str | None = None
    path: str | None = None
    tag: str | None = None
    branch: str | None = None
    commit: str | None = None
    sha256: str | None = None


class BuildOptions(CraftBaseModel):
    """Build-time options for a Flatpak module."""

    model_config = pydantic.ConfigDict(populate_by_name=True)

    cflags: str | None = None
    cxxflags: str | None = None
    ldflags: str | None = None
    prefix: str | None = None
    env: dict[str, str] = pydantic.Field(default_factory=dict)
    build_args: list[str] = pydantic.Field(default_factory=list, alias="build-args")
    config_opts: list[str] = pydantic.Field(default_factory=list, alias="config-opts")
    append_path: str | None = pydantic.Field(default=None, alias="append-path")
    prepend_path: str | None = pydantic.Field(default=None, alias="prepend-path")


class Module(CraftBaseModel):
    """A module to build within the Flatpak.

    Represents a single module that will be built as part of the Flatpak,
    including its build system, configuration, sources, and any nested modules.
    """

    model_config = pydantic.ConfigDict(populate_by_name=True)

    name: str
    buildsystem: BuildSystem = BuildSystem.AUTOTOOLS
    config_opts: list[str] = pydantic.Field(default_factory=list, alias="config-opts")
    build_commands: list[str] = pydantic.Field(
        default_factory=list, alias="build-commands"
    )
    build_options: BuildOptions | None = pydantic.Field(
        default=None, alias="build-options"
    )
    cleanup: list[str] = pydantic.Field(default_factory=list)
    rename: dict[str, str] = pydantic.Field(default_factory=dict)
    sources: list[Source] = pydantic.Field(default_factory=list)
    modules: list[Module] = pydantic.Field(default_factory=list)


class FinishArgs(CraftBaseModel):
    """Flatpak finish-args (sandbox permissions).

    Defines the sandbox permissions and capabilities for the Flatpak application,
    including file system access, device access, and socket access.
    """

    model_config = pydantic.ConfigDict(populate_by_name=True)

    share: list[str] = pydantic.Field(default_factory=list)
    socket: list[str] = pydantic.Field(default_factory=list)
    filesystem: list[str] = pydantic.Field(default_factory=list)
    device: list[str] = pydantic.Field(default_factory=list)


class Project(CraftProject):
    """The flatcraft project model, representing a flatcraft.yaml file.

    This model represents the complete configuration of a Flatpak application
    project, including metadata, runtime configuration, modules, and permissions.
    """

    model_config = pydantic.ConfigDict(populate_by_name=True)

    app_id: Annotated[str, pydantic.Field(alias="app-id")]
    runtime: str
    runtime_version: Annotated[str, pydantic.Field(alias="runtime-version")]
    sdk: str
    command: str
    modules: list[Module]
    finish_args: FinishArgs | None = pydantic.Field(default=None, alias="finish-args")

    @pydantic.field_validator("app_id")
    @classmethod
    def validate_app_id(cls, v: str) -> str:
        """Validate that app_id follows reverse-DNS format with at least 3 segments.

        Args:
            v: The app_id value to validate.

        Returns:
            The validated app_id.

        Raises:
            ValueError: If app_id is not in valid reverse-DNS format.

        """
        # Split by dots
        segments = v.split(".")
        if len(segments) < MIN_APP_ID_SEGMENTS:
            raise ValueError(
                f"app_id must have at least 3 segments in reverse-DNS format, got: {v}"
            )

        # Per the D-Bus specification, each segment may contain underscores.
        # First letter must be alphabetic.
        for segment in segments:
            if not segment:
                raise ValueError(f"app_id segments cannot be empty, got: {v}")
            if not re.match(r"^[a-zA-Z][a-zA-Z0-9_\-]*$", segment):
                raise ValueError(
                    f"app_id segment '{segment}' is not a valid identifier. "
                    f"Each segment must start with a letter and contain only "
                    f"alphanumeric characters, underscores, or hyphens, got: {v}"
                )

        return v

    @pydantic.field_validator("runtime_version")
    @classmethod
    def validate_runtime_version(cls, v: str) -> str:
        """Validate that runtime_version is a valid version string.

        Version strings should follow semantic versioning with 1-2 segments
        (e.g., 1.0, 45, 3.38).

        Args:
            v: The runtime_version value to validate.

        Returns:
            The validated runtime_version.

        Raises:
            ValueError: If runtime_version is not a valid version string.

        """
        # Version validation: 1 or 2 numeric segments separated by dots
        # Valid formats: "1", "1.0", "45", "45.0", "3.38"
        if not re.match(r"^\d+(\.\d+)?$", v):
            raise ValueError(
                f"runtime_version must be a valid version string "
                f"(e.g., '1.0', '45.0'), got: {v}"
            )
        return v
