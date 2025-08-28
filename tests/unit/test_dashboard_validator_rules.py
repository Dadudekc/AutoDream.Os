from src.core.unified_dashboard_validator import UnifiedDashboardValidator


def test_deliverable_rule_detects_missing_file(tmp_path):
    validator = UnifiedDashboardValidator(base_path=tmp_path)
    deliverables = ["missing.txt"]
    rules = {"deliverables_exist": True, "devlog_entries_found": False}
    status, discrepancies, evidence, confidence = validator._apply_task_validation_rules(
        deliverables, 0, "agent", "task", tmp_path, rules
    )
    assert status == "PARTIAL"
    assert "Deliverable not found" in discrepancies[0]


def test_devlog_rule_detects_insufficient_entries(tmp_path, monkeypatch):
    validator = UnifiedDashboardValidator(base_path=tmp_path)
    monkeypatch.setattr(validator, "_count_devlog_entries", lambda a, t: 0)
    deliverables = []
    rules = {"deliverables_exist": False, "devlog_entries_found": True}
    status, discrepancies, evidence, confidence = validator._apply_task_validation_rules(
        deliverables, 2, "agent", "task", tmp_path, rules
    )
    assert status == "PARTIAL"
    assert "Insufficient devlog entries" in discrepancies[0]

def test_deliverable_rule_is_skipped_when_disabled(tmp_path):
    validator = UnifiedDashboardValidator(base_path=tmp_path)
    deliverables = ["missing.txt"]
    rules = {"deliverables_exist": False, "devlog_entries_found": False}
    status, discrepancies, evidence, confidence = validator._apply_task_validation_rules(
        deliverables, 0, "agent", "task", tmp_path, rules
    )
    assert status == "VALID"
    assert not discrepancies
