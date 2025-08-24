#!/usr/bin/env python3
"""
Error Pattern Detector - V2 Error Pattern Detection
==================================================
Specialized module for detecting and analyzing error patterns
from error analytics data. Follows V2 standards with advanced
pattern recognition capabilities.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

# Import our error handling system
from src.core.error_handler import (
    ErrorHandler,
    ErrorInfo,
    ErrorSeverity,
)

# ──────────────────────────── Logging
log = logging.getLogger("error_pattern_detector")


@dataclass
class PatternAnalysisResult:
    """Result of pattern analysis"""
    
    pattern_id: str
    error_signature: str
    occurrences: int
    first_seen: datetime
    last_seen: datetime
    severity_distribution: Dict[ErrorSeverity, int]
    category_distribution: Dict[str, int]
    frequency_score: float
    impact_score: float
    confidence_level: float


class ErrorPatternDetector:
    """Advanced error pattern detection and analysis"""
    
    def __init__(self, error_handler: ErrorHandler):
        self.error_handler = error_handler
        self.detected_patterns: List[ErrorPattern] = []
        self.pattern_analysis_cache: Dict[str, PatternAnalysisResult] = {}
        
    def detect_error_patterns(self) -> List[ErrorPattern]:
        """Detect error patterns and update statistics"""
        try:
            patterns = self.error_handler.get_error_patterns()
            new_patterns = len(patterns) - len(self.detected_patterns)
            
            if new_patterns > 0:
                self.detected_patterns = patterns
                log.info(f"Detected {new_patterns} new error patterns")
                
                # Analyze pattern severity
                for pattern in patterns:
                    if pattern.occurrences >= 10:
                        log.warning(
                            f"High-frequency pattern detected: {pattern.error_signature} ({pattern.occurrences} occurrences)"
                        )
                        
            return self.detected_patterns
            
        except Exception as e:
            log.error(f"Error in pattern detection: {e}")
            return []
    
    def analyze_pattern_severity(self, pattern: ErrorPattern) -> Dict[ErrorSeverity, int]:
        """Analyze severity distribution for a specific pattern"""
        try:
            severity_counts = {}
            errors = self.error_handler.get_errors_by_pattern(pattern.error_signature)
            
            for error in errors:
                severity = error.severity
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
                
            return severity_counts
            
        except Exception as e:
            log.error(f"Error analyzing pattern severity: {e}")
            return {}
    
    def analyze_pattern_categories(self, pattern: ErrorPattern) -> Dict[str, int]:
        """Analyze category distribution for a specific pattern"""
        try:
            category_counts = {}
            errors = self.error_handler.get_errors_by_pattern(pattern.error_signature)
            
            for error in errors:
                category = error.category
                category_counts[category] = category_counts.get(category, 0) + 1
                
            return category_counts
            
        except Exception as e:
            log.error(f"Error analyzing pattern categories: {e}")
            return {}
    
    def calculate_frequency_score(self, pattern: ErrorPattern) -> float:
        """Calculate frequency score based on occurrence rate"""
        try:
            # Base score on occurrences per day
            if pattern.first_seen and pattern.last_seen:
                days_active = (pattern.last_seen - pattern.first_seen).days + 1
                if days_active > 0:
                    return pattern.occurrences / days_active
            return pattern.occurrences
            
        except Exception as e:
            log.error(f"Error calculating frequency score: {e}")
            return 0.0
    
    def calculate_impact_score(self, pattern: ErrorPattern) -> float:
        """Calculate impact score based on severity and frequency"""
        try:
            severity_weights = {
                ErrorSeverity.LOW: 1.0,
                ErrorSeverity.MEDIUM: 2.0,
                ErrorSeverity.HIGH: 4.0,
                ErrorSeverity.CRITICAL: 8.0
            }
            
            # Get severity distribution
            severity_dist = self.analyze_pattern_severity(pattern)
            
            # Calculate weighted impact
            total_weighted_occurrences = 0
            for severity, count in severity_dist.items():
                weight = severity_weights.get(severity, 1.0)
                total_weighted_occurrences += count * weight
                
            return total_weighted_occurrences / pattern.occurrences if pattern.occurrences > 0 else 0.0
            
        except Exception as e:
            log.error(f"Error calculating impact score: {e}")
            return 0.0
    
    def get_pattern_analysis(self, pattern: ErrorPattern) -> PatternAnalysisResult:
        """Get comprehensive analysis for a specific pattern"""
        try:
            # Check cache first
            if pattern.error_signature in self.pattern_analysis_cache:
                return self.pattern_analysis_cache[pattern.error_signature]
            
            # Perform analysis
            severity_dist = self.analyze_pattern_severity(pattern)
            category_dist = self.analyze_pattern_categories(pattern)
            frequency_score = self.calculate_frequency_score(pattern)
            impact_score = self.calculate_impact_score(pattern)
            
            # Calculate confidence level based on data quality
            confidence = min(1.0, pattern.occurrences / 10.0)  # Higher confidence with more data
            
            result = PatternAnalysisResult(
                pattern_id=pattern.error_signature,
                error_signature=pattern.error_signature,
                occurrences=pattern.occurrences,
                first_seen=pattern.first_seen,
                last_seen=pattern.last_seen,
                severity_distribution=severity_dist,
                category_distribution=category_dist,
                frequency_score=frequency_score,
                impact_score=impact_score,
                confidence_level=confidence
            )
            
            # Cache the result
            self.pattern_analysis_cache[pattern.error_signature] = result
            return result
            
        except Exception as e:
            log.error(f"Error getting pattern analysis: {e}")
            return None
    
    def get_high_priority_patterns(self, threshold: int = 10) -> List[PatternAnalysisResult]:
        """Get patterns that exceed the occurrence threshold"""
        try:
            high_priority = []
            patterns = self.detect_error_patterns()
            
            for pattern in patterns:
                if pattern.occurrences >= threshold:
                    analysis = self.get_pattern_analysis(pattern)
                    if analysis:
                        high_priority.append(analysis)
            
            # Sort by impact score (descending)
            high_priority.sort(key=lambda x: x.impact_score, reverse=True)
            return high_priority
            
        except Exception as e:
            log.error(f"Error getting high priority patterns: {e}")
            return []
    
    def get_pattern_statistics(self) -> Dict[str, Any]:
        """Get pattern detection statistics"""
        try:
            patterns = self.detect_error_patterns()
            
            return {
                "total_patterns": len(patterns),
                "high_frequency_patterns": len([p for p in patterns if p.occurrences >= 10]),
                "patterns_analyzed": len(self.pattern_analysis_cache),
                "cache_hit_rate": len(self.pattern_analysis_cache) / max(len(patterns), 1)
            }
            
        except Exception as e:
            log.error(f"Error getting pattern statistics: {e}")
            return {}
    
    def clear_cache(self):
        """Clear the pattern analysis cache"""
        self.pattern_analysis_cache.clear()
        log.info("Pattern analysis cache cleared")
    
    def shutdown(self):
        """Shutdown the pattern detector"""
        self.clear_cache()
        log.info("Error Pattern Detector shutdown complete")
