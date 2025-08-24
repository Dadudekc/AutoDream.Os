import importlib.util
from pathlib import Path


def load_cleanup():
    spec = importlib.util.spec_from_file_location(
        "cleanup", Path(__file__).resolve().parents[2] / "src/ai_ml/testing/cleanup.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.CleanupManager


def test_cleanup(tmp_path):
    file_path = tmp_path / "temp.txt"
    file_path.write_text("data")
    CleanupManager = load_cleanup()
    cleaner = CleanupManager()
    removed = cleaner.cleanup([str(file_path)])
    assert removed == 1
    assert not file_path.exists()
