# Copyright 2025 Alex Lowe
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
"""Tests for flatcraft custom exceptions."""

from __future__ import annotations

import pytest
from craft_application.errors import CraftError
from flatcraft.errors import FlatcraftError, FlatpakBuilderError, ManifestError


class TestFlatcraftError:
    """Tests for the FlatcraftError base exception."""

    def test_flatcraft_error_instantiation(self) -> None:
        """Test that FlatcraftError can be instantiated with a message."""
        message = "Test flatcraft error"
        error = FlatcraftError(message)
        assert str(error) == message

    def test_flatcraft_error_with_empty_message(self) -> None:
        """Test that FlatcraftError can be instantiated with empty message."""
        error = FlatcraftError("")
        assert str(error) == ""

    def test_flatcraft_error_inheritance(self) -> None:
        """Test that FlatcraftError inherits from CraftError."""
        error = FlatcraftError("Test")
        assert isinstance(error, CraftError)


class TestFlatpakBuilderError:
    """Tests for the FlatpakBuilderError exception."""

    def test_flatpak_builder_error_instantiation(self) -> None:
        """Test that FlatpakBuilderError can be instantiated with a message."""
        message = "flatpak-builder failed"
        error = FlatpakBuilderError(message)
        assert str(error) == message

    def test_flatpak_builder_error_with_long_message(self) -> None:
        """Test that FlatpakBuilderError handles long messages."""
        message = "flatpak-builder failed with detailed error:\nLine 1\nLine 2"
        error = FlatpakBuilderError(message)
        assert str(error) == message

    def test_flatpak_builder_error_inheritance(self) -> None:
        """Test that FlatpakBuilderError inherits from FlatcraftError."""
        error = FlatpakBuilderError("Test")
        assert isinstance(error, FlatcraftError)


class TestManifestError:
    """Tests for the ManifestError exception."""

    def test_manifest_error_instantiation(self) -> None:
        """Test that ManifestError can be instantiated with a message."""
        message = "Manifest generation failed"
        error = ManifestError(message)
        assert str(error) == message

    def test_manifest_error_with_details(self) -> None:
        """Test that ManifestError can be instantiated with detailed message."""
        message = "Failed to write manifest: Permission denied"
        error = ManifestError(message)
        assert str(error) == message

    def test_manifest_error_inheritance(self) -> None:
        """Test that ManifestError inherits from FlatcraftError."""
        error = ManifestError("Test")
        assert isinstance(error, FlatcraftError)


class TestErrorHierarchy:
    """Tests for the error exception hierarchy."""

    def test_all_errors_are_exceptions(self) -> None:
        """Test that all custom errors are proper Exception subclasses."""
        assert issubclass(FlatcraftError, Exception)
        assert issubclass(FlatpakBuilderError, Exception)
        assert issubclass(ManifestError, Exception)

    def test_error_hierarchy(self) -> None:
        """Test the inheritance hierarchy."""
        assert issubclass(FlatpakBuilderError, FlatcraftError)
        assert issubclass(ManifestError, FlatcraftError)

    def test_can_raise_and_catch_errors(self) -> None:
        """Test that errors can be raised and caught properly."""
        with pytest.raises(FlatcraftError):
            raise ManifestError("Test error")

        with pytest.raises(FlatcraftError):
            raise FlatpakBuilderError("Test error")
