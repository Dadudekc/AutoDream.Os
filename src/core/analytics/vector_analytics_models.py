#!/usr/bin/env python3
"""
Vector Analytics Models - V2 Compliance Module
==============================================

Data models and configuration classes for vector analytics enhancement system.
Extracted from monolithic vector_analytics_enhancement_system.py for V2 compliance.

Responsibilities:
- Analytics configuration management
- Data models and enums for analytics processing
- Analytics insight data structures
- Configuration validation and defaults

V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class AnalyticsMode(Enum):
    """Analytics processing modes."""
    REALTIME = "realtime"
    BATCH = "batch"
    HYBRID = "hybrid"
    ADAPTIVE = "adaptive"


class IntelligenceLevel(Enum):
    """Intelligence processing levels."""
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass
class AnalyticsInsight:
    """Analytics insight data structure."""
    insight_id: str
    insight_type: str
    confidence: float
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    priority: str = "normal"
    tags: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate insight data after initialization."""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")
        if self.priority not in ["low", "normal", "high", "critical"]:
            raise ValueError("Priority must be one of: low, normal, high, critical")


@dataclass
class VectorAnalyticsConfig:
    """Configuration for vector analytics enhancement system."""
    
    # Core settings
    intelligence_level: IntelligenceLevel = IntelligenceLevel.ADVANCED
    analytics_mode: AnalyticsMode = AnalyticsMode.HYBRID
    max_workers: int = 4
    cache_size: int = 1000
    
    # Feature flags
    enable_realtime_analytics: bool = True
    enable_predictive_analytics: bool = True
    enable_pattern_recognition: bool = True
    enable_intelligent_caching: bool = True
    enable_parallel_processing: bool = True
    enable_autonomous_optimization: bool = True
    
    # Performance settings
    batch_size: int = 100
    update_interval: float = 1.0
    timeout_seconds: float = 30.0
    retry_attempts: int = 3
    
    # Analytics thresholds
    confidence_threshold: float = 0.7
    pattern_threshold: float = 0.8
    anomaly_threshold: float = 0.9
    optimization_threshold: float = 0.85
    
    # Data retention
    max_insights: int = 10000
    max_patterns: int = 5000
    retention_days: int = 30
    
    def validate(self) -> bool:
        """Validate configuration settings."""
        if self.max_workers < 1:
            raise ValueError("max_workers must be at least 1")
        if self.cache_size < 100:
            raise ValueError("cache_size must be at least 100")
        if not 0.0 <= self.confidence_threshold <= 1.0:
            raise ValueError("confidence_threshold must be between 0.0 and 1.0")
        if not 0.0 <= self.pattern_threshold <= 1.0:
            raise ValueError("pattern_threshold must be between 0.0 and 1.0")
        if not 0.0 <= self.anomaly_threshold <= 1.0:
            raise ValueError("anomaly_threshold must be between 0.0 and 1.0")
        if self.batch_size < 1:
            raise ValueError("batch_size must be at least 1")
        if self.update_interval < 0.1:
            raise ValueError("update_interval must be at least 0.1 seconds")
        if self.timeout_seconds < 1.0:
            raise ValueError("timeout_seconds must be at least 1.0")
        if self.retry_attempts < 0:
            raise ValueError("retry_attempts must be non-negative")
        if self.max_insights < 100:
            raise ValueError("max_insights must be at least 100")
        if self.max_patterns < 50:
            raise ValueError("max_patterns must be at least 50")
        if self.retention_days < 1:
            raise ValueError("retention_days must be at least 1")
        return True


@dataclass
class AnalyticsMetrics:
    """Analytics performance metrics."""
    processed_insights: int = 0
    generated_patterns: int = 0
    predictions_made: int = 0
    anomalies_detected: int = 0
    optimization_cycles: int = 0
    average_processing_time: float = 0.0
    success_rate: float = 0.0
    error_count: int = 0
    last_update: datetime = field(default_factory=datetime.now)
    
    def update_success_rate(self):
        """Update success rate based on processed vs error counts."""
        total_operations = self.processed_insights + self.error_count
        if total_operations > 0:
            self.success_rate = self.processed_insights / total_operations
        else:
            self.success_rate = 0.0


