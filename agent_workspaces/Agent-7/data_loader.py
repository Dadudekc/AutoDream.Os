#!/usr/bin/env python3
"""Utility helpers for locating project resources."""

from pathlib import Path


def get_project_root() -> Path:
    """Return the project root directory.

    At the moment this simply returns the current working directory, but having
    this in its own module allows for future expansion such as reading from
    configuration files or environment variables.
    """
    return Path.cwd()
