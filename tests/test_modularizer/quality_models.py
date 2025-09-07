"""
🧪 QUALITY ASSURANCE MODELS - MODULARIZED COMPONENT
Testing Framework Enhancement Manager - Agent-3

This module contains data models and classes for the quality assurance system.
Extracted from quality_assurance_protocols.py for better modularity.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class QualityLevel:
    """Quality level classification for modularized components."""
    level: str
    score: float
    description: str
    color: str


@dataclass
class QualityMetric:
    """Quality metric for modularization assessment."""
    name: str
    value: float
    weight: float
    threshold: float
    status: str


class QualityThresholds:
    """Quality thresholds configuration for the system."""
    
    def __init__(self):
        self.thresholds = {
            "file_size_reduction": 30.0,  # Minimum 30% reduction
            "module_count": 5.0,          # Minimum 5 modules
            "interface_quality": 0.7,     # Minimum 0.7 interface quality
            "dependency_complexity": 0.6, # Maximum 0.6 complexity
            "naming_conventions": 0.8,    # Minimum 0.8 naming score
            "documentation": 0.7,         # Minimum 0.7 documentation score
            "code_organization": 0.75,    # Minimum 0.75 organization score
            "test_coverage": 80.0         # Minimum 80% test coverage
        }
    
    def get_threshold(self, metric_name: str) -> float:
        """Get threshold value for a specific metric."""
        return self.thresholds.get(metric_name, 0.0)
    
    def set_threshold(self, metric_name: str, value: float) -> None:
        """Set threshold value for a specific metric."""
        self.thresholds[metric_name] = value


class QualityLevels:
    """Quality level classifications for the system."""
    
    def __init__(self):
        self.levels = {
            "excellent": QualityLevel("EXCELLENT", 90.0, "Outstanding modularization quality", "🟢"),
            "good": QualityLevel("GOOD", 75.0, "Good modularization quality", "🟡"),
            "fair": QualityLevel("FAIR", 60.0, "Acceptable modularization quality", "🟠"),
            "poor": QualityLevel("POOR", 45.0, "Below acceptable quality", "🔴"),
            "critical": QualityLevel("CRITICAL", 30.0, "Critical quality issues", "⚫")
        }
    
    def get_level(self, level_name: str) -> QualityLevel:
        """Get quality level by name."""
        return self.levels.get(level_name, self.levels["unknown"])
    
    def determine_level(self, score: float) -> QualityLevel:
        """Determine quality level based on score."""
        if score >= 90.0:
            return self.levels["excellent"]
        elif score >= 75.0:
            return self.levels["good"]
        elif score >= 60.0:
            return self.levels["fair"]
        elif score >= 45.0:
            return self.levels["poor"]
        else:
            return self.levels["critical"]
