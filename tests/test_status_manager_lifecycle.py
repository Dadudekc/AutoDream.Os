import asyncio
import importlib.util
import json
import sys
import types
from pathlib import Path


def _load_status_manager() -> tuple[type, type]:
    repo_root = Path(__file__).resolve().parents[1]
    src_path = repo_root / "src"
    core_path = src_path / "core"
    managers_path = core_path / "managers"

    sys.modules.setdefault("src", types.ModuleType("src")).__path__ = [str(src_path)]
    sys.modules.setdefault("src.core", types.ModuleType("src.core")).__path__ = [
        str(core_path)
    ]
    sys.modules.setdefault(
        "src.core.managers", types.ModuleType("src.core.managers")
    ).__path__ = [str(managers_path)]

    spec = importlib.util.spec_from_file_location(
        "src.core.managers.status_manager", managers_path / "status_manager.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["src.core.managers.status_manager"] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.StatusManager, module.StatusLevel


StatusManager, StatusLevel = _load_status_manager()


def test_status_manager_start_stop():
    manager = StatusManager()
    asyncio.run(manager._initialize_manager())

    # Ensure resource initialized
    assert manager.reporter._file is not None
    assert not manager.reporter._file.closed
    assert manager.reporter.path is not None

    # Add a sample status
    manager.add_status("component", "ok", StatusLevel.SUCCESS, "message")

    asyncio.run(manager._shutdown_manager())

    # Resource should be released and final report written
    assert manager.reporter._file is None
    assert manager.reporter.path is not None
    with open(manager.reporter.path) as f:
        data = json.load(f)
    assert data["total_components"] == 1

    # Cleanup created report file
    Path(manager.reporter.path).unlink()
