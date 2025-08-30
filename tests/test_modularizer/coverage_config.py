"""
🧪 COVERAGE CONFIGURATION - TEST-011 Modularization Implementation
Testing Framework Enhancement Manager - Agent-3

This module contains the configuration management for testing coverage analysis.
Extracted from the monolithic testing_coverage_analysis.py file to achieve V2 compliance.
"""

from typing import Dict, Any
from .coverage_models import CoverageLevel, get_default_coverage_levels


class CoverageConfiguration:
    """
    Configuration management for testing coverage analysis.
    
    This class provides:
    - Coverage level definitions
    - Risk assessment thresholds
    - Coverage targets for different metrics
    - Configuration validation and customization
    """
    
    def __init__(self, custom_config: Dict[str, Any] = None):
        """
        Initialize coverage configuration.
        
        Args:
            custom_config: Optional custom configuration to override defaults
        """
        self.coverage_levels = self._initialize_coverage_levels()
        self.risk_thresholds = self._initialize_risk_thresholds()
        self.coverage_targets = self._initialize_coverage_targets()
        
        # Apply custom configuration if provided
        if custom_config:
            self._apply_custom_config(custom_config)
    
    def _initialize_coverage_levels(self) -> Dict[str, CoverageLevel]:
        """Initialize coverage level classifications."""
        return get_default_coverage_levels()
    
    def _initialize_risk_thresholds(self) -> Dict[str, float]:
        """Initialize risk assessment thresholds."""
        return {
            "high_risk": 60.0,      # Below 60% coverage is high risk
            "medium_risk": 75.0,    # Below 75% coverage is medium risk
            "low_risk": 85.0,       # Below 85% coverage is low risk
            "safe": 95.0            # Above 95% coverage is safe
        }
    
    def _initialize_coverage_targets(self) -> Dict[str, float]:
        """Initialize coverage targets for different metrics."""
        return {
            "line_coverage": 90.0,      # Target 90% line coverage
            "branch_coverage": 85.0,    # Target 85% branch coverage
            "function_coverage": 95.0,  # Target 95% function coverage
            "class_coverage": 90.0,     # Target 90% class coverage
            "overall_coverage": 85.0    # Target 85% overall coverage
        }
    
    def _apply_custom_config(self, custom_config: Dict[str, Any]) -> None:
        """Apply custom configuration overrides."""
        if "coverage_levels" in custom_config:
            self.coverage_levels.update(custom_config["coverage_levels"])
        
        if "risk_thresholds" in custom_config:
            self.risk_thresholds.update(custom_config["risk_thresholds"])
        
        if "coverage_targets" in custom_config:
            self.coverage_targets.update(custom_config["coverage_targets"])
    
    def get_coverage_level(self, percentage: float) -> CoverageLevel:
        """
        Get the coverage level for a given percentage.
        
        Args:
            percentage: The coverage percentage
            
        Returns:
            The appropriate CoverageLevel object
        """
        if not isinstance(percentage, (int, float)) or percentage < 0 or percentage > 100:
            raise ValueError("Percentage must be a number between 0 and 100")
        
        # Find the highest level that the percentage meets or exceeds
        for level_name, level in sorted(
            self.coverage_levels.items(),
            key=lambda x: x[1].percentage,
            reverse=True
        ):
            if percentage >= level.percentage:
                return level
        
        # If no level is found, return the lowest level
        return min(self.coverage_levels.values(), key=lambda x: x.percentage)
    
    def get_risk_level(self, percentage: float) -> str:
        """
        Get the risk level for a given coverage percentage.
        
        Args:
            percentage: The coverage percentage
            
        Returns:
            The risk level string
        """
        if not isinstance(percentage, (int, float)) or percentage < 0 or percentage > 100:
            raise ValueError("Percentage must be a number between 0 and 100")
        
        if percentage >= self.risk_thresholds["safe"]:
            return "safe"
        elif percentage >= self.risk_thresholds["low_risk"]:
            return "low_risk"
        elif percentage >= self.risk_thresholds["medium_risk"]:
            return "medium_risk"
        else:
            return "high_risk"
    
    def get_coverage_target(self, metric_name: str) -> float:
        """
        Get the coverage target for a specific metric.
        
        Args:
            metric_name: The name of the coverage metric
            
        Returns:
            The target coverage percentage
        """
        if metric_name not in self.coverage_targets:
            raise ValueError(f"Unknown coverage metric: {metric_name}")
        
        return self.coverage_targets[metric_name]
    
    def set_coverage_target(self, metric_name: str, target: float) -> None:
        """
        Set a custom coverage target for a specific metric.
        
        Args:
            metric_name: The name of the coverage metric
            target: The new target coverage percentage
        """
        if not isinstance(target, (int, float)) or target < 0 or target > 100:
            raise ValueError("Target must be a number between 0 and 100")
        
        if metric_name not in self.coverage_targets:
            raise ValueError(f"Unknown coverage metric: {metric_name}")
        
        self.coverage_targets[metric_name] = target
    
    def set_risk_threshold(self, threshold_name: str, value: float) -> None:
        """
        Set a custom risk threshold.
        
        Args:
            threshold_name: The name of the risk threshold
            value: The new threshold value
        """
        if threshold_name not in self.risk_thresholds:
            raise ValueError(f"Unknown risk threshold: {threshold_name}")
        
        if not isinstance(value, (int, float)) or value < 0 or value > 100:
            raise ValueError("Threshold value must be a number between 0 and 100")
        
        self.risk_thresholds[threshold_name] = value
    
    def add_custom_coverage_level(self, name: str, level: CoverageLevel) -> None:
        """
        Add a custom coverage level.
        
        Args:
            name: The name for the custom level
            level: The CoverageLevel object
        """
        if not isinstance(name, str) or not name:
            raise ValueError("Level name must be a non-empty string")
        
        if not isinstance(level, CoverageLevel):
            raise ValueError("Level must be a CoverageLevel object")
        
        self.coverage_levels[name] = level
    
    def get_configuration_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the current configuration.
        
        Returns:
            Dictionary containing configuration summary
        """
        return {
            "coverage_levels": {
                name: {
                    "level": level.level,
                    "percentage": level.percentage,
                    "description": level.description,
                    "color": level.color
                }
                for name, level in self.coverage_levels.items()
            },
            "risk_thresholds": self.risk_thresholds.copy(),
            "coverage_targets": self.coverage_targets.copy()
        }
    
    def validate_configuration(self) -> bool:
        """
        Validate the current configuration.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        try:
            # Validate coverage levels
            for name, level in self.coverage_levels.items():
                if not isinstance(level, CoverageLevel):
                    return False
            
            # Validate risk thresholds
            for name, threshold in self.risk_thresholds.items():
                if not isinstance(threshold, (int, float)) or threshold < 0 or threshold > 100:
                    return False
            
            # Validate coverage targets
            for name, target in self.coverage_targets.items():
                if not isinstance(target, (int, float)) or target < 0 or target > 100:
                    return False
            
            return True
            
        except Exception:
            return False
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to default values."""
        self.coverage_levels = self._initialize_coverage_levels()
        self.risk_thresholds = self._initialize_risk_thresholds()
        self.coverage_targets = self._initialize_coverage_targets()


# Factory function for creating default configuration
def create_default_coverage_config() -> CoverageConfiguration:
    """Create a default coverage configuration."""
    return CoverageConfiguration()


# Factory function for creating custom configuration
def create_custom_coverage_config(custom_config: Dict[str, Any]) -> CoverageConfiguration:
    """Create a custom coverage configuration."""
    return CoverageConfiguration(custom_config)
