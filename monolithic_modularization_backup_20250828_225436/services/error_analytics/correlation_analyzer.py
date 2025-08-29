from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import logging

from __future__ import annotations
from dataclasses import dataclass
from error analytics data. Follows V2 standards with advanced
from src.core.error_handler import (
import statistics

#!/usr/bin/env python3
"""
Error Correlation Analyzer - V2 Error Correlation Analysis
=========================================================
Specialized module for analyzing error correlations and relationships
correlation detection and analysis capabilities.
"""



# Import our error handling system
    ErrorHandler,
    ErrorInfo,
    ErrorSeverity,
)

# ──────────────────────────── Logging
log = logging.getLogger("error_correlation_analyzer")


@dataclass
class ErrorCorrelation:
    """Error correlation analysis"""
    
    primary_error: str
    correlated_errors: List[str]
    correlation_strength: float
    time_window: float
    confidence_level: float
    correlation_type: str  # "temporal", "causal", "sequential"
    impact_score: float


@dataclass
class CorrelationAnalysisResult:
    """Result of correlation analysis"""
    
    total_correlations: int
    strong_correlations: int
    moderate_correlations: int
    weak_correlations: int
    correlations_by_type: Dict[str, int]
    top_correlations: List[ErrorCorrelation]
    correlation_matrix: Dict[str, Dict[str, float]]


