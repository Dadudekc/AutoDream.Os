#!/usr/bin/env python3
"""
Report Export Manager
====================

Handles report generation and export operations.
Separates export concerns from metadata management.

Author: Agent-1 (Performance & Health Systems)
License: MIT
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from .repository_metadata import RepositoryMetadata

logger = logging.getLogger(__name__)


class ReportExportManager:
    """Handles report generation and export operations"""
    
    def __init__(self):
        """Initialize the report export manager"""
        logger.info("Report Export Manager initialized")

    def export_discovery_report(self, repositories: Dict[str, RepositoryMetadata], 
                               scan_history: List[Dict[str, Any]], 
                               output_path: Optional[str] = None) -> str:
        """Export discovery results to JSON report"""
        try:
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"repository_discovery_report_{timestamp}.json"

            # Ensure output directory exists
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)

            report_data = {
                "scan_timestamp": datetime.now().isoformat(),
                "discovery_summary": self._generate_discovery_summary(repositories, scan_history),
                "repositories": [
                    self._repository_to_dict(repo) for repo in repositories.values()
                ],
                "scan_history": scan_history,
            }

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(report_data, f, indent=2, default=str, ensure_ascii=False)

            logger.info(f"Discovery report exported to: {output_path}")
            return str(output_file)

        except Exception as e:
            logger.error(f"Failed to export discovery report: {e}")
            return ""

    def export_repository_report(self, repository: RepositoryMetadata, 
                                scan_history: List[Dict[str, Any]], 
                                output_path: Optional[str] = None) -> str:
        """Export a detailed report for a specific repository"""
        try:
            summary = self._generate_repository_summary(repository, scan_history)
            if not summary:
                return ""

            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"repository_{repository.repository_id}_{timestamp}.json"

            # Ensure output directory exists
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(summary, f, indent=2, default=str, ensure_ascii=False)

            logger.info(f"Repository report exported to: {output_path}")
            return str(output_file)

        except Exception as e:
            logger.error(f"Failed to export repository report: {e}")
            return ""

    def _generate_discovery_summary(self, repositories: Dict[str, RepositoryMetadata], 
                                   scan_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate discovery summary"""
        try:
            if not repositories:
                return {"error": "No repositories available"}

            summary = {
                "total_repositories": len(repositories),
                "total_size_mb": sum(
                    r.size_bytes for r in repositories.values()
                ) / (1024 * 1024),
                "average_health_score": sum(
                    r.health_score for r in repositories.values()
                ) / len(repositories),
                "average_market_readiness": sum(
                    r.market_readiness for r in repositories.values()
                ) / len(repositories),
                "technology_distribution": {},
                "architecture_patterns": {},
                "scan_history": scan_history[-10:] if scan_history else [],
                "scan_statistics": self._calculate_scan_statistics(scan_history),
            }

            # Technology distribution
            for repo in repositories.values():
                lang = repo.technology_stack.get("language", "unknown")
                if lang:
                    summary["technology_distribution"][lang] = (
                        summary["technology_distribution"].get(lang, 0) + 1
                    )

            # Architecture patterns
            for repo in repositories.values():
                for pattern in repo.architecture_patterns:
                    summary["architecture_patterns"][pattern] = (
                        summary["architecture_patterns"].get(pattern, 0) + 1
                    )

            return summary

        except Exception as e:
            logger.error(f"Failed to generate discovery summary: {e}")
            return {"error": str(e)}

    def _generate_repository_summary(self, repository: RepositoryMetadata, 
                                    scan_history: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Generate a detailed summary for a specific repository"""
        try:
            # Get scan history for this repository
            repo_scans = [scan for scan in scan_history if scan["repository_id"] == repository.repository_id]
            
            summary = {
                "repository_id": repository.repository_id,
                "name": repository.name,
                "path": repository.path,
                "size_mb": repository.size_bytes / (1024 * 1024),
                "file_count": repository.file_count,
                "language_count": repository.language_count,
                "last_modified": repository.last_modified.isoformat() if repository.last_modified else None,
                "technology_stack": repository.technology_stack,
                "scores": {
                    "health_score": repository.health_score,
                    "market_readiness": repository.market_readiness,
                },
                "architecture_patterns": repository.architecture_patterns,
                "dependencies_count": len(repository.dependencies),
                "recommendations_count": len(repository.recommendations),
                "scan_history": repo_scans,
                "performance_summary": repository.get_performance_summary(),
                "security_summary": repository.get_security_summary(),
            }

            return summary

        except Exception as e:
            logger.error(f"Failed to generate repository summary: {e}")
            return None

    def _repository_to_dict(self, repository: RepositoryMetadata) -> Dict[str, Any]:
        """Convert repository to dictionary for export"""
        return {
            "repository_id": repository.repository_id,
            "name": repository.name,
            "path": repository.path,
            "size_bytes": repository.size_bytes,
            "file_count": repository.file_count,
            "technology_stack": repository.technology_stack,
            "health_score": repository.health_score,
            "market_readiness": repository.market_readiness,
            "architecture_patterns": repository.architecture_patterns,
            "dependencies": repository.dependencies,
            "recommendations": repository.recommendations,
            "performance_metrics": repository.performance_metrics,
            "security_analysis": repository.security_analysis,
        }

    def _calculate_scan_statistics(self, scan_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate scan operation statistics"""
        try:
            if not scan_history:
                return {}

            total_scans = len(scan_history)
            scan_types = {}
            total_duration = 0.0

            for scan in scan_history:
                scan_type = scan.get("scan_type", "unknown")
                scan_types[scan_type] = scan_types.get(scan_type, 0) + 1
                total_duration += scan.get("duration", 0.0)

            return {
                "total_scans": total_scans,
                "scan_types": scan_types,
                "average_duration": total_duration / total_scans if total_scans > 0 else 0.0,
                "total_duration": total_duration,
            }

        except Exception as e:
            logger.error(f"Failed to calculate scan statistics: {e}")
            return {}