@dataclass
class PatternMatch:
    """Pattern matching result."""
    pattern_id: str
    pattern_type: str
    confidence: float
    data: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate pattern match after initialization."""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")


@dataclass
class PredictionResult:
    """Prediction result data structure."""
    prediction_id: str
    prediction_type: str
    predicted_value: Any
    confidence: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate prediction result after initialization."""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")
    
    def is_expired(self) -> bool:
        """Check if prediction has expired."""
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at


# Analytics processing constants
ANALYTICS_TYPES = [
    "business_intelligence",
    "pattern_analysis", 
    "predictive_modeling",
    "anomaly_detection",
    "performance_optimization",
    "trend_analysis",
    "correlation_analysis",
    "clustering_analysis"
]

INSIGHT_PRIORITIES = ["low", "normal", "high", "critical"]

PATTERN_TYPES = [
    "behavioral",
    "temporal", 
    "spatial",
    "frequency",
    "correlation",
    "anomaly"
]

# Default configurations
DEFAULT_CONFIG = VectorAnalyticsConfig()

# Validation functions
def validate_analytics_config(config: VectorAnalyticsConfig) -> bool:
    """Validate analytics configuration."""
    return config.validate()

def validate_insight(insight: AnalyticsInsight) -> bool:
    """Validate analytics insight."""
    if not insight.insight_id or not insight.insight_type:
        return False
    if insight.confidence < 0.0 or insight.confidence > 1.0:
        return False
    if insight.priority not in INSIGHT_PRIORITIES:
        return False
    return True

def validate_pattern_match(pattern: PatternMatch) -> bool:
    """Validate pattern match."""
    if not pattern.pattern_id or not pattern.pattern_type:
        return False
    if pattern.confidence < 0.0 or pattern.confidence > 1.0:
        return False
    return True

def validate_prediction_result(prediction: PredictionResult) -> bool:
    """Validate prediction result."""
    if not prediction.prediction_id or not prediction.prediction_type:
        return False
    if prediction.confidence < 0.0 or prediction.confidence > 1.0:
        return False
    return True


# Factory functions
def create_default_config() -> VectorAnalyticsConfig:
    """Create default analytics configuration."""
    return VectorAnalyticsConfig()

def create_insight(insight_id: str, insight_type: str, confidence: float, 
                  data: Dict[str, Any], priority: str = "normal") -> AnalyticsInsight:
    """Create analytics insight with validation."""
    insight = AnalyticsInsight(
        insight_id=insight_id,
        insight_type=insight_type,
        confidence=confidence,
        data=data,
        priority=priority
    )
    if not validate_insight(insight):
        raise ValueError("Invalid insight data")
    return insight

def create_pattern_match(pattern_id: str, pattern_type: str, confidence: float,
                        data: Dict[str, Any]) -> PatternMatch:
    """Create pattern match with validation."""
    pattern = PatternMatch(
        pattern_id=pattern_id,
        pattern_type=pattern_type,
        confidence=confidence,
        data=data
    )
    if not validate_pattern_match(pattern):
        raise ValueError("Invalid pattern match data")
    return pattern

def create_prediction_result(prediction_id: str, prediction_type: str, 
                           predicted_value: Any, confidence: float) -> PredictionResult:
    """Create prediction result with validation."""
    prediction = PredictionResult(
        prediction_id=prediction_id,
        prediction_type=prediction_type,
        predicted_value=predicted_value,
        confidence=confidence
    )
    if not validate_prediction_result(prediction):
        raise ValueError("Invalid prediction result data")
    return prediction
