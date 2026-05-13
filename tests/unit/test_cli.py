# Copyright 2025 Alex Lowe
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
"""Tests for the flatcraft CLI module."""

from __future__ import annotations

from unittest import mock

from flatcraft.cli import main


class TestCLI:
    """Tests for the CLI module."""

    def test_main_creates_flatcraft_app(self) -> None:
        """Test that main creates a Flatcraft application instance."""
        with (
            mock.patch("flatcraft.cli.Flatcraft") as mock_flatcraft,
            mock.patch("flatcraft.cli.APP_METADATA") as mock_metadata,
        ):
            mock_instance = mock.MagicMock()
            mock_instance.run.return_value = 0
            mock_flatcraft.return_value = mock_instance

            main()
            mock_flatcraft.assert_called_once_with(app=mock_metadata, services=None)

    def test_main_calls_app_run(self) -> None:
        """Test that main calls the app.run() method."""
        with mock.patch("flatcraft.cli.Flatcraft") as mock_flatcraft:
            mock_instance = mock.MagicMock()
            mock_instance.run.return_value = 0
            mock_flatcraft.return_value = mock_instance

            main()
            mock_instance.run.assert_called_once()

    def test_main_returns_app_run_result(self) -> None:
        """Test that main returns the result of app.run()."""
        with mock.patch("flatcraft.cli.Flatcraft") as mock_flatcraft:
            mock_instance = mock.MagicMock()
            mock_instance.run.return_value = 42
            mock_flatcraft.return_value = mock_instance

            result = main()
            assert result == 42
