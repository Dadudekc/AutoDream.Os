#!/usr/bin/env python3
"""Orchestrate web development environment setup."""
from __future__ import annotations

from pathlib import Path
import sys

# Ensure project root on path for absolute imports when executed directly
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.setup.setup_web_environment import WebEnvironmentSetup
from scripts.setup.setup_web_dependencies import WebDependencyInstaller
from scripts.setup.setup_web_configuration import WebConfigurator
from scripts.setup.setup_web_validation import WebSetupValidator


def main() -> None:
    """Run the complete web development environment setup."""
    project_root = PROJECT_ROOT

    env = WebEnvironmentSetup(project_root)
    if not env.check_python_version():
        return
    if not env.create_virtual_environment():
        return
    python_path, pip_path = env.activate_virtual_environment()

    deps = WebDependencyInstaller(pip_path, python_path, project_root)
    if not deps.install_core_dependencies():
        return
    if not deps.setup_webdriver_managers():
        return

    config = WebConfigurator(project_root)
    config.create_directory_structure()
    config.create_config_files()

    validator = WebSetupValidator(python_path, project_root)
    if not validator.run_import_tests():
        return

    print("🎉 Web development environment setup complete!")


if __name__ == "__main__":  # pragma: no cover - script entry point
    main()
