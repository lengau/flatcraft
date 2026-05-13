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
import subprocess
from pathlib import Path
from typing import Any

from flatcraft.errors import FlatpakBuilderError, ManifestError
from flatcraft.models.project import Module, Project, Source


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
        finish_args: list[str] = []
        for share in project.finish_args.share:
            finish_args.append(f"--share={share}")
        for socket in project.finish_args.socket:
            finish_args.append(f"--socket={socket}")
        for fs in project.finish_args.filesystem:
            finish_args.append(f"--filesystem={fs}")
        for device in project.finish_args.device:
            finish_args.append(f"--device={device}")
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
        subprocess.run(cmd, check=True, capture_output=True, text=True)  # noqa: S603
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
        subprocess.run(cmd, check=True, capture_output=True, text=True)  # noqa: S603
    except subprocess.CalledProcessError as e:
        msg = f"Failed to create bundle:\n{e.stderr}"
        raise FlatpakBuilderError(msg) from e
    return bundle_path
