"""Fixtures for file utility tests."""
from typing import Any, Dict, Generator
from unittest.mock import patch

import pytest


@pytest.fixture(scope="function")
def mock_file_system() -> Generator[Dict[str, Any], None, None]:
    """Provide mock file system for testing."""
    mock_fs: Dict[str, Any] = {"files": {}, "directories": set(), "permissions": {}}

    with patch("pathlib.Path.exists") as mock_exists, patch(
        "pathlib.Path.is_file"
    ) as mock_is_file, patch("pathlib.Path.is_dir") as mock_is_dir, patch(
        "builtins.open"
    ) as mock_open:

        def exists_side_effect(path):
            path_str = str(path)
            return path_str in mock_fs["files"] or path_str in mock_fs["directories"]

        def is_file_side_effect(path):
            path_str = str(path)
            return path_str in mock_fs["files"]

        def is_dir_side_effect(path):
            path_str = str(path)
            return path_str in mock_fs["directories"]

        mock_exists.side_effect = exists_side_effect
        mock_is_file.side_effect = is_file_side_effect
        mock_is_dir.side_effect = is_dir_side_effect

        yield mock_fs
