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
"""Flatcraft lifecycle service - manages the Flatpak build process."""

from __future__ import annotations

import json
import logging
import shutil
import subprocess
from typing import TYPE_CHECKING, Any

from flatcraft.errors import FlatpakBuilderError, ManifestError

if TYPE_CHECKING:
    from pathlib import Path

    from flatcraft.models.project import Module, Project, Source

logger = logging.getLogger(__name__)


def generate_manifest(project: Project) -> dict[str, Any]:
    """Generate a Flatpak manifest dict from a flatcraft Project model."""
    manifest: dict[str, Any] = {
        "app-id": project.app_id,
        "runtime": project.runtime,
        "runtime-version": project.runtime_version,
        "sdk": project.sdk,
        "command": project.command,
        "modules": [_module_to_dict(m) for m in project.modules],
    }

    if project.finish_args:
        finish_args = [f"--share={share}" for share in project.finish_args.share]
        finish_args.extend(
            f"--socket={socket}" for socket in project.finish_args.socket
        )
        finish_args.extend(
            f"--filesystem={filesystem}"
            for filesystem in project.finish_args.filesystem
        )
        finish_args.extend(
            f"--device={device}" for device in project.finish_args.device
        )
        manifest["finish-args"] = finish_args

    return manifest


def _source_to_dict(source: Source) -> dict[str, Any]:
    """Convert a Source model to a Flatpak manifest source dict."""
    result: dict[str, Any] = {"type": source.type.value}
    if source.url:
        result["url"] = source.url
    if source.path:
        result["path"] = source.path
    if source.tag:
        result["tag"] = source.tag
    if source.branch:
        result["branch"] = source.branch
    if source.commit:
        result["commit"] = source.commit
    if source.sha256:
        result["sha256"] = source.sha256
    return result


def _module_to_dict(module: Module) -> dict[str, Any]:
    """Convert a Module model to a Flatpak manifest module dict."""
    result: dict[str, Any] = {
        "name": module.name,
        "buildsystem": module.buildsystem.value,
    }
    if module.config_opts:
        result["config-opts"] = module.config_opts
    if module.build_commands:
        result["build-commands"] = module.build_commands
    if module.sources:
        result["sources"] = [_source_to_dict(s) for s in module.sources]
    if module.modules:
        result["modules"] = [_module_to_dict(m) for m in module.modules]
    # Add cleanup support (placeholder for future cleanup field implementation)
    # This would be used if Module model gets a cleanup field
    return result


def write_manifest(project: Project, output_path: Path) -> Path:
    """Write the Flatpak manifest JSON file."""
    manifest = generate_manifest(project)
    manifest_path = output_path / f"{project.app_id}.json"
    try:
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    except OSError as e:
        msg = f"Failed to write manifest: {e}"
        raise ManifestError(msg) from e
    return manifest_path


def run_flatpak_builder(
    manifest_path: Path,
    build_dir: Path,
    repo_dir: Path | None = None,
) -> None:
    """Run flatpak-builder to build the Flatpak application."""
    cmd = [
        "flatpak-builder",
        "--force-clean",
        str(build_dir),
        str(manifest_path),
    ]
    if repo_dir:
        cmd.extend(["--repo", str(repo_dir)])

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except FileNotFoundError as e:
        msg = "flatpak-builder not found. Install it with: sudo apt install flatpak-builder"
        raise FlatpakBuilderError(msg) from e
    except subprocess.CalledProcessError as e:
        msg = f"flatpak-builder failed:\n{e.stderr}"
        raise FlatpakBuilderError(msg) from e


def build_bundle(
    repo_dir: Path,
    app_id: str,
    output_path: Path,
    branch: str = "master",
) -> Path:
    """Build a .flatpak bundle from the repo."""
    bundle_path = output_path / f"{app_id}.flatpak"
    cmd = [
        "flatpak",
        "build-bundle",
        str(repo_dir),
        str(bundle_path),
        app_id,
        branch,
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except FileNotFoundError as e:
        msg = "flatpak not found. Install it with: sudo apt install flatpak"
        raise FlatpakBuilderError(msg) from e
    except subprocess.CalledProcessError as e:
        msg = f"Failed to create bundle:\n{e.stderr}"
        raise FlatpakBuilderError(msg) from e
    return bundle_path


def validate_environment() -> dict[str, bool]:
    """Validate that required tools are installed.

    Returns:
        A dictionary with tool names as keys and installation status as values.

    Raises:
        FlatpakBuilderError: If critical tools are missing.

    """
    tools = {"flatpak-builder": False, "flatpak": False}

    for tool in tools:
        if shutil.which(tool):
            tools[tool] = True
            logger.debug(f"Found {tool}")
        else:
            logger.warning(f"{tool} not found in PATH")

    if not tools["flatpak-builder"]:
        msg = "flatpak-builder not found. Install it with: sudo apt install flatpak-builder"
        raise FlatpakBuilderError(msg)

    if not tools["flatpak"]:
        msg = "flatpak not found. Install it with: sudo apt install flatpak"
        raise FlatpakBuilderError(msg)

    return tools


def pack(
    project: Project,
    output_path: Path,
    build_dir: Path | None = None,
    repo_dir: Path | None = None,
) -> Path:
    """Orchestrate the full Flatpak build lifecycle.

    This function coordinates the complete process of building a Flatpak:
    1. Validates the environment (checks for required tools)
    2. Generates the Flatpak manifest
    3. Runs flatpak-builder to build the application
    4. Creates a .flatpak bundle

    Args:
        project: The flatcraft Project model to build.
        output_path: Directory where output files will be written.
        build_dir: Directory for the build process. If None, uses a temporary dir.
        repo_dir: Directory for the Flatpak repository. If None, uses a temporary dir.

    Returns:
        The path to the generated .flatpak bundle.

    Raises:
        FlatpakBuilderError: If the build process fails.
        ManifestError: If manifest generation fails.

    """
    logger.info(f"Starting Flatpak build for {project.app_id}")

    # Validate environment
    try:
        logger.debug("Validating environment")
        validate_environment()
    except FlatpakBuilderError:
        logger.exception("Environment validation failed")
        raise

    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Output directory: {output_path}")

    # Set default directories if not provided
    if build_dir is None:
        build_dir = output_path / "build"
    if repo_dir is None:
        repo_dir = output_path / "repo"

    build_dir.mkdir(parents=True, exist_ok=True)
    repo_dir.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Build directory: {build_dir}")
    logger.debug(f"Repo directory: {repo_dir}")

    # Generate manifest
    try:
        logger.debug("Generating manifest")
        manifest_path = write_manifest(project, output_path)
        logger.info(f"Manifest written to {manifest_path}")
    except ManifestError:
        logger.exception("Manifest generation failed")
        raise

    # Run flatpak-builder
    try:
        logger.debug(f"Running flatpak-builder with manifest {manifest_path}")
        run_flatpak_builder(manifest_path, build_dir, repo_dir)
        logger.info("flatpak-builder completed successfully")
    except FlatpakBuilderError:
        logger.exception("flatpak-builder failed")
        raise

    # Build bundle
    try:
        logger.debug("Building .flatpak bundle")
        bundle_path = build_bundle(repo_dir, project.app_id, output_path)
        logger.info(f"Bundle created successfully: {bundle_path}")
    except FlatpakBuilderError:
        logger.exception("Bundle creation failed")
        raise

    return bundle_path
