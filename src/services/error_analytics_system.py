#!/usr/bin/env python3
"""
Error Analytics System - V2 Error Analysis and Reporting
=======================================================
Comprehensive error analytics system that orchestrates specialized modules
for pattern detection, trend analysis, correlation analysis, and reporting.
Follows V2 standards with advanced analytics and visualization capabilities.
"""

import logging
import time
import threading
from typing import Dict, List, Optional, Any
from datetime import datetime

# Import our error handling system
from src.core.error_handler import ErrorHandler

# Import extracted analytics modules
from .error_analytics import (
    ErrorPatternDetector,
    ErrorTrendAnalyzer,
    ErrorCorrelationAnalyzer,
    ErrorReportGenerator,
    ReportFormat
)

# ──────────────────────────── Logging
log = logging.getLogger("error_analytics_system")
    
# ────────────────────────── Core Analytics System
class ErrorAnalyticsSystem:
    """Advanced error analytics and reporting system that orchestrates specialized modules"""

    def __init__(
        self,
        error_handler: ErrorHandler,
        config: Optional[Dict[str, Any]] = None,
    ):
        self.error_handler = error_handler
        self.config = config or {}
        self.is_active = True
        self.analytics_thread = None

        # Initialize specialized analytics modules
        self.pattern_detector = ErrorPatternDetector(error_handler)
        self.trend_analyzer = ErrorTrendAnalyzer(error_handler, config)
        self.correlation_analyzer = ErrorCorrelationAnalyzer(error_handler, config)
        self.report_generator = ErrorReportGenerator(config)
        
        # Performance tracking
        self.stats = {
            "analyses_performed": 0,
            "patterns_detected": 0,
            "trends_identified": 0,
            "correlations_found": 0,
            "reports_generated": 0,
        }
        
        # Initialize analytics system
        self._initialize_analytics()
    
    def _initialize_analytics(self) -> bool:
        """Initialize the analytics system"""
        try:
            if self.config.get("enable_background_thread", True):
                self._start_analytics_thread()

            log.info("Error Analytics System initialized successfully")
            return True

        except Exception as e:
            log.error(f"Failed to initialize analytics system: {e}")
            return False
    
    def _start_analytics_thread(self):
        """Start background analytics processing"""
        
        def analytics_loop():
            while self.is_active:
                try:
                    self._perform_comprehensive_analysis()
                    time.sleep(self.config.get("analysis_interval", 300))
                except Exception as e:
                    log.error(f"Error in analytics loop: {e}")
        
        self.analytics_thread = threading.Thread(target=analytics_loop, daemon=True)
        self.analytics_thread.start()
    
    def _perform_comprehensive_analysis(self):
        """Perform comprehensive error analysis using specialized modules"""
        try:
            # Pattern detection using specialized module
            patterns = self.pattern_detector.detect_error_patterns()
            self.stats["patterns_detected"] = len(patterns)
            
            # Trend analysis using specialized module
            trends = self.trend_analyzer.analyze_error_trends()
            self.stats["trends_identified"] = len(trends)
            
            # Correlation analysis using specialized module
            correlations = self.correlation_analyzer.analyze_error_correlations()
            self.stats["correlations_found"] = len(correlations)
            
            self.stats["analyses_performed"] += 1
            
        except Exception as e:
            log.error(f"Error in comprehensive analysis: {e}")
    
    def get_pattern_analysis(self):
        """Get pattern analysis from specialized module"""
        try:
            return self.pattern_detector.get_high_priority_patterns()
        except Exception as e:
            log.error(f"Error getting pattern analysis: {e}")
            return []
    
    def get_trend_analysis(self):
        """Get trend analysis from specialized module"""
        try:
            return self.trend_analyzer.get_comprehensive_trend_analysis()
        except Exception as e:
            log.error(f"Error getting trend analysis: {e}")
            return None
    
    def get_correlation_analysis(self):
        """Get correlation analysis from specialized module"""
        try:
            return self.correlation_analyzer.get_comprehensive_correlation_analysis()
        except Exception as e:
            log.error(f"Error getting correlation analysis: {e}")
            return None
    
    def generate_report(self, format_type: ReportFormat = ReportFormat.JSON):
        """Generate comprehensive report using specialized module"""
        try:
            # Get data from all modules
            patterns = self.pattern_detector.detect_error_patterns()
            trends = self.trend_analyzer.analyze_error_trends()
            correlations = self.correlation_analyzer.analyze_error_correlations()
            
            # Convert to dictionaries for report generation
            pattern_dicts = [self._pattern_to_dict(p) for p in patterns]
            trend_dicts = [self._trend_to_dict(t) for t in trends]
            correlation_dicts = [self._correlation_to_dict(c) for c in correlations]
            
            # Generate report
            report = self.report_generator.generate_comprehensive_report(
                patterns=pattern_dicts,
                trends=trend_dicts,
                correlations=correlation_dicts,
                format_type=format_type
            )
            
            self.stats["reports_generated"] += 1
            return report
            
        except Exception as e:
            log.error(f"Error generating report: {e}")
            return None
    
    def _pattern_to_dict(self, pattern):
        """Convert pattern object to dictionary for report generation"""
        try:
            return {
                "error_signature": getattr(pattern, "error_signature", "Unknown"),
                "occurrences": getattr(pattern, "occurrences", 0),
                "first_seen": getattr(pattern, "first_seen", None),
                "last_seen": getattr(pattern, "last_seen", None),
                "severity_distribution": getattr(pattern, "severity_distribution", {}),
                "category_distribution": getattr(pattern, "category_distribution", {})
            }
        except Exception as e:
            log.error(f"Error converting pattern to dict: {e}")
            return {}
    
    def _trend_to_dict(self, trend):
        """Convert trend object to dictionary for report generation"""
        try:
            return {
                "time_period": getattr(trend, "time_period", "Unknown"),
                "error_count": getattr(trend, "error_count", 0),
                "trend_direction": getattr(trend, "trend_direction", "unknown"),
                "trend_confidence": getattr(trend, "trend_confidence", 0.0)
            }
        except Exception as e:
            log.error(f"Error converting trend to dict: {e}")
            return {}
    
    def _correlation_to_dict(self, correlation):
        """Convert correlation object to dictionary for report generation"""
        try:
            return {
                "primary_error": getattr(correlation, "primary_error", "Unknown"),
                "correlated_errors": getattr(correlation, "correlated_errors", []),
                "correlation_strength": getattr(correlation, "correlation_strength", 0.0),
                "correlation_type": getattr(correlation, "correlation_type", "unknown")
            }
        except Exception as e:
            log.error(f"Error converting correlation to dict: {e}")
            return {}
    
    def get_analytics_statistics(self) -> Dict[str, Any]:
        """Get comprehensive analytics statistics from all modules"""
        try:
            pattern_stats = self.pattern_detector.get_pattern_statistics()
            trend_stats = self.trend_analyzer.get_trend_statistics()
            correlation_stats = self.correlation_analyzer.get_correlation_statistics()
            report_stats = self.report_generator.get_report_statistics()
            
            return {
                **self.stats,
                "pattern_analysis": pattern_stats,
                "trend_analysis": trend_stats,
                "correlation_analysis": correlation_stats,
                "report_generation": report_stats
            }
            
        except Exception as e:
            log.error(f"Error getting analytics statistics: {e}")
            return self.stats
    
    def shutdown(self):
        """Shutdown the analytics system and all modules"""
        self.is_active = False
        
        # Wait for analytics thread
        if self.analytics_thread and self.analytics_thread.is_alive():
            self.analytics_thread.join(timeout=5.0)
        
        # Shutdown all modules
        try:
            self.pattern_detector.shutdown()
            self.trend_analyzer.shutdown()
            self.correlation_analyzer.shutdown()
            self.report_generator.shutdown()
        except Exception as e:
            log.error(f"Error shutting down modules: {e}")
        
        log.info("Error Analytics System shutdown complete")
