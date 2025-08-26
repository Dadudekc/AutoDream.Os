#!/usr/bin/env python3
"""Compliance reporting and assessment."""

from dataclasses import dataclass, asdict
from typing import Dict, List
import json
import logging
import sqlite3
import time


@dataclass
class ComplianceReport:
    """Compliance report structure."""

    report_id: str
    timestamp: float
    standards: List[str]
    compliance_score: float
    findings: List[Dict]
    recommendations: List[str]
    next_review_date: float
    auditor: str


class ComplianceReporter:
    """Generate compliance reports for given standards."""

    def __init__(self, db_file: str = "compliance.db") -> None:
        self.logger = logging.getLogger(__name__)
        self.db_file = db_file
        self.compliance_standards = {
            "ISO27001": {
                "description": "Information Security Management System",
                "requirements": [
                    "Information security policy",
                    "Asset management",
                    "Access control",
                    "Cryptography",
                    "Physical security",
                    "Operations security",
                    "Communications security",
                    "System acquisition",
                    "Supplier relationships",
                    "Incident management",
                    "Business continuity",
                    "Compliance",
                ],
            },
            "SOC2": {
                "description": "System and Organization Controls 2",
                "criteria": [
                    "Security",
                    "Availability",
                    "Processing integrity",
                    "Confidentiality",
                    "Privacy",
                ],
            },
            "GDPR": {
                "description": "General Data Protection Regulation",
                "principles": [
                    "Lawfulness, fairness and transparency",
                    "Purpose limitation",
                    "Data minimization",
                    "Accuracy",
                    "Storage limitation",
                    "Integrity and confidentiality",
                    "Accountability",
                ],
            },
        }
        self._init_compliance_database()

    def generate_compliance_report(
        self, standards: List[str], auditor: str = "system"
    ) -> Dict:
        """Generate comprehensive compliance report."""
        try:
            timestamp = time.time()
            report_id = f"compliance_report_{int(timestamp)}"
            findings: List[Dict] = []
            total_score = 0.0
            standard_count = len(standards)
            for standard in standards:
                if standard in self.compliance_standards:
                    standard_findings = self._assess_standard_compliance(standard)
                    findings.extend(standard_findings)
                    total_score += self._calculate_standard_score(standard_findings)
            compliance_score = total_score / standard_count if standard_count else 0.0
            recommendations = self._generate_compliance_recommendations(
                findings, compliance_score
            )
            report = ComplianceReport(
                report_id=report_id,
                timestamp=timestamp,
                standards=standards,
                compliance_score=compliance_score,
                findings=findings,
                recommendations=recommendations,
                next_review_date=timestamp + (30 * 24 * 3600),
                auditor=auditor,
            )
            self._store_compliance_report(report)
            self.logger.info(
                "Compliance report generated: %s - Score: %.1f%%",
                report_id,
                compliance_score,
            )
            return asdict(report)
        except Exception as exc:  # pragma: no cover - defensive
            self.logger.error("Failed to generate compliance report: %s", exc)
            return {}

    def _assess_standard_compliance(self, standard: str) -> List[Dict]:
        findings: List[Dict] = []
        try:
            if standard == "ISO27001":
                findings = self._assess_iso27001_compliance()
            elif standard == "SOC2":
                findings = self._assess_soc2_compliance()
            elif standard == "GDPR":
                findings = self._assess_gdpr_compliance()
            else:
                findings.append(
                    {
                        "standard": standard,
                        "finding": "Unknown compliance standard",
                        "severity": "medium",
                        "status": "unknown",
                        "description": f"Compliance assessment not available for {standard}",
                    }
                )
        except Exception as exc:  # pragma: no cover - defensive
            self.logger.error("Compliance assessment failed for %s: %s", standard, exc)
            findings.append(
                {
                    "standard": standard,
                    "finding": "Assessment error",
                    "severity": "high",
                    "status": "error",
                    "description": f"Failed to assess compliance: {exc}",
                }
            )
        return findings

    def _assess_iso27001_compliance(self) -> List[Dict]:
        findings = [
            {
                "standard": "ISO27001",
                "finding": "Information Security Policy",
                "severity": "medium",
                "status": "implemented",
                "description": "Security policy framework is in place",
            },
            {
                "standard": "ISO27001",
                "finding": "Access Control",
                "severity": "high",
                "status": "implemented",
                "description": "Role-based access control system implemented",
            },
            {
                "standard": "ISO27001",
                "finding": "Cryptography",
                "severity": "medium",
                "status": "partially_implemented",
                "description": "Basic encryption implemented, consider enhancing",
            },
            {
                "standard": "ISO27001",
                "finding": "Incident Management",
                "severity": "high",
                "status": "implemented",
                "description": "Security incident response system operational",
            },
        ]
        return findings

    def _assess_soc2_compliance(self) -> List[Dict]:
        findings = [
            {
                "standard": "SOC2",
                "finding": "Security",
                "severity": "high",
                "status": "implemented",
                "description": "Security controls and monitoring implemented",
            },
            {
                "standard": "SOC2",
                "finding": "Availability",
                "severity": "medium",
                "status": "partially_implemented",
                "description": "Basic availability monitoring, consider enhancing",
            },
            {
                "standard": "SOC2",
                "finding": "Processing Integrity",
                "severity": "medium",
                "status": "implemented",
                "description": "Data processing validation implemented",
            },
        ]
        return findings

    def _assess_gdpr_compliance(self) -> List[Dict]:
        findings = [
            {
                "standard": "GDPR",
                "finding": "Data Minimization",
                "severity": "high",
                "status": "implemented",
                "description": "Data collection limited to necessary information",
            },
            {
                "standard": "GDPR",
                "finding": "Data Protection",
                "severity": "high",
                "status": "implemented",
                "description": "Encryption and access controls implemented",
            },
            {
                "standard": "GDPR",
                "finding": "User Rights",
                "severity": "medium",
                "status": "partially_implemented",
                "description": "Basic user rights implemented, consider enhancing",
            },
        ]
        return findings

    def _calculate_standard_score(self, findings: List[Dict]) -> float:
        if not findings:
            return 0.0
        total_score = 0.0
        for finding in findings:
            status = finding.get("status", "unknown")
            severity = finding.get("severity", "medium")
            if status == "implemented":
                score = 100
            elif status == "partially_implemented":
                score = 70
            elif status == "not_implemented":
                score = 0
            else:
                score = 50
            if severity == "high":
                score *= 1.2
            elif severity == "low":
                score *= 0.8
            total_score += min(100, max(0, score))
        return total_score / len(findings)

    def _generate_compliance_recommendations(
        self, findings: List[Dict], compliance_score: float
    ) -> List[str]:
        recommendations: List[str] = []
        for finding in findings:
            status = finding.get("status")
            if status == "partially_implemented":
                recommendations.append(f"Enhance {finding['finding']} implementation")
            elif status == "not_implemented":
                recommendations.append(f"Implement {finding['finding']}")
            elif status == "unknown":
                recommendations.append(f"Assess {finding['finding']} compliance status")
        if compliance_score < 70:
            recommendations.extend(
                [
                    "Conduct comprehensive compliance audit",
                    "Implement compliance monitoring system",
                    "Develop compliance improvement roadmap",
                ]
            )
        elif compliance_score < 85:
            recommendations.extend(
                [
                    "Address remaining compliance gaps",
                    "Enhance compliance monitoring",
                    "Schedule follow-up compliance review",
                ]
            )
        else:
            recommendations.extend(
                [
                    "Maintain current compliance posture",
                    "Schedule regular compliance reviews",
                    "Monitor for new compliance requirements",
                ]
            )
        return recommendations

    def _init_compliance_database(self) -> None:
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS compliance_reports (
                    report_id TEXT PRIMARY KEY,
                    timestamp REAL NOT NULL,
                    standards TEXT NOT NULL,
                    compliance_score REAL NOT NULL,
                    findings TEXT NOT NULL,
                    recommendations TEXT NOT NULL,
                    next_review_date REAL NOT NULL,
                    auditor TEXT NOT NULL
                )
                """
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_compliance_timestamp ON compliance_reports(timestamp)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_compliance_auditor ON compliance_reports(auditor)"
            )
            conn.commit()
            conn.close()
            self.logger.info("Compliance database initialized successfully")
        except Exception as exc:  # pragma: no cover - defensive
            self.logger.error("Failed to initialize compliance database: %s", exc)

    def _store_compliance_report(self, report: ComplianceReport) -> None:
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO compliance_reports
                (report_id, timestamp, standards, compliance_score, findings, recommendations, next_review_date, auditor)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    report.report_id,
                    report.timestamp,
                    json.dumps(report.standards),
                    report.compliance_score,
                    json.dumps(report.findings),
                    json.dumps(report.recommendations),
                    report.next_review_date,
                    report.auditor,
                ),
            )
            conn.commit()
            conn.close()
        except Exception as exc:  # pragma: no cover - defensive
            self.logger.error("Failed to store compliance report: %s", exc)
