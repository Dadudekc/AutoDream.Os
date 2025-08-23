#!/usr/bin/env python3
"""
Repository Report Generator
===========================

Responsible for generating reports and exports.
Delegates specific responsibilities to focused components.

Author: Agent-1 (Performance & Health Systems)
License: MIT
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from .repository_metadata import RepositoryMetadata, RepositoryMetadataManager
from .report_export import ReportExportManager

logger = logging.getLogger(__name__)


class RepositoryReportGenerator:
    """
    Repository report generator for comprehensive reporting
    
    Features:
    - Discovery summary reports
    - Repository metadata export
    - JSON report generation
    - Scan history tracking
    - Statistical analysis
    """

    def __init__(self):
        """Initialize the repository report generator"""
        self.metadata_manager = RepositoryMetadataManager()
        self.export_manager = ReportExportManager()
        self.scan_history: List[Dict[str, Any]] = []
        logger.info("Repository Report Generator initialized")

    def add_repository(self, metadata: RepositoryMetadata):
        """Add a repository to the report generator"""
        self.metadata_manager.add_repository(metadata)

    def record_scan(self, repository_id: str, scan_type: str = "basic", duration: float = 0.0):
        """Record a scan operation"""
        scan_record = {
            "timestamp": datetime.now().isoformat(),
            "repository_id": repository_id,
            "scan_type": scan_type,
            "duration": duration,
        }
        self.scan_history.append(scan_record)
        logger.debug(f"Recorded scan: {repository_id} ({scan_type})")

    def get_discovery_summary(self) -> Dict[str, Any]:
        """Get a summary of all discovered repositories"""
        repositories = self.metadata_manager.get_all_repositories()
        return self.export_manager._generate_discovery_summary(repositories, self.scan_history)

    def export_discovery_report(self, output_path: Optional[str] = None) -> str:
        """Export discovery results to JSON report"""
        repositories = self.metadata_manager.get_all_repositories()
        return self.export_manager.export_discovery_report(repositories, self.scan_history, output_path)

    def generate_repository_summary(self, repository_id: str) -> Optional[Dict[str, Any]]:
        """Generate a detailed summary for a specific repository"""
        repository = self.metadata_manager.get_repository(repository_id)
        if not repository:
            logger.warning(f"Repository not found: {repository_id}")
            return None
        
        return self.export_manager._generate_repository_summary(repository, self.scan_history)

    def export_repository_report(self, repository_id: str, output_path: Optional[str] = None) -> str:
        """Export a detailed report for a specific repository"""
        repository = self.metadata_manager.get_repository(repository_id)
        if not repository:
            logger.warning(f"Repository not found: {repository_id}")
            return ""
        
        return self.export_manager.export_repository_report(repository, self.scan_history, output_path)

    def get_report_statistics(self) -> Dict[str, Any]:
        """Get statistics about generated reports"""
        return {
            "total_repositories": self.metadata_manager.get_repository_count(),
            "total_scans": len(self.scan_history),
            "report_capabilities": {
                "discovery_summary": True,
                "repository_summary": True,
                "json_export": True,
                "scan_history": True,
            },
            "last_scan": self.scan_history[-1] if self.scan_history else None,
        }

    def clear_history(self):
        """Clear scan history"""
        self.scan_history.clear()
        logger.info("Scan history cleared")

    def clear_repositories(self):
        """Clear all repositories"""
        self.metadata_manager.clear_repositories()

    def get_repositories_by_language(self, language: str) -> List[RepositoryMetadata]:
        """Get repositories by programming language"""
        return self.metadata_manager.get_repositories_by_language(language)

    def get_repositories_by_score_range(self, min_score: float, max_score: float) -> List[RepositoryMetadata]:
        """Get repositories within a health score range"""
        return self.metadata_manager.get_repositories_by_score_range(min_score, max_score)


def main():
    """Main function for standalone testing"""
    import argparse

    parser = argparse.ArgumentParser(description="Repository Report Generator")
    parser.add_argument("--summary", action="store_true", help="Show discovery summary")
    parser.add_argument("--export", action="store_true", help="Export discovery report")
    parser.add_argument("--stats", action="store_true", help="Show report statistics")
    parser.add_argument("--clear", action="store_true", help="Clear all data")

    args = parser.parse_args()

    generator = RepositoryReportGenerator()

    try:
        if args.summary:
            summary = generator.get_discovery_summary()
            if "error" in summary:
                print(f"❌ Error: {summary['error']}")
            else:
                print(f"📊 Discovery Summary:")
                print(f"  Total Repositories: {summary['total_repositories']}")
                print(f"  Average Health Score: {summary['average_health_score']:.1f}/100")
                print(f"  Average Market Readiness: {summary['average_market_readiness']:.1f}/100")
                print(f"  Total Size: {summary['total_size_mb']:.1f} MB")
                print(f"  Total Scans: {summary['scan_statistics'].get('total_scans', 0)}")

        elif args.export:
            if generator.metadata_manager.get_repository_count() > 0:
                output_file = generator.export_discovery_report()
                if output_file:
                    print(f"📄 Discovery report exported to: {output_file}")
                else:
                    print("❌ Failed to export report")
            else:
                print("❌ No repositories to export. Add repositories first.")

        elif args.stats:
            stats = generator.get_report_statistics()
            print(f"📊 Report Generator Statistics:")
            print(f"  Total Repositories: {stats['total_repositories']}")
            print(f"  Total Scans: {stats['total_scans']}")
            print(f"  Report Capabilities: {stats['report_capabilities']}")

        elif args.clear:
            generator.clear_history()
            generator.clear_repositories()
            print("🗑️ All data cleared")

        else:
            print("📊 Repository Report Generator ready")
            print("Use --summary to show discovery summary")
            print("Use --export to export discovery report")
            print("Use --stats to show report statistics")
            print("Use --clear to clear all data")

    except Exception as e:
        print(f"❌ Operation failed: {e}")
        exit(1)


if __name__ == "__main__":
    main()
