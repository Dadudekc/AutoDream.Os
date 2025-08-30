#!/usr/bin/env python3
"""
Database Auditor - Core Component
Extracted from EMERGENCY_RESTORE_004_DATABASE_AUDIT.py

Responsible for:
- Database structure analysis and auditing
- File existence and accessibility checks
- Metadata consistency validation
- Critical issue identification
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

from ..models.audit_results import AuditResults, FileAnalysis
from ..models.integrity_issues import IntegrityIssues
from ..services.logging_service import LoggingService
from ..services.validation_service import ValidationService


class DatabaseAuditor:
    """Database structure analysis and auditing system"""

    def __init__(self):
        self.logger = LoggingService().get_logger("DatabaseAuditor")
        self.validation_service = ValidationService()

        # Critical database files to audit
        self.critical_files = [
            ("task_list.json", Path("agent_workspaces/meeting/task_list.json")),
            ("meeting.json", Path("agent_workspaces/meeting/meeting.json")),
        ]

    def audit_database_structure(self) -> Dict[str, Any]:
        """Audit the overall structure of the contract database"""
        self.logger.info("Auditing database structure...")

        audit_results = AuditResults(
            timestamp=datetime.now().isoformat(),
            file_analysis={},
            structure_validation={},
            metadata_consistency={},
            critical_issues=[],
        )

        # Analyze each critical file
        for filename, filepath in self.critical_files:
            file_info = self._analyze_file(filepath)
            audit_results.file_analysis[filename] = file_info

            # Check for critical issues
            if not file_info.exists:
                audit_results.critical_issues.append(f"CRITICAL: {filename} not found!")
            elif not file_info.readable:
                audit_results.critical_issues.append(
                    f"CRITICAL: {filename} not readable!"
                )
            elif not file_info.valid_json:
                audit_results.critical_issues.append(
                    f"CRITICAL: {filename} contains invalid JSON!"
                )

        # Validate overall structure
        audit_results.structure_validation = self._validate_structure(
            audit_results.file_analysis
        )

        # Check metadata consistency
        audit_results.metadata_consistency = self._check_metadata_consistency(
            audit_results.file_analysis
        )

        self.logger.info(
            f"Database structure audit completed. Found {len(audit_results.critical_issues)} critical issues."
        )

        return audit_results.to_dict()

    def _analyze_file(self, filepath: Path) -> FileAnalysis:
        """Analyze individual file for existence, accessibility, and validity"""
        file_info = FileAnalysis(
            filename=filepath.name,
            filepath=str(filepath),
            exists=filepath.exists(),
            readable=False,
            valid_json=False,
            size_bytes=0,
            last_modified=None,
            json_error=None,
        )

        if not file_info.exists:
            return file_info

        try:
            # Check readability
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                file_info.readable = True
                file_info.size_bytes = len(content.encode("utf-8"))

                # Validate JSON
                try:
                    json.loads(content)
                    file_info.valid_json = True
                except json.JSONDecodeError as e:
                    file_info.json_error = str(e)
                    file_info.valid_json = False

                # Get last modified time
                file_info.last_modified = datetime.fromtimestamp(
                    filepath.stat().st_mtime
                ).isoformat()

        except Exception as e:
            file_info.readable = False
            file_info.json_error = str(e)

        return file_info

    def _validate_structure(
        self, file_analysis: Dict[str, FileAnalysis]
    ) -> Dict[str, Any]:
        """Validate the overall database structure"""
        structure_validation = {
            "total_files": len(file_analysis),
            "existing_files": sum(1 for f in file_analysis.values() if f.exists),
            "readable_files": sum(1 for f in file_analysis.values() if f.readable),
            "valid_json_files": sum(1 for f in file_analysis.values() if f.valid_json),
            "structure_score": 0.0,
        }

        # Calculate structure score
        if structure_validation["total_files"] > 0:
            structure_validation["structure_score"] = (
                structure_validation["valid_json_files"]
                / structure_validation["total_files"]
            )

        return structure_validation

    def _check_metadata_consistency(
        self, file_analysis: Dict[str, FileAnalysis]
    ) -> Dict[str, Any]:
        """Check metadata consistency across database files"""
        metadata_consistency = {
            "file_count_consistency": True,
            "json_validity_consistency": True,
            "accessibility_consistency": True,
            "consistency_score": 0.0,
        }

        # Check if all files have consistent properties
        existing_files = [f for f in file_analysis.values() if f.exists]
        if existing_files:
            # Check if all existing files are readable
            metadata_consistency["accessibility_consistency"] = all(
                f.readable for f in existing_files
            )

            # Check if all existing files have valid JSON
            metadata_consistency["json_validity_consistency"] = all(
                f.valid_json for f in existing_files
            )

            # Calculate consistency score
            consistency_factors = [
                metadata_consistency["accessibility_consistency"],
                metadata_consistency["json_validity_consistency"],
            ]
            metadata_consistency["consistency_score"] = sum(consistency_factors) / len(
                consistency_factors
            )

        return metadata_consistency

    def get_audit_summary(self) -> Dict[str, Any]:
        """Get a summary of the audit results"""
        return {
            "auditor": "DatabaseAuditor",
            "timestamp": datetime.now().isoformat(),
            "critical_files_checked": len(self.critical_files),
            "audit_status": "COMPLETED",
        }
