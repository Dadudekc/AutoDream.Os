#!/usr/bin/env python3
"""
V2 Compliance Validator - Advanced
=================================

This module contains advanced V2 compliance validation functionality including
web interface integration, advanced reporting, and global instance management.

Author: Agent-2 (Architecture & Design Specialist)
Mission: Modularize v2_compliance_validator.py for V2 compliance
License: MIT
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List, Callable

# Import core components
from .v2_compliance_validator_core import (
    V2ComplianceValidatorCore,
    ComplianceViolation,
    QualityMetrics
)

logger = logging.getLogger(__name__)


class V2ComplianceValidatorAdvanced(V2ComplianceValidatorCore):
    """
    Advanced V2 compliance validator with web interface integration.
    
    V2 Compliance: Advanced validation framework with web interface support.
    """
    
    def __init__(self):
        super().__init__()
        self.web_interface_callbacks: List[Callable] = []
    
    async def validate_directory(self, directory_path: str) -> Dict[str, Any]:
        """Validate V2 compliance for entire directory with web interface notifications."""
        try:
            logger.info(f"🔍 Starting V2 compliance validation for {directory_path}")
            
            violations = []
            quality_metrics = {}
            
            # Scan directory for files
            import os
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    if self._is_analyzable_file(file):
                        file_path = os.path.join(root, file)
                        try:
                            # Analyze file
                            violation = await self._analyze_file(file_path)
                            if violation:
                                violations.append(violation)
                            
                            # Calculate quality metrics
                            metrics = await self._calculate_quality_metrics(file_path)
                            if metrics:
                                quality_metrics[file_path] = metrics
                                
                        except Exception as e:
                            logger.error(f"❌ Failed to analyze {file_path}: {e}")
            
            # Update internal state
            self.violations.extend(violations)
            self.quality_metrics.update(quality_metrics)
            
            # Generate validation report
            report = self._generate_validation_report(violations, quality_metrics)
            
            # Notify web interface
            self._notify_web_interface("validation_completed", report)
            
            logger.info(f"✅ V2 compliance validation completed: {len(violations)} violations found")
            return report
            
        except Exception as e:
            logger.error(f"❌ Directory validation failed: {e}")
            return {"error": str(e)}
    
    def _notify_web_interface(self, event_type: str, data: Dict[str, Any]):
        """Notify web interface of validation events."""
        try:
            for callback in self.web_interface_callbacks:
                try:
                    callback(event_type, data)
                except Exception as e:
                    logger.error(f"❌ Web interface callback error: {e}")
        except Exception as e:
            logger.error(f"❌ Web interface notification failed: {e}")
    
    def add_web_interface_callback(self, callback: Callable):
        """Add web interface callback for real-time updates."""
        self.web_interface_callbacks.append(callback)
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get current validation summary for web interface."""
        return {
            "total_violations": len(self.violations),
            "violations_by_severity": {
                severity: len([v for v in self.violations if v.severity == severity])
                for severity in ["medium", "high", "critical"]
            },
            "quality_metrics_count": len(self.quality_metrics),
            "last_validation": datetime.now().isoformat()
        }
    
    def get_detailed_violations_report(self) -> Dict[str, Any]:
        """Get detailed violations report for web interface."""
        violations_by_severity = {}
        for violation in self.violations:
            severity = violation.severity
            if severity not in violations_by_severity:
                violations_by_severity[severity] = []
            violations_by_severity[severity].append({
                "file_path": violation.file_path,
                "line_count": violation.line_count,
                "violation_type": violation.violation_type,
                "recommendations": violation.recommendations,
                "detected_at": violation.detected_at.isoformat()
            })
        
        return {
            "violations_by_severity": violations_by_severity,
            "total_violations": len(self.violations),
            "summary": {
                "critical": len([v for v in self.violations if v.severity == "critical"]),
                "high": len([v for v in self.violations if v.severity == "high"]),
                "medium": len([v for v in self.violations if v.severity == "medium"])
            }
        }
    
    def get_quality_metrics_summary(self) -> Dict[str, Any]:
        """Get quality metrics summary for web interface."""
        if not self.quality_metrics:
            return {"message": "No quality metrics available"}
        
        # Calculate summary statistics
        total_files = len(self.quality_metrics)
        avg_scores = {
            "compliance": sum(m.compliance_score for m in self.quality_metrics.values()) / total_files,
            "structure": sum(m.structure_score for m in self.quality_metrics.values()) / total_files,
            "documentation": sum(m.documentation_score for m in self.quality_metrics.values()) / total_files,
            "performance": sum(m.performance_score for m in self.quality_metrics.values()) / total_files,
            "security": sum(m.security_score for m in self.quality_metrics.values()) / total_files,
            "overall": sum(m.overall_score for m in self.quality_metrics.values()) / total_files
        }
        
        # Get files with lowest scores
        lowest_overall = min(self.quality_metrics.values(), key=lambda m: m.overall_score)
        lowest_compliance = min(self.quality_metrics.values(), key=lambda m: m.compliance_score)
        
        return {
            "total_files_analyzed": total_files,
            "average_scores": avg_scores,
            "lowest_scores": {
                "overall": {
                    "file_path": lowest_overall.file_path,
                    "score": lowest_overall.overall_score
                },
                "compliance": {
                    "file_path": lowest_compliance.file_path,
                    "score": lowest_compliance.compliance_score
                }
            },
            "files_requiring_attention": [
                {
                    "file_path": path,
                    "overall_score": metrics.overall_score,
                    "violation_count": len(metrics.violations)
                }
                for path, metrics in self.quality_metrics.items()
                if metrics.overall_score < 70 or len(metrics.violations) > 0
            ]
        }
    
    def export_validation_report(self, format_type: str = "json") -> Dict[str, Any]:
        """Export comprehensive validation report."""
        try:
            report = {
                "export_timestamp": datetime.now().isoformat(),
                "validation_summary": self.get_validation_summary(),
                "violations_report": self.get_detailed_violations_report(),
                "quality_metrics": self.get_quality_metrics_summary(),
                "recommendations": self._generate_global_recommendations(
                    self.violations, self.quality_metrics
                )
            }
            
            # Notify web interface of export
            self._notify_web_interface("report_exported", {"format": format_type, "timestamp": report["export_timestamp"]})
            
            return report
            
        except Exception as e:
            logger.error(f"❌ Report export failed: {e}")
            return {"error": str(e)}
    
    def clear_validation_data(self):
        """Clear all validation data and reset state."""
        self.violations.clear()
        self.quality_metrics.clear()
        logger.info("🧹 Validation data cleared")
        
        # Notify web interface
        self._notify_web_interface("data_cleared", {"timestamp": datetime.now().isoformat()})
    
    def get_compliance_trends(self) -> Dict[str, Any]:
        """Get compliance trends over time (placeholder for future implementation)."""
        # This would typically track compliance over time
        # For now, return current state
        return {
            "current_compliance_rate": self._calculate_current_compliance_rate(),
            "trend_analysis": "Trend analysis not yet implemented",
            "recommendations": [
                "Implement historical tracking for trend analysis",
                "Add compliance rate monitoring over time",
                "Create compliance improvement metrics"
            ]
        }
    
    def _calculate_current_compliance_rate(self) -> float:
        """Calculate current compliance rate."""
        if not self.quality_metrics:
            return 0.0
        
        compliant_files = sum(1 for metrics in self.quality_metrics.values() 
                            if metrics.compliance_score == 100.0)
        total_files = len(self.quality_metrics)
        
        return (compliant_files / total_files * 100) if total_files > 0 else 0.0


