#!/usr/bin/env python3
"""Compliance reporting including cryptography verification."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List
import json
import logging
import sqlite3
import time
import ssl

from .encryption import EncryptionManager


@dataclass
class ComplianceReport:
    """Structure representing a compliance report."""

    report_id: str
    timestamp: float
    standards: List[str]
    compliance_score: float
    findings: List[Dict]
    recommendations: List[str]
    next_review_date: float
    auditor: str
    crypto_coverage: float


class ComplianceReporter:
    """Generate compliance reports for given standards.

    The reporter performs a lightweight assessment for ISO27001 and stores
    results in a SQLite database.  A specific cryptography check ensures that
    both encryption at rest and in transit are functional.
    """

    def __init__(self, db_file: str = "compliance.db") -> None:
        self.logger = logging.getLogger(__name__)
        self.db_file = db_file
        self.compliance_standards = {
            "ISO27001": [
                "Information security policy",
                "Access control",
                "Cryptography",
            ]
        }
        self._init_compliance_database()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def generate_compliance_report(
        self, standards: List[str], auditor: str = "system"
    ) -> Dict:
        """Generate a compliance report for the selected standards."""

        timestamp = time.time()
        report_id = f"compliance_report_{int(timestamp)}"
        findings: List[Dict] = []
        total_score = 0.0

        for standard in standards:
            if standard == "ISO27001":
                standard_findings = self._assess_iso27001_compliance()
            else:
                standard_findings = [
                    {
                        "standard": standard,
                        "finding": "Unknown standard",
                        "severity": "medium",
                        "status": "unknown",
                        "description": f"Compliance assessment not available for {standard}",
                    }
                ]
            findings.extend(standard_findings)
            total_score += self._calculate_standard_score(standard_findings)

        standard_count = len(standards)
        compliance_score = total_score / standard_count if standard_count else 0.0
        crypto_coverage = 100.0 if self._verify_cryptography() else 0.0
        recommendations = self._generate_recommendations(findings, crypto_coverage)
        report = ComplianceReport(
            report_id=report_id,
            timestamp=timestamp,
            standards=standards,
            compliance_score=compliance_score,
            findings=findings,
            recommendations=recommendations,
            next_review_date=timestamp + (30 * 24 * 3600),
            auditor=auditor,
            crypto_coverage=crypto_coverage,
        )
        self._store_compliance_report(report)
        return asdict(report)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _assess_iso27001_compliance(self) -> List[Dict]:
        """Return a minimal set of ISO27001 findings."""

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
        ]

        if self._verify_cryptography():
            findings.append(
                {
                    "standard": "ISO27001",
                    "finding": "Cryptography",
                    "severity": "high",
                    "status": "implemented",
                    "description": "Encryption at rest and in transit verified",
                }
            )
        else:
            findings.append(
                {
                    "standard": "ISO27001",
                    "finding": "Cryptography",
                    "severity": "high",
                    "status": "not_implemented",
                    "description": "Missing cryptography coverage",
                }
            )
        return findings

    def _verify_cryptography(self) -> bool:
        """Ensure encryption utilities operate correctly."""

        try:
            manager = EncryptionManager()
            data = b"test"
            token = manager.encrypt(data)
            if manager.decrypt(token) != data:
                return False
            context = EncryptionManager.create_secure_context()
            return context.minimum_version >= ssl.TLSVersion.TLSv1_2
        except Exception as exc:  # pragma: no cover - defensive
            self.logger.error("Cryptography verification failed: %s", exc)
            return False

    def _calculate_standard_score(self, findings: List[Dict]) -> float:
        total = len(findings)
        if not total:
            return 0.0
        implemented = sum(1 for f in findings if f["status"] == "implemented")
        return (implemented / total) * 100.0

    def _generate_recommendations(
        self, findings: List[Dict], crypto_coverage: float
    ) -> List[str]:
        recs: List[str] = []
        if crypto_coverage < 100.0:
            recs.append("Improve cryptography implementation")
        if any(f["status"] != "implemented" for f in findings):
            recs.append("Address outstanding compliance findings")
        return recs

    def _init_compliance_database(self) -> None:
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
                auditor TEXT NOT NULL,
                crypto_coverage REAL DEFAULT 0
            )
            """
        )
        conn.commit()
        conn.close()

    def _store_compliance_report(self, report: ComplianceReport) -> None:
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO compliance_reports
            (report_id, timestamp, standards, compliance_score, findings,
             recommendations, next_review_date, auditor, crypto_coverage)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                report.crypto_coverage,
            ),
        )
        conn.commit()
        conn.close()


__all__ = ["ComplianceReport", "ComplianceReporter"]
