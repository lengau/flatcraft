# Copyright 2025 Alex Lowe
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
"""Tests for the flatcraft application."""

import flatcraft


class TestVersion:
    """Tests for version handling."""

    def test_version_exists(self, project_main_module):
        assert hasattr(project_main_module, "__version__")

    def test_version_is_string(self):
        assert isinstance(flatcraft.__version__, str)
