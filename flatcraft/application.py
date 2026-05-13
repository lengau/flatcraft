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
"""Flatcraft application definition."""

from __future__ import annotations

import craft_application

from flatcraft import models


class Flatcraft(craft_application.Application):
    """Flatcraft application class."""

    @override
    def _get_app_plugins(self) -> dict[str, craft_application.PluginType]:
        """Return application-specific plugins."""
        return {}


from typing_extensions import override  # noqa: E402

APP_METADATA = craft_application.AppMetadata(
    name="flatcraft",
    summary="A craft tool for creating Flatpak packages",
    ProjectClass=models.Project,
)
