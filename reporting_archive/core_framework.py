#!/usr/bin/env python3
"""
Core Quality Assurance Framework
================================

Core data structures, enums, and base classes for the V2 quality assurance system.
Follows V2 coding standards: ≤300 lines per module.
"""

import json
import time
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class QualityLevel(Enum):
    """Quality level enumeration"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TestType(Enum):
    """Test type enumeration"""
    UNIT = "unit"
    INTEGRATION = "integration"
    PERFORMANCE = "performance"
    SECURITY = "security"
    COMPATIBILITY = "compatibility"
    ACCESSIBILITY = "accessibility"


@dataclass
class QualityMetric:
    """Quality metric data structure"""
    metric_name: str
    value: Union[float, int, str, bool]
    threshold: Union[float, int, str, bool]
    quality_level: QualityLevel
    timestamp: float
    service_id: str
    description: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return asdict(self)

    def meets_threshold(self) -> bool:
        """Check if metric meets quality threshold"""
        if isinstance(self.value, (int, float)) and isinstance(self.threshold, (int, float)):
            return self.value >= self.threshold
        return self.value == self.threshold

    def get_quality_status(self) -> str:
        """Get human-readable quality status"""
        if self.meets_threshold():
            return "PASS"
        return "FAIL"


@dataclass
class TestResult:
    """Test result data structure"""
    test_id: str
    test_name: str
    test_type: TestType
    service_id: str
    status: str  # "passed", "failed", "error", "skipped"
    execution_time: float
    timestamp: float
    details: Dict[str, Any]
    quality_score: float

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        result = asdict(self)
        result['test_type'] = self.test_type.value
        return result

    def is_successful(self) -> bool:
        """Check if test was successful"""
        return self.status == "passed"

    def get_execution_summary(self) -> str:
        """Get human-readable execution summary"""
        return f"{self.test_name} ({self.test_type.value}): {self.status.upper()} in {self.execution_time:.2f}s"


@dataclass
class QualityReport:
    """Quality report data structure"""
    report_id: str
    timestamp: float
    overall_quality_score: float
    service_count: int
    tests_executed: int
    tests_passed: int
    tests_failed: int
    quality_metrics: List[QualityMetric]
    test_results: List[TestResult]
    recommendations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return asdict(self)

    def get_pass_rate(self) -> float:
        """Calculate test pass rate"""
        if self.tests_executed == 0:
            return 0.0
        return (self.tests_passed / self.tests_executed) * 100

    def get_fail_rate(self) -> float:
        """Calculate test fail rate"""
        if self.tests_executed == 0:
            return 0.0
        return (self.tests_failed / self.tests_executed) * 100

    def get_quality_summary(self) -> str:
        """Get human-readable quality summary"""
        pass_rate = self.get_pass_rate()
        return f"Quality Score: {self.overall_quality_score:.1f}/100, Pass Rate: {pass_rate:.1f}%"

    def export_to_json(self, file_path: str) -> bool:
        """Export report to JSON file"""
        try:
            with open(file_path, 'w') as f:
                json.dump(self.to_dict(), f, indent=2, default=str)
            return True
        except Exception as e:
            logger.error(f"Failed to export report to {file_path}: {e}")
            return False


class QualityConfig:
    """Quality assurance configuration"""
    
    def __init__(self, config_path: str = "qa_config"):
        self.config_path = Path(config_path)
        self.config_path.mkdir(exist_ok=True)
        
        # Default quality thresholds
        self.default_thresholds = {
            "test_coverage": 80.0,
            "code_quality": 7.0,
            "performance_latency": 100.0,
            "security_score": 8.0,
            "documentation_coverage": 90.0
        }
        
        # Quality level mappings
        self.quality_levels = {
            "critical": 9.0,
            "high": 7.0,
            "medium": 5.0,
            "low": 3.0
        }

    def get_threshold(self, metric_name: str) -> float:
        """Get threshold for specific metric"""
        return self.default_thresholds.get(metric_name, 0.0)

    def set_threshold(self, metric_name: str, value: float) -> None:
        """Set threshold for specific metric"""
        self.default_thresholds[metric_name] = value

    def get_quality_level(self, score: float) -> QualityLevel:
        """Get quality level based on score"""
        if score >= self.quality_levels["critical"]:
            return QualityLevel.CRITICAL
        elif score >= self.quality_levels["high"]:
            return QualityLevel.HIGH
        elif score >= self.quality_levels["medium"]:
            return QualityLevel.MEDIUM
        else:
            return QualityLevel.LOW

    def save_config(self) -> bool:
        """Save configuration to file"""
        try:
            config_file = self.config_path / "qa_config.json"
            with open(config_file, 'w') as f:
                json.dump({
                    "thresholds": self.default_thresholds,
                    "quality_levels": self.quality_levels
                }, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Failed to save QA config: {e}")
            return False

    def load_config(self) -> bool:
        """Load configuration from file"""
        try:
            config_file = self.config_path / "qa_config.json"
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    self.default_thresholds = config.get("thresholds", self.default_thresholds)
                    self.quality_levels = config.get("quality_levels", self.quality_levels)
            return True
        except Exception as e:
            logger.error(f"Failed to load QA config: {e}")
            return False