class ErrorCorrelationAnalyzer:
    """Advanced error correlation analysis and detection"""

    def __init__(self, error_handler: ErrorHandler, config: Optional[Dict[str, Any]] = None):
        self.error_handler = error_handler
        self.config = config or {}
        self.correlations: List[ErrorCorrelation] = []
        
        # Configuration
        self.correlation_threshold = self.config.get("correlation_threshold", 0.7)
        self.time_window_minutes = self.config.get("time_window_minutes", 30)
        self.minimum_correlation_confidence = self.config.get("minimum_correlation_confidence", 0.6)
        
    def analyze_error_correlations(self) -> List[ErrorCorrelation]:
        """Analyze error correlations and relationships"""
        try:
            # Get recent errors
            recent_errors = self.error_handler.get_error_history(limit=1000)
            
            if not recent_errors:
                return []
            
            # Group errors by time windows
            time_windows = self._group_errors_by_time_windows(recent_errors)
            
            # Analyze correlations within each time window
            new_correlations = []
            for window_start, window_errors in time_windows.items():
                if len(window_errors) > 1:
                    window_correlations = self._analyze_window_correlations(window_errors)
                    new_correlations.extend(window_correlations)
            
            # Merge and deduplicate correlations
            self.correlations = self._merge_correlations(new_correlations)
            
            log.info(f"Analyzed {len(self.correlations)} error correlations")
            return self.correlations
            
        except Exception as e:
            log.error(f"Error in correlation analysis: {e}")
            return []
    
    def _group_errors_by_time_windows(self, errors: List[ErrorInfo]) -> Dict[datetime, List[ErrorInfo]]:
        """Group errors by time windows for correlation analysis"""
        try:
            time_windows = defaultdict(list)
            
            for error in errors:
                # Round to nearest time window
                window_start = error.timestamp.replace(
                    minute=(error.timestamp.minute // self.time_window_minutes) * self.time_window_minutes,
                    second=0,
                    microsecond=0
                )
                time_windows[window_start].append(error)
            
            return dict(time_windows)
            
        except Exception as e:
            log.error(f"Error grouping errors by time windows: {e}")
            return {}
    
    def _analyze_window_correlations(self, window_errors: List[ErrorInfo]) -> List[ErrorCorrelation]:
        """Analyze correlations within a specific time window"""
        try:
            correlations = []
            
            # Get unique error types in this window
            error_types = list(set(error.error_type for error in window_errors))
            
            if len(error_types) < 2:
                return []
            
            # Analyze correlations between all pairs of error types
            for i, primary_type in enumerate(error_types):
                for secondary_type in error_types[i+1:]:
                    correlation = self._calculate_error_correlation(
                        window_errors, primary_type, secondary_type
                    )
                    if correlation and correlation.correlation_strength >= self.correlation_threshold:
                        correlations.append(correlation)
            
            return correlations
            
        except Exception as e:
            log.error(f"Error analyzing window correlations: {e}")
            return []
    
    def _calculate_error_correlation(
        self, 
        errors: List[ErrorInfo], 
        error_type_1: str, 
        error_type_2: str
    ) -> Optional[ErrorCorrelation]:
        """Calculate correlation between two error types"""
        try:
            # Count occurrences of each error type
            type_1_count = sum(1 for e in errors if e.error_type == error_type_1)
            type_2_count = sum(1 for e in errors if e.error_type == error_type_2)
            
            if type_1_count == 0 or type_2_count == 0:
                return None
            
            # Calculate correlation strength using Jaccard similarity
            total_errors = len(errors)
            intersection = type_1_count + type_2_count - total_errors
            union = type_1_count + type_2_count - intersection
            
            if union == 0:
                return None
            
            correlation_strength = intersection / union
            
            # Calculate confidence based on data quality
            confidence = min(1.0, min(type_1_count, type_2_count) / 5.0)
            
            # Determine correlation type
            correlation_type = self._determine_correlation_type(errors, error_type_1, error_type_2)
            
            # Calculate impact score
            impact_score = self._calculate_correlation_impact(errors, error_type_1, error_type_2)
            
            correlation = ErrorCorrelation(
                primary_error=error_type_1,
                correlated_errors=[error_type_2],
                correlation_strength=correlation_strength,
                time_window=self.time_window_minutes,
                confidence_level=confidence,
                correlation_type=correlation_type,
                impact_score=impact_score
            )
            
            return correlation
            
        except Exception as e:
            log.error(f"Error calculating error correlation: {e}")
            return None
    
    def _determine_correlation_type(
        self, 
        errors: List[ErrorInfo], 
        error_type_1: str, 
        error_type_2: str
    ) -> str:
        """Determine the type of correlation between two error types"""
        try:
            # Get timestamps for each error type
            type_1_timestamps = [e.timestamp for e in errors if e.error_type == error_type_1]
            type_2_timestamps = [e.timestamp for e in errors if e.error_type == error_type_2]
            
            if not type_1_timestamps or not type_2_timestamps:
                return "unknown"
            
            # Check for sequential correlation (one follows the other)
            sequential_count = 0
            for ts1 in type_1_timestamps:
                for ts2 in type_2_timestamps:
                    time_diff = abs((ts2 - ts1).total_seconds())
                    if 0 < time_diff <= 300:  # Within 5 minutes
                        sequential_count += 1
            
            if sequential_count > 0:
                return "sequential"
            
            # Check for temporal correlation (occurring at similar times)
            temporal_count = 0
            for ts1 in type_1_timestamps:
                for ts2 in type_2_timestamps:
                    time_diff = abs((ts2 - ts1).total_seconds())
                    if time_diff <= 60:  # Within 1 minute
                        temporal_count += 1
            
            if temporal_count > 0:
                return "temporal"
            
            return "causal"
            
        except Exception as e:
            log.error(f"Error determining correlation type: {e}")
            return "unknown"
    
    def _calculate_correlation_impact(
        self, 
        errors: List[ErrorInfo], 
        error_type_1: str, 
        error_type_2: str
    ) -> float:
        """Calculate the impact score for a correlation"""
        try:
            # Get errors of both types
            type_1_errors = [e for e in errors if e.error_type == error_type_1]
            type_2_errors = [e for e in errors if e.error_type == error_type_2]
            
            # Calculate average severity for each type
            severity_weights = {
                ErrorSeverity.LOW: 1.0,
                ErrorSeverity.MEDIUM: 2.0,
                ErrorSeverity.HIGH: 4.0,
                ErrorSeverity.CRITICAL: 8.0
            }
            
            def calculate_type_impact(error_list):
                if not error_list:
                    return 0.0
                
                total_weight = 0
                for error in error_list:
                    weight = severity_weights.get(error.severity, 1.0)
                    total_weight += weight
                
                return total_weight / len(error_list)
            
            impact_1 = calculate_type_impact(type_1_errors)
            impact_2 = calculate_type_impact(type_2_errors)
            
            # Return average impact
            return (impact_1 + impact_2) / 2.0
            
        except Exception as e:
            log.error(f"Error calculating correlation impact: {e}")
            return 0.0
    
    def _merge_correlations(self, correlations: List[ErrorCorrelation]) -> List[ErrorCorrelation]:
        """Merge and deduplicate correlations"""
        try:
            if not correlations:
                return []
            
            # Group by primary error
            correlation_groups = defaultdict(list)
            for corr in correlations:
                correlation_groups[corr.primary_error].append(corr)
            
            # Merge correlations for each primary error
            merged_correlations = []
            for primary_error, corr_list in correlation_groups.items():
                if len(corr_list) == 1:
                    merged_correlations.append(corr_list[0])
                else:
                    # Merge multiple correlations for the same primary error
                    merged_corr = self._merge_correlation_group(corr_list)
                    if merged_corr:
                        merged_correlations.append(merged_corr)
            
            # Sort by correlation strength (descending)
            merged_correlations.sort(key=lambda x: x.correlation_strength, reverse=True)
            
            return merged_correlations
            
        except Exception as e:
            log.error(f"Error merging correlations: {e}")
            return correlations
    
    def _merge_correlation_group(self, correlations: List[ErrorCorrelation]) -> Optional[ErrorCorrelation]:
        """Merge a group of correlations for the same primary error"""
        try:
            if not correlations:
                return None
            
            if len(correlations) == 1:
                return correlations[0]
            
            # Merge correlated errors
            all_correlated = []
            for corr in correlations:
                all_correlated.extend(corr.correlated_errors)
            
            # Remove duplicates
            unique_correlated = list(set(all_correlated))
            
            # Calculate average correlation strength and confidence
            avg_strength = statistics.mean([c.correlation_strength for c in correlations])
            avg_confidence = statistics.mean([c.confidence_level for c in correlations])
            avg_impact = statistics.mean([c.impact_score for c in correlations])
            
            # Determine most common correlation type
            type_counts = defaultdict(int)
            for corr in correlations:
                type_counts[corr.correlation_type] += 1
            
            most_common_type = max(type_counts.items(), key=lambda x: x[1])[0]
            
            merged_correlation = ErrorCorrelation(
                primary_error=correlations[0].primary_error,
                correlated_errors=unique_correlated,
                correlation_strength=avg_strength,
                time_window=self.time_window_minutes,
                confidence_level=avg_confidence,
                correlation_type=most_common_type,
                impact_score=avg_impact
            )
            
            return merged_correlation
            
        except Exception as e:
            log.error(f"Error merging correlation group: {e}")
            return correlations[0] if correlations else None
    
    def get_correlation_statistics(self) -> Dict[str, Any]:
        """Get correlation analysis statistics"""
        try:
            if not self.correlations:
                return {}
            
            strong_correlations = [c for c in self.correlations if c.correlation_strength >= 0.8]
            moderate_correlations = [c for c in self.correlations if 0.6 <= c.correlation_strength < 0.8]
            weak_correlations = [c for c in self.correlations if c.correlation_strength < 0.6]
            
            # Group by correlation type
            type_counts = defaultdict(int)
            for corr in self.correlations:
                type_counts[corr.correlation_type] += 1
            
            return {
                "total_correlations": len(self.correlations),
                "strong_correlations": len(strong_correlations),
                "moderate_correlations": len(moderate_correlations),
                "weak_correlations": len(weak_correlations),
                "correlations_by_type": dict(type_counts),
                "average_correlation_strength": statistics.mean([c.correlation_strength for c in self.correlations]),
                "average_confidence": statistics.mean([c.confidence_level for c in self.correlations])
            }
            
        except Exception as e:
            log.error(f"Error getting correlation statistics: {e}")
            return {}
    
    def get_correlations_by_type(self, correlation_type: str) -> List[ErrorCorrelation]:
        """Get correlations filtered by type"""
        try:
            return [c for c in self.correlations if c.correlation_type == correlation_type]
        except Exception as e:
            log.error(f"Error getting correlations by type: {e}")
            return []
    
    def get_correlations_by_strength(self, min_strength: float = 0.0, max_strength: float = 1.0) -> List[ErrorCorrelation]:
        """Get correlations filtered by strength range"""
        try:
            return [
                c for c in self.correlations 
                if min_strength <= c.correlation_strength <= max_strength
            ]
        except Exception as e:
            log.error(f"Error getting correlations by strength: {e}")
            return []
    
    def get_top_correlations(self, limit: int = 10) -> List[ErrorCorrelation]:
        """Get top correlations by strength and impact"""
        try:
            # Sort by combined score (strength * impact * confidence)
            sorted_correlations = sorted(
                self.correlations,
                key=lambda x: x.correlation_strength * x.impact_score * x.confidence_level,
                reverse=True
            )
            
            return sorted_correlations[:limit]
            
        except Exception as e:
            log.error(f"Error getting top correlations: {e}")
            return []
    
    def get_comprehensive_correlation_analysis(self) -> CorrelationAnalysisResult:
        """Get comprehensive correlation analysis"""
        try:
            # Analyze correlations
            correlations = self.analyze_error_correlations()
            
            # Get statistics
            stats = self.get_correlation_statistics()
            
            # Get top correlations
            top_correlations = self.get_top_correlations()
            
            # Build correlation matrix
            correlation_matrix = self._build_correlation_matrix()
            
            result = CorrelationAnalysisResult(
                total_correlations=stats.get("total_correlations", 0),
                strong_correlations=stats.get("strong_correlations", 0),
                moderate_correlations=stats.get("moderate_correlations", 0),
                weak_correlations=stats.get("weak_correlations", 0),
                correlations_by_type=stats.get("correlations_by_type", {}),
                top_correlations=top_correlations,
                correlation_matrix=correlation_matrix
            )
            
            return result
            
        except Exception as e:
            log.error(f"Error getting comprehensive correlation analysis: {e}")
            return None
    
    def _build_correlation_matrix(self) -> Dict[str, Dict[str, float]]:
        """Build a correlation matrix for all error types"""
        try:
            matrix = {}
            
            # Get all unique error types
            all_error_types = set()
            for corr in self.correlations:
                all_error_types.add(corr.primary_error)
                all_error_types.add(corr.correlated_errors[0])  # Assuming single correlation for now
            
            # Initialize matrix
            for error_type in all_error_types:
                matrix[error_type] = {other_type: 0.0 for other_type in all_error_types}
                matrix[error_type][error_type] = 1.0  # Self-correlation
            
            # Fill matrix with correlation values
            for corr in self.correlations:
                primary = corr.primary_error
                for correlated in corr.correlated_errors:
                    if primary in matrix and correlated in matrix[primary]:
                        matrix[primary][correlated] = corr.correlation_strength
                        matrix[correlated][primary] = corr.correlation_strength
            
            return matrix
            
        except Exception as e:
            log.error(f"Error building correlation matrix: {e}")
            return {}
    
    def shutdown(self):
        """Shutdown the correlation analyzer"""
        self.correlations.clear()
        log.info("Error Correlation Analyzer shutdown complete")
