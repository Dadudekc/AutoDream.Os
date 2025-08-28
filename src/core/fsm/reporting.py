"""Reporting helpers for FSM compliance integration."""
from __future__ import annotations
from datetime import datetime
from typing import Any, Dict
import json


def generate_report(integration) -> Dict[str, Any]:
    """Build a dictionary report from an FSMComplianceIntegration instance."""
    return {
        "integration_status": integration.integration_status,
        "health_status": integration.get_integration_health(),
        "compliance_workflows": integration.list_compliance_workflows(),
        "mappings": {
            "fsm_to_compliance": integration.fsm_compliance_mapping,
            "compliance_to_fsm": integration.compliance_fsm_mapping,
        },
        "exported_at": datetime.now().isoformat(),
    }


def export_report(report_data: Dict[str, Any], fmt: str = "json") -> str:
    """Serialize a report to the requested format."""
    if fmt.lower() != "json":
        raise ValueError(f"Report format '{fmt}' not supported")
    return json.dumps(report_data, indent=2, default=str)


__all__ = ["generate_report", "export_report"]
