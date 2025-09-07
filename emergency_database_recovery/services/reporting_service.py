#!/usr/bin/env python3
"""
Reporting Service - Emergency Database Recovery System
Provides comprehensive reporting functionality for audit results and recovery actions
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .logging_service import LoggingService


class ReportingService:
    """Comprehensive reporting service for emergency database recovery"""

    def __init__(self):
        self.logger = LoggingService().get_logger("ReportingService")
        self.report_templates = {
            "audit_summary": "audit_summary_{timestamp}.json",
            "recovery_report": "recovery_report_{timestamp}.json",
            "integrity_check": "integrity_check_{timestamp}.json",
            "emergency_alert": "emergency_alert_{timestamp}.json",
        }

    def generate_audit_summary_report(
        self, audit_results: Dict[str, Any], output_dir: Optional[Path] = None
    ) -> Dict[str, Any]:
        """Generate comprehensive audit summary report"""
        timestamp = datetime.now().isoformat()

        report = {
            "report_type": "audit_summary",
            "timestamp": timestamp,
            "audit_metadata": {
                "total_files_analyzed": len(audit_results.get("file_analysis", {})),
                "critical_issues_found": len(audit_results.get("critical_issues", [])),
                "overall_health_score": self._calculate_health_score(audit_results),
                "recommendations_count": len(audit_results.get("recommendations", [])),
            },
            "file_analysis_summary": self._summarize_file_analysis(audit_results),
            "critical_issues": audit_results.get("critical_issues", []),
            "structure_validation": audit_results.get("structure_validation", {}),
            "metadata_consistency": audit_results.get("metadata_consistency", {}),
            "recommendations": audit_results.get("recommendations", []),
            "next_actions": self._generate_next_actions(audit_results),
        }

        # Save report if output directory specified
        if output_dir:
            self._save_report(report, "audit_summary", output_dir)

        self.logger.info(
            f"Generated audit summary report with {report['audit_metadata']['critical_issues_found']} critical issues"
        )
        return report

    def generate_recovery_action_report(
        self,
        recovery_actions: List[Dict[str, Any]],
        status: str,
        output_dir: Optional[Path] = None,
    ) -> Dict[str, Any]:
        """Generate recovery action execution report"""
        timestamp = datetime.now().isoformat()

        report = {
            "report_type": "recovery_action",
            "timestamp": timestamp,
            "recovery_status": status,
            "actions_executed": len(recovery_actions),
            "actions_summary": self._summarize_recovery_actions(recovery_actions),
            "success_rate": self._calculate_success_rate(recovery_actions),
            "time_taken": self._calculate_total_time(recovery_actions),
            "next_steps": self._generate_recovery_next_steps(recovery_actions, status),
        }

        # Save report if output directory specified
        if output_dir:
            self._save_report(report, "recovery_report", output_dir)

        self.logger.info(
            f"Generated recovery action report: {status} - {report['actions_executed']} actions executed"
        )
        return report

    def generate_integrity_check_report(
        self, integrity_results: Dict[str, Any], output_dir: Optional[Path] = None
    ) -> Dict[str, Any]:
        """Generate database integrity check report"""
        timestamp = datetime.now().isoformat()

        report = {
            "report_type": "integrity_check",
            "timestamp": timestamp,
            "integrity_status": integrity_results.get("overall_integrity", False),
            "validation_summary": {
                "files_validated": integrity_results.get("files_validated", 0),
                "files_with_issues": integrity_results.get("files_with_issues", 0),
                "critical_issues": integrity_results.get("critical_issues", 0),
            },
            "backup_status": integrity_results.get("backup_status", {}),
            "cross_reference_issues": integrity_results.get(
                "cross_reference_issues", []
            ),
            "recommendations": integrity_results.get("recommendations", []),
            "risk_assessment": self._assess_integrity_risk(integrity_results),
        }

        # Save report if output directory specified
        if output_dir:
            self._save_report(report, "integrity_check", output_dir)

        self.logger.info(
            f"Generated integrity check report: Overall integrity: {report['integrity_status']}"
        )
        return report

    def generate_emergency_alert_report(
        self,
        alert_type: str,
        severity: str,
        message: str,
        context: Dict[str, Any],
        output_dir: Optional[Path] = None,
    ) -> Dict[str, Any]:
        """Generate emergency alert report"""
        timestamp = datetime.now().isoformat()

        report = {
            "report_type": "emergency_alert",
            "timestamp": timestamp,
            "alert_type": alert_type,
            "severity": severity,
            "message": message,
            "context": context,
            "response_required": severity in ["CRITICAL", "HIGH"],
            "escalation_needed": severity == "CRITICAL",
            "immediate_actions": self._generate_emergency_actions(severity, alert_type),
        }

        # Save report if output directory specified
        if output_dir:
            self._save_report(report, "emergency_alert", output_dir)

        self.logger.warning(
            f"Generated emergency alert report: {alert_type} - {severity} - {message}"
        )
        return report

    def _calculate_health_score(self, audit_results: Dict[str, Any]) -> float:
        """Calculate overall health score from audit results"""
        total_files = len(audit_results.get("file_analysis", {}))
        if total_files == 0:
            return 100.0

        critical_issues = len(audit_results.get("critical_issues", []))
        warnings = len(audit_results.get("warnings", []))

        # Health score calculation: 100 - (critical * 20) - (warnings * 5)
        health_score = 100.0 - (critical_issues * 20) - (warnings * 5)
        return max(0.0, min(100.0, health_score))

    def _summarize_file_analysis(self, audit_results: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize file analysis results"""
        file_analysis = audit_results.get("file_analysis", {})

        summary = {
            "total_files": len(file_analysis),
            "files_exist": 0,
            "files_readable": 0,
            "files_valid_json": 0,
            "files_with_issues": 0,
        }

        for file_info in file_analysis.values():
            if file_info.get("exists", False):
                summary["files_exist"] += 1
            if file_info.get("readable", False):
                summary["files_readable"] += 1
            if file_info.get("valid_json", False):
                summary["files_valid_json"] += 1
            if not file_info.get("valid_json", True):
                summary["files_with_issues"] += 1

        return summary

    def _generate_next_actions(self, audit_results: Dict[str, Any]) -> List[str]:
        """Generate next actions based on audit results"""
        actions = []

        critical_issues = audit_results.get("critical_issues", [])
        if critical_issues:
            actions.append("Immediate: Address all critical issues identified")
            actions.append("Priority: Review and fix file accessibility problems")

        warnings = audit_results.get("warnings", [])
        if warnings:
            actions.append("Review: Address warnings to improve system health")

        if not critical_issues and not warnings:
            actions.append("Maintenance: Schedule regular integrity checks")
            actions.append("Optimization: Review system performance metrics")

        return actions

    def _summarize_recovery_actions(
        self, recovery_actions: List[Dict[str, Any]]
    ) -> Dict[str, int]:
        """Summarize recovery actions by type and status"""
        summary = {
            "total_actions": len(recovery_actions),
            "successful": 0,
            "failed": 0,
            "in_progress": 0,
        }

        for action in recovery_actions:
            status = action.get("status", "unknown")
            if status == "success":
                summary["successful"] += 1
            elif status == "failed":
                summary["failed"] += 1
            elif status == "in_progress":
                summary["in_progress"] += 1

        return summary

    def _calculate_success_rate(self, recovery_actions: List[Dict[str, Any]]) -> float:
        """Calculate success rate of recovery actions"""
        if not recovery_actions:
            return 0.0

        successful = sum(
            1 for action in recovery_actions if action.get("status") == "success"
        )
        return (successful / len(recovery_actions)) * 100.0

    def _calculate_total_time(self, recovery_actions: List[Dict[str, Any]]) -> float:
        """Calculate total time taken for recovery actions"""
        total_time = 0.0
        for action in recovery_actions:
            total_time += action.get("duration_seconds", 0.0)
        return total_time

    def _generate_recovery_next_steps(
        self, recovery_actions: List[Dict[str, Any]], status: str
    ) -> List[str]:
        """Generate next steps based on recovery status"""
        if status == "completed":
            return [
                "Verify all recovered systems are functioning correctly",
                "Update system documentation with recovery procedures",
                "Schedule post-recovery review and lessons learned session",
            ]
        elif status == "partial":
            return [
                "Continue with remaining recovery actions",
                "Assess impact of partially recovered systems",
                "Prioritize remaining recovery tasks",
            ]
        else:
            return [
                "Investigate recovery failures",
                "Implement alternative recovery strategies",
                "Escalate to emergency response team if needed",
            ]

    def _assess_integrity_risk(self, integrity_results: Dict[str, Any]) -> str:
        """Assess overall integrity risk level"""
        critical_issues = integrity_results.get("critical_issues", 0)
        files_with_issues = integrity_results.get("files_with_issues", 0)
        total_files = integrity_results.get("files_validated", 0)

        if critical_issues > 0:
            return "CRITICAL"
        elif (
            files_with_issues > total_files * 0.1
        ):  # More than 10% of files have issues
            return "HIGH"
        elif files_with_issues > 0:
            return "MEDIUM"
        else:
            return "LOW"

    def _generate_emergency_actions(self, severity: str, alert_type: str) -> List[str]:
        """Generate immediate actions for emergency alerts"""
        if severity == "CRITICAL":
            return [
                "Immediate: Activate emergency response protocol",
                "Priority: Isolate affected systems",
                "Escalation: Notify emergency response team",
                "Documentation: Record all actions taken",
            ]
        elif severity == "HIGH":
            return [
                "Immediate: Assess impact and scope",
                "Priority: Implement containment measures",
                "Monitoring: Continuous status monitoring",
                "Communication: Update stakeholders",
            ]
        else:
            return [
                "Monitor: Watch for escalation indicators",
                "Document: Record incident details",
                "Review: Assess prevention measures",
            ]

    def _save_report(self, report: Dict[str, Any], report_type: str, output_dir: Path):
        """Save report to file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = self.report_templates[report_type].format(timestamp=timestamp)
            filepath = output_dir / filename

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)

            self.logger.info(f"Saved {report_type} report to {filepath}")
        except Exception as e:
            self.logger.error(f"Failed to save {report_type} report: {e}")
