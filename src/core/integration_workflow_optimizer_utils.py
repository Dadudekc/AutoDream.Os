"""
Integration Workflow Optimizer Utils - V2 Compliant
===================================================

Utility functions for integration workflow optimization.
V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions, KISS principle
"""

import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

from .integration_workflow_optimizer_models import (
    IntegrationWorkflow,
    SeamlessConnection,
    AutomationTool,
    IntegrationReport
)


class IntegrationWorkflowUtils:
    """Utility functions for integration workflow optimization."""
    
    def __init__(self):
        """Initialize integration workflow utils."""
        self.config_path = Path("config/integration_workflows.json")
    
    def save_workflow_configuration(self, workflows: List[IntegrationWorkflow]) -> bool:
        """Save workflow configuration to file."""
        try:
            config_data = {
                "workflows": [
                    {
                        "workflow_id": w.workflow_id,
                        "pattern": w.pattern.value,
                        "source_service": w.source_service,
                        "target_service": w.target_service,
                        "connection_type": w.connection_type,
                        "automation_level": w.automation_level,
                        "status": w.status
                    }
                    for w in workflows
                ]
            }
            
            self.config_path.parent.mkdir(exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            return True
        except Exception:
            return False
    
    def load_workflow_configuration(self) -> List[IntegrationWorkflow]:
        """Load workflow configuration from file."""
        try:
            if not self.config_path.exists():
                return []
            
            with open(self.config_path, 'r') as f:
                config_data = json.load(f)
            
            workflows = []
            for w_data in config_data.get("workflows", []):
                workflow = IntegrationWorkflow(
                    workflow_id=w_data["workflow_id"],
                    pattern=w_data["pattern"],
                    source_service=w_data["source_service"],
                    target_service=w_data["target_service"],
                    connection_type=w_data["connection_type"],
                    automation_level=w_data["automation_level"],
                    status=w_data.get("status", "active")
                )
                workflows.append(workflow)
            
            return workflows
        except Exception:
            return []
    
    def validate_workflow_configuration(self, workflow: IntegrationWorkflow) -> bool:
        """Validate workflow configuration."""
        required_fields = [
            workflow.workflow_id,
            workflow.source_service,
            workflow.target_service,
            workflow.connection_type,
            workflow.automation_level
        ]
        
        return all(field and field.strip() for field in required_fields)
    
    def test_workflow_connection(self, connection: SeamlessConnection) -> bool:
        """Test workflow connection."""
        try:
            # Simulate connection test
            test_command = f"ping -c 1 {connection.destination}"
            result = subprocess.run(
                test_command.split(),
                capture_output=True,
                text=True,
                timeout=connection.timeout
            )
            
            return result.returncode == 0
        except Exception:
            return False
    
    def generate_workflow_documentation(self, workflows: List[IntegrationWorkflow]) -> str:
        """Generate workflow documentation."""
        doc_lines = [
            "# Integration Workflow Documentation",
            "",
            f"Total Workflows: {len(workflows)}",
            "",
            "## Workflow Details",
            ""
        ]
        
        for workflow in workflows:
            doc_lines.extend([
                f"### {workflow.workflow_id}",
                f"- Pattern: {workflow.pattern.value}",
                f"- Source: {workflow.source_service}",
                f"- Target: {workflow.target_service}",
                f"- Connection: {workflow.connection_type}",
                f"- Automation: {workflow.automation_level}",
                f"- Status: {workflow.status}",
                ""
            ])
        
        return "\n".join(doc_lines)
    
    def export_integration_report(self, report: IntegrationReport, file_path: str) -> bool:
        """Export integration report to file."""
        try:
            report_data = {
                "report_id": report.report_id,
                "total_workflows": report.total_workflows,
                "active_connections": report.active_connections,
                "automation_coverage": report.automation_coverage,
                "performance_score": report.performance_score,
                "recommendations": report.recommendations
            }
            
            with open(file_path, 'w') as f:
                json.dump(report_data, f, indent=2)
            
            return True
        except Exception:
            return False