# Global instance for web interface integration
_v2_compliance_validator: V2ComplianceValidatorAdvanced | None = None


def get_v2_compliance_validator() -> V2ComplianceValidatorAdvanced:
    """Get the global V2 compliance validator instance."""
    global _v2_compliance_validator
    if _v2_compliance_validator is None:
        _v2_compliance_validator = V2ComplianceValidatorAdvanced()
    return _v2_compliance_validator


def reset_global_validator():
    """Reset the global validator instance."""
    global _v2_compliance_validator
    _v2_compliance_validator = None
    logger.info("🔄 Global V2 compliance validator reset")


# Export advanced components
__all__ = [
    'V2ComplianceValidatorAdvanced',
    'get_v2_compliance_validator',
    'reset_global_validator'
]


if __name__ == "__main__":
    """Demonstrate module functionality with practical examples."""
    print("🐝 V2 Compliance Validator - Advanced Module")
    print("=" * 50)
    print("✅ Web interface integration loaded successfully")
    print("✅ Advanced reporting loaded successfully")
    print("✅ Global instance management loaded successfully")
    print("✅ Export functionality loaded successfully")
    print("🐝 WE ARE SWARM - Advanced compliance validation ready!")
    
    # Example usage
    validator = get_v2_compliance_validator()
    print("✅ Global validator instance created successfully")
    print("🚀 Ready for advanced compliance validation!")
