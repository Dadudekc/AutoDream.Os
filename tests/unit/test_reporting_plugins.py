"""Tests for Reporting plugin hooks."""

import importlib.util
import logging
from dataclasses import dataclass
from pathlib import Path


def load_reporting_class():
    spec = importlib.util.spec_from_file_location(
        "reporting", Path(__file__).resolve().parents[2] / "src/core/fsm/execution_engine/reporting.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Reporting


Reporting = load_reporting_class()


@dataclass
class DummyWorkflow:
    workflow_name: str


class DummyReporting(Reporting):
    def __init__(self):
        # Minimal attributes required by Reporting
        self.workflows = {"1": DummyWorkflow("wf")}
        self.logger = logging.getLogger("dummy")
        self.active_workflows = set()
        self.workflow_queue = []


def test_reporting_plugin_extension():
    reporter = DummyReporting()
    reporter.register_report_plugin(
        "custom", lambda data: "custom:" + data["workflow_name"]
    )
    output = reporter.export_workflow_report("1", "custom")
    assert output == "custom:wf"

