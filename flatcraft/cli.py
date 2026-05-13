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
"""Flatcraft CLI entry point."""

from __future__ import annotations

import sys

from craft_application import ServiceFactory

from flatcraft.application import APP_METADATA, Flatcraft


def main() -> int:
    """Run the flatcraft CLI."""
    app = Flatcraft(app=APP_METADATA, services=ServiceFactory(app=APP_METADATA))
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
