import os
from pathlib import Path

from tools.modularizer import backup, analysis, generator, reporting
from tools.modularizer import (
    unified_learning_engine,
    fsm_compliance_integration,
    validation_manager,
    base_manager,
)


def test_backup_creates_copy(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    (src / "example.txt").write_text("data", encoding="utf-8")
    os.chdir(tmp_path)
    backup_dir = backup.create_backup(src)
    assert backup_dir.exists()
    assert (backup_dir / "example.txt").read_text(encoding="utf-8") == "data"


def test_analysis_targets():
    targets = analysis.get_targets()
    assert len(targets) == 4


def test_generator_writes_file(tmp_path):
    target = tmp_path / "out.txt"
    generator.write_file(target, "hello")
    assert target.read_text(encoding="utf-8") == "hello"


def test_reporting_structure():
    report = reporting.generate_report()
    assert report["contract_id"] == "MODULAR-001"
    assert report["files_modularized"][0]["original_file"] == "unified_learning_engine.py"


def _setup_src(tmp_path: Path):
    root = tmp_path / "src"
    root.mkdir(parents=True)
    return root


def test_unified_learning_engine(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _setup_src(tmp_path)
    unified_learning_engine.modularize()
    assert (
        tmp_path
        / "src/core/learning/core/learning_engine_core.py"
    ).exists()


def test_fsm_compliance_integration(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _setup_src(tmp_path)
    fsm_compliance_integration.modularize()
    assert (
        tmp_path
        / "src/core/fsm/compliance/compliance_core.py"
    ).exists()


def test_validation_manager(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _setup_src(tmp_path)
    validation_manager.modularize()
    assert (
        tmp_path
        / "src/core/validation/validation_core.py"
    ).exists()


def test_base_manager(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _setup_src(tmp_path)
    base_manager.modularize()
    assert (
        tmp_path
        / "src/core/managers/base_manager_core.py"
    ).exists()
