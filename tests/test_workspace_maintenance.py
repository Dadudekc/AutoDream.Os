from pathlib import Path

from src.workspace_maintenance.orchestrator import WorkspaceMaintenanceOrchestrator


def test_maintenance_orchestrator(tmp_path: Path) -> None:
    (tmp_path / "example.txt").write_text("data")
    orchestrator = WorkspaceMaintenanceOrchestrator(tmp_path)
    report = orchestrator.run()
    assert report["files_scanned"] == 1
    assert report["health"]["status"] == "healthy"
    assert report["remediation"] == ["checked_1_files"]
