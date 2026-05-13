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
from typing import Annotated

import pydantic
from craft_application.models import CraftBaseModel, Project as CraftProject


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
    """A source for a Flatpak module."""

    type: SourceType
    url: str | None = None
    path: str | None = None
    tag: str | None = None
    branch: str | None = None
    commit: str | None = None
    sha256: str | None = None


class Module(CraftBaseModel):
    """A module to build within the Flatpak."""

    name: str
    buildsystem: BuildSystem = BuildSystem.AUTOTOOLS
    config_opts: list[str] = pydantic.Field(default_factory=list, alias="config-opts")
    build_commands: list[str] = pydantic.Field(
        default_factory=list, alias="build-commands"
    )
    sources: list[Source] = pydantic.Field(default_factory=list)
    modules: list[Module] = pydantic.Field(default_factory=list)


class FinishArgs(CraftBaseModel):
    """Flatpak finish-args (sandbox permissions)."""

    share: list[str] = pydantic.Field(default_factory=list)
    socket: list[str] = pydantic.Field(default_factory=list)
    filesystem: list[str] = pydantic.Field(default_factory=list)
    device: list[str] = pydantic.Field(default_factory=list)


class Project(CraftProject):
    """The flatcraft project model, representing a flatcraft.yaml file."""

    app_id: Annotated[str, pydantic.Field(alias="app-id")]
    runtime: str
    runtime_version: Annotated[str, pydantic.Field(alias="runtime-version")]
    sdk: str
    command: str
    modules: list[Module]
    finish_args: FinishArgs | None = pydantic.Field(
        default=None, alias="finish-args"
    )
