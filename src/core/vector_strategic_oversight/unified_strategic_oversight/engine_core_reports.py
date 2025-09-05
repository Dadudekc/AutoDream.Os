"""
Strategic Oversight Engine Core Reports - KISS Simplified
========================================================

Report management functionality for strategic oversight operations.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined report operations.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

import logging
from typing import Dict, List, Optional
from .models import StrategicOversightReport
from .enums import ReportType


class StrategicOversightEngineCoreReports:
    """Report management for strategic oversight engine."""
    
    def __init__(self, reports: Dict[str, StrategicOversightReport], logger: logging.Logger):
        """Initialize report management."""
        self.reports = reports
        self.logger = logger
    
    def add_report(self, report: StrategicOversightReport) -> bool:
        """Add a strategic oversight report - simplified."""
        try:
            self.reports[report.report_id] = report
            self.logger.info(f"Added strategic oversight report: {report.report_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add strategic oversight report: {e}")
            return False
    
    def get_report(self, report_id: str) -> Optional[StrategicOversightReport]:
        """Get a strategic oversight report by ID - simplified."""
        try:
            return self.reports.get(report_id)
        except Exception as e:
            self.logger.error(f"Failed to get strategic oversight report: {e}")
            return None
    
    def get_reports(self, report_type: ReportType = None, limit: int = 10) -> List[StrategicOversightReport]:
        """Get strategic oversight reports - simplified."""
        try:
            reports = list(self.reports.values())
            
            if report_type:
                reports = [r for r in reports if r.report_type == report_type]
            
            # Sort by creation date (newest first)
            reports.sort(key=lambda x: x.created_at, reverse=True)
            
            return reports[:limit]
        except Exception as e:
            self.logger.error(f"Failed to get strategic oversight reports: {e}")
            return []
