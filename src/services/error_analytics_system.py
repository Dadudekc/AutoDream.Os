#!/usr/bin/env python3
"""
Error Analytics System - V2 Error Analysis and Reporting
=======================================================
Comprehensive error analytics system with pattern detection, trend analysis,
and automated reporting for system insights and debugging.
Follows V2 standards with advanced analytics and visualization capabilities.
"""

import logging
import json
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
import statistics
from collections import defaultdict, Counter

# Import our error handling system
from advanced_error_handler import (
    AdvancedErrorHandler, ErrorInfo, ErrorSeverity, ErrorCategory, 
    RecoveryStrategy, ErrorPattern
)

# ──────────────────────────── Logging
log = logging.getLogger("error_analytics_system")

# ────────────────────────── Enums and Data Classes
class AnalysisType(str, Enum):
    """Types of error analysis"""
    PATTERN_DETECTION = "pattern_detection"
    TREND_ANALYSIS = "trend_analysis"
    CORRELATION_ANALYSIS = "correlation_analysis"
    IMPACT_ANALYSIS = "impact_analysis"
    PREDICTIVE_ANALYSIS = "predictive_analysis"

class ReportFormat(str, Enum):
    """Report output formats"""
    JSON = "json"
    MARKDOWN = "markdown"
    HTML = "html"
    CSV = "csv"
    CONSOLE = "console"

@dataclass
class ErrorTrend:
    """Error trend information"""
    time_period: str
    error_count: int
    severity_distribution: Dict[ErrorSeverity, int]
    category_distribution: Dict[ErrorCategory, int]
    recovery_success_rate: float
    average_resolution_time: float

@dataclass
class ErrorCorrelation:
    """Error correlation analysis"""
    primary_error: str
    correlated_errors: List[str]
    correlation_strength: float
    time_window: float
    confidence_level: float

@dataclass
class ErrorImpact:
    """Error impact assessment"""
    service_name: str
    error_count: int
    downtime_minutes: float
    user_affected: int
    business_impact_score: float
    cost_estimate: float

@dataclass
class PredictiveInsight:
    """Predictive analysis insight"""
    insight_type: str
    prediction: str
    confidence: float
    timeframe: str
    recommended_action: str
    evidence: List[str]

@dataclass
class AnalyticsReport:
    """Comprehensive analytics report"""
    report_id: str
    timestamp: datetime
    time_range: str
    summary: Dict[str, Any]
    trends: List[ErrorTrend]
    patterns: List[ErrorPattern]
    correlations: List[ErrorCorrelation]
    impacts: List[ErrorImpact]
    predictions: List[PredictiveInsight]
    recommendations: List[str]

# ────────────────────────── Core Analytics System
class ErrorAnalyticsSystem:
    """Advanced error analytics and reporting system"""
    
    def __init__(self, error_handler: AdvancedErrorHandler, config: Optional[Dict[str, Any]] = None):
        self.error_handler = error_handler
        self.config = config or {}
        self.is_active = True
        self.analytics_thread = None
        
        # Analytics storage
        self.trends: List[ErrorTrend] = []
        self.correlations: List[ErrorCorrelation] = []
        self.impacts: List[ErrorImpact] = []
        self.predictions: List[PredictiveInsight] = []
        
        # Configuration
        self.analysis_interval = self.config.get("analysis_interval", 300)  # 5 minutes
        self.trend_window_hours = self.config.get("trend_window_hours", 24)
        self.correlation_threshold = self.config.get("correlation_threshold", 0.7)
        self.prediction_confidence_threshold = self.config.get("prediction_confidence_threshold", 0.8)
        
        # Performance tracking
        self.stats = {
            "analyses_performed": 0,
            "patterns_detected": 0,
            "trends_identified": 0,
            "correlations_found": 0,
            "predictions_generated": 0,
            "reports_generated": 0
        }
        
        # Initialize analytics system
        self._initialize_analytics()
    
    def _initialize_analytics(self) -> bool:
        """Initialize the analytics system"""
        try:
            # Start analytics thread
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
                    time.sleep(self.analysis_interval)
                except Exception as e:
                    log.error(f"Error in analytics loop: {e}")
        
        self.analytics_thread = threading.Thread(target=analytics_loop, daemon=True)
        self.analytics_thread.start()
    
    def _perform_comprehensive_analysis(self):
        """Perform comprehensive error analysis"""
        try:
            # Pattern detection
            self._detect_error_patterns()
            
            # Trend analysis
            self._analyze_error_trends()
            
            # Correlation analysis
            self._analyze_error_correlations()
            
            # Impact analysis
            self._analyze_error_impacts()
            
            # Predictive analysis
            self._generate_predictive_insights()
            
            self.stats["analyses_performed"] += 1
            
        except Exception as e:
            log.error(f"Error in comprehensive analysis: {e}")
    
    def _detect_error_patterns(self):
        """Detect error patterns and update statistics"""
        try:
            patterns = self.error_handler.get_error_patterns()
            new_patterns = len(patterns) - self.stats["patterns_detected"]
            
            if new_patterns > 0:
                self.stats["patterns_detected"] = len(patterns)
                log.info(f"Detected {new_patterns} new error patterns")
                
                # Analyze pattern severity
                for pattern in patterns:
                    if pattern.occurrences >= 10:
                        log.warning(f"High-frequency pattern detected: {pattern.error_signature} ({pattern.occurrences} occurrences)")
                
        except Exception as e:
            log.error(f"Error in pattern detection: {e}")
    
    def _analyze_error_trends(self):
        """Analyze error trends over time"""
        try:
            # Get recent errors
            recent_errors = self.error_handler.get_error_history(limit=1000)
            
            if not recent_errors:
                return
            
            # Group errors by time periods (hourly)
            current_time = datetime.now()
            time_periods = {}
            
            for error in recent_errors:
                # Round to nearest hour
                hour_key = error.timestamp.replace(minute=0, second=0, microsecond=0)
                
                if hour_key not in time_periods:
                    time_periods[hour_key] = {
                        'errors': [],
                        'severity_counts': defaultdict(int),
                        'category_counts': defaultdict(int),
                        'recovery_successes': 0,
                        'total_errors': 0,
                        'resolution_times': []
                    }
                
                period = time_periods[hour_key]
                period['errors'].append(error)
                period['severity_counts'][error.severity] += 1
                period['category_counts'][error.category] += 1
                period['total_errors'] += 1
                
                if error.resolved:
                    period['recovery_successes'] += 1
                    if error.resolution_time:
                        resolution_time = (error.resolution_time - error.timestamp).total_seconds() / 60
                        period['resolution_times'].append(resolution_time)
            
            # Create trend objects
            new_trends = []
            for hour_key, period_data in time_periods.items():
                recovery_rate = (period_data['recovery_successes'] / period_data['total_errors'] * 100) if period_data['total_errors'] > 0 else 0.0
                avg_resolution = statistics.mean(period_data['resolution_times']) if period_data['resolution_times'] else 0.0
                
                trend = ErrorTrend(
                    time_period=hour_key.strftime("%Y-%m-%d %H:00"),
                    error_count=period_data['total_errors'],
                    severity_distribution=dict(period_data['severity_counts']),
                    category_distribution=dict(period_data['category_counts']),
                    recovery_success_rate=recovery_rate,
                    average_resolution_time=avg_resolution
                )
                
                new_trends.append(trend)
            
            # Update trends (keep last 24 hours)
            self.trends = sorted(new_trends, key=lambda x: x.time_period)[-24:]
            self.stats["trends_identified"] = len(self.trends)
            
        except Exception as e:
            log.error(f"Error in trend analysis: {e}")
    
    def _analyze_error_correlations(self):
        """Analyze correlations between different types of errors"""
        try:
            recent_errors = self.error_handler.get_error_history(limit=500)
            
            if len(recent_errors) < 10:
                return
            
            # Group errors by service and time
            service_errors = defaultdict(list)
            for error in recent_errors:
                service_errors[error.context.service_name].append(error)
            
            # Find correlations between services
            new_correlations = []
            services = list(service_errors.keys())
            
            for i, service1 in enumerate(services):
                for service2 in services[i+1:]:
                    correlation = self._calculate_service_correlation(
                        service_errors[service1], 
                        service_errors[service2]
                    )
                    
                    if correlation > self.correlation_threshold:
                        correlation_obj = ErrorCorrelation(
                            primary_error=service1,
                            correlated_errors=[service2],
                            correlation_strength=correlation,
                            time_window=24.0,  # 24 hours
                            confidence_level=min(correlation * 1.2, 1.0)
                        )
                        new_correlations.append(correlation_obj)
            
            # Update correlations
            self.correlations = new_correlations
            self.stats["correlations_found"] = len(self.correlations)
            
        except Exception as e:
            log.error(f"Error in correlation analysis: {e}")
    
    def _calculate_service_correlation(self, errors1: List[ErrorInfo], 
                                    errors2: List[ErrorInfo]) -> float:
        """Calculate correlation between two services' error patterns"""
        try:
            if not errors1 or not errors2:
                return 0.0
            
            # Create time series for both services
            time_series1 = self._create_error_time_series(errors1)
            time_series2 = self._create_error_time_series(errors2)
            
            # Calculate correlation coefficient
            if len(time_series1) != len(time_series2) or len(time_series1) < 2:
                return 0.0
            
            correlation = statistics.correlation(time_series1, time_series2)
            return abs(correlation) if correlation is not None else 0.0
            
        except Exception:
            return 0.0
    
    def _create_error_time_series(self, errors: List[ErrorInfo]) -> List[int]:
        """Create time series from error list"""
        try:
            # Group errors by hour
            hourly_counts = defaultdict(int)
            for error in errors:
                hour_key = error.timestamp.replace(minute=0, second=0, microsecond=0)
                hourly_counts[hour_key] += 1
            
            # Create 24-hour series
            current_hour = datetime.now().replace(minute=0, second=0, microsecond=0)
            series = []
            
            for i in range(24):
                hour = current_hour - timedelta(hours=i)
                series.append(hourly_counts.get(hour, 0))
            
            return list(reversed(series))
            
        except Exception:
            return [0] * 24
    
    def _analyze_error_impacts(self):
        """Analyze business impact of errors"""
        try:
            recent_errors = self.error_handler.get_error_history(limit=1000)
            
            if not recent_errors:
                return
            
            # Group errors by service
            service_impacts = defaultdict(lambda: {
                'error_count': 0,
                'downtime_minutes': 0.0,
                'critical_errors': 0,
                'recovery_time': 0.0
            })
            
            for error in recent_errors:
                service = error.context.service_name
                impact = service_impacts[service]
                
                impact['error_count'] += 1
                
                if error.severity in [ErrorSeverity.CRITICAL, ErrorSeverity.FATAL]:
                    impact['critical_errors'] += 1
                
                if error.resolved and error.resolution_time:
                    recovery_time = (error.resolution_time - error.timestamp).total_seconds() / 60
                    impact['recovery_time'] += recovery_time
                    impact['downtime_minutes'] += recovery_time
            
            # Calculate impact scores
            new_impacts = []
            for service, impact_data in service_impacts.items():
                # Calculate business impact score (0-100)
                error_score = min(impact_data['error_count'] * 5, 50)
                critical_score = min(impact_data['critical_errors'] * 20, 30)
                downtime_score = min(impact_data['downtime_minutes'] / 10, 20)
                
                business_impact_score = error_score + critical_score + downtime_score
                
                # Estimate cost (rough calculation)
                cost_per_minute = 100  # Example: $100 per minute of downtime
                cost_estimate = impact_data['downtime_minutes'] * cost_per_minute
                
                impact_obj = ErrorImpact(
                    service_name=service,
                    error_count=impact_data['error_count'],
                    downtime_minutes=impact_data['downtime_minutes'],
                    user_affected=impact_data['error_count'] * 10,  # Rough estimate
                    business_impact_score=business_impact_score,
                    cost_estimate=cost_estimate
                )
                
                new_impacts.append(impact_obj)
            
            # Sort by impact score
            self.impacts = sorted(new_impacts, key=lambda x: x.business_impact_score, reverse=True)
            
        except Exception as e:
            log.error(f"Error in impact analysis: {e}")
    
    def _generate_predictive_insights(self):
        """Generate predictive insights based on error patterns"""
        try:
            new_predictions = []
            
            # Analyze error frequency trends
            if len(self.trends) >= 6:  # Need at least 6 hours of data
                recent_trends = self.trends[-6:]
                error_counts = [trend.error_count for trend in recent_trends]
                
                # Check for increasing trend
                if len(error_counts) >= 3:
                    recent_avg = statistics.mean(error_counts[-3:])
                    earlier_avg = statistics.mean(error_counts[:3])
                    
                    if recent_avg > earlier_avg * 1.5:  # 50% increase
                        prediction = PredictiveInsight(
                            insight_type="error_increase",
                            prediction="Error rate is increasing and may continue to rise",
                            confidence=0.75,
                            timeframe="next 2-4 hours",
                            recommended_action="Review system health and prepare for potential issues",
                            evidence=[f"Recent average: {recent_avg:.1f}", f"Earlier average: {earlier_avg:.1f}"]
                        )
                        new_predictions.append(prediction)
            
            # Analyze service dependencies
            if self.correlations:
                high_correlation = max(self.correlations, key=lambda x: x.correlation_strength)
                
                if high_correlation.correlation_strength > 0.8:
                    prediction = PredictiveInsight(
                        insight_type="service_dependency",
                        prediction=f"Service {high_correlation.primary_error} failures may cascade to other services",
                        confidence=high_correlation.confidence_level,
                        timeframe="immediate",
                        recommended_action="Implement circuit breakers and fallback mechanisms",
                        evidence=[f"Correlation strength: {high_correlation.correlation_strength:.2f}"]
                    )
                    new_predictions.append(prediction)
            
            # Analyze recovery patterns
            if self.trends:
                recent_trends = self.trends[-3:]
                recovery_rates = [trend.recovery_success_rate for trend in recent_trends]
                
                if len(recovery_rates) >= 2:
                    avg_recovery_rate = statistics.mean(recovery_rates)
                    
                    if avg_recovery_rate < 70:  # Low recovery rate
                        prediction = PredictiveInsight(
                            insight_type="recovery_degradation",
                            prediction="System recovery capabilities may be degrading",
                            confidence=0.7,
                            timeframe="next 1-2 hours",
                            recommended_action="Review auto-recovery mechanisms and manual intervention procedures",
                            evidence=[f"Average recovery rate: {avg_recovery_rate:.1f}%"]
                        )
                        new_predictions.append(prediction)
            
            # Update predictions
            self.predictions = new_predictions
            self.stats["predictions_generated"] = len(self.predictions)
            
        except Exception as e:
            log.error(f"Error in predictive analysis: {e}")
    
    def generate_analytics_report(self, time_range: str = "24h", 
                                format_type: ReportFormat = ReportFormat.MARKDOWN) -> AnalyticsReport:
        """Generate comprehensive analytics report"""
        try:
            # Create report
            report = AnalyticsReport(
                report_id=f"report_{int(time.time())}",
                timestamp=datetime.now(),
                time_range=time_range,
                summary=self._generate_summary(),
                trends=self.trends.copy(),
                patterns=self.error_handler.get_error_patterns(),
                correlations=self.correlations.copy(),
                impacts=self.impacts.copy(),
                predictions=self.predictions.copy(),
                recommendations=self._generate_recommendations()
            )
            
            self.stats["reports_generated"] += 1
            
            # Format and output report
            self._output_report(report, format_type)
            
            return report
            
        except Exception as e:
            log.error(f"Error generating analytics report: {e}")
            raise
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate summary statistics"""
        try:
            error_stats = self.error_handler.get_error_statistics()
            
            summary = {
                "total_errors": error_stats["total_errors"],
                "recovered_errors": error_stats["recovered_errors"],
                "fatal_errors": error_stats["fatal_errors"],
                "recovery_success_rate": error_stats["recovery_success_rate"],
                "patterns_detected": len(self.error_handler.get_error_patterns()),
                "trends_analyzed": len(self.trends),
                "correlations_found": len(self.correlations),
                "high_impact_services": len([i for i in self.impacts if i.business_impact_score > 50]),
                "predictions_active": len(self.predictions),
                "system_health_score": self._calculate_system_health_score()
            }
            
            return summary
            
        except Exception as e:
            log.error(f"Error generating summary: {e}")
            return {}
    
    def _calculate_system_health_score(self) -> float:
        """Calculate overall system health score (0-100)"""
        try:
            error_stats = self.error_handler.get_error_statistics()
            
            if error_stats["total_errors"] == 0:
                return 100.0
            
            # Base score from recovery rate
            base_score = error_stats["recovery_success_rate"]
            
            # Penalties for various issues
            penalty = 0
            
            # High error rate penalty
            if error_stats["total_errors"] > 100:
                penalty += 20
            
            # Fatal errors penalty
            if error_stats["fatal_errors"] > 0:
                penalty += 30
            
            # Low pattern detection penalty
            if len(self.error_handler.get_error_patterns()) < 3:
                penalty += 10
            
            # High impact services penalty
            high_impact_count = len([i for i in self.impacts if i.business_impact_score > 70])
            penalty += high_impact_count * 5
            
            final_score = max(0, base_score - penalty)
            return min(100, final_score)
            
        except Exception:
            return 50.0
    
    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations"""
        try:
            recommendations = []
            
            # Recovery rate recommendations
            error_stats = self.error_handler.get_error_statistics()
            if error_stats["recovery_success_rate"] < 80:
                recommendations.append("Improve auto-recovery mechanisms and implement better fallback strategies")
            
            # Pattern-based recommendations
            patterns = self.error_handler.get_error_patterns()
            high_frequency_patterns = [p for p in patterns if p.occurrences > 10]
            if high_frequency_patterns:
                recommendations.append(f"Investigate and resolve {len(high_frequency_patterns)} high-frequency error patterns")
            
            # Service dependency recommendations
            if self.correlations:
                recommendations.append("Implement circuit breakers and service isolation to prevent cascading failures")
            
            # Impact-based recommendations
            critical_services = [i for i in self.impacts if i.business_impact_score > 80]
            if critical_services:
                recommendations.append(f"Prioritize fixes for {len(critical_services)} critical services with high business impact")
            
            # Predictive recommendations
            if self.predictions:
                recommendations.append("Act on predictive insights to prevent potential issues before they occur")
            
            # General recommendations
            if not recommendations:
                recommendations.append("System is performing well - continue monitoring and preventive maintenance")
            
            return recommendations
            
        except Exception as e:
            log.error(f"Error generating recommendations: {e}")
            return ["Error generating recommendations"]
    
    def _output_report(self, report: AnalyticsReport, format_type: ReportFormat):
        """Output report in specified format"""
        try:
            if format_type == ReportFormat.CONSOLE:
                self._output_console_report(report)
            elif format_type == ReportFormat.MARKDOWN:
                self._output_markdown_report(report)
            elif format_type == ReportFormat.JSON:
                self._output_json_report(report)
            elif format_type == ReportFormat.HTML:
                self._output_html_report(report)
            elif format_type == ReportFormat.CSV:
                self._output_csv_report(report)
                
        except Exception as e:
            log.error(f"Error outputting report: {e}")
    
    def _output_console_report(self, report: AnalyticsReport):
        """Output report to console"""
        print("\n" + "="*80)
        print("ERROR ANALYTICS REPORT")
        print("="*80)
        print(f"Generated: {report.timestamp}")
        print(f"Time Range: {report.time_range}")
        print(f"Report ID: {report.report_id}")
        
        # Summary
        print("\n📊 SUMMARY")
        print("-" * 40)
        for key, value in report.summary.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        
        # Trends
        if report.trends:
            print("\n📈 TRENDS (Last 6 hours)")
            print("-" * 40)
            for trend in report.trends[-6:]:
                print(f"  {trend.time_period}: {trend.error_count} errors, "
                      f"{trend.recovery_success_rate:.1f}% recovery rate")
        
        # Patterns
        if report.patterns:
            print("\n🔍 ERROR PATTERNS")
            print("-" * 40)
            for pattern in report.patterns[:5]:  # Top 5
                print(f"  {pattern.error_signature}: {pattern.occurrences} occurrences")
        
        # Recommendations
        if report.recommendations:
            print("\n💡 RECOMMENDATIONS")
            print("-" * 40)
            for i, rec in enumerate(report.recommendations, 1):
                print(f"  {i}. {rec}")
        
        print("\n" + "="*80)
    
    def _output_markdown_report(self, report: AnalyticsReport):
        """Output report in Markdown format"""
        try:
            report_path = f"reports/error_analytics_{report.report_id}.md"
            Path("reports").mkdir(exist_ok=True)
            
            with open(report_path, 'w') as f:
                f.write(f"# Error Analytics Report\n\n")
                f.write(f"**Generated:** {report.timestamp}\n")
                f.write(f"**Time Range:** {report.time_range}\n")
                f.write(f"**Report ID:** {report.report_id}\n\n")
                
                # Summary
                f.write("## Summary\n\n")
                for key, value in report.summary.items():
                    f.write(f"- **{key.replace('_', ' ').title()}:** {value}\n")
                f.write("\n")
                
                # Trends
                if report.trends:
                    f.write("## Error Trends\n\n")
                    f.write("| Time Period | Error Count | Recovery Rate |\n")
                    f.write("|-------------|-------------|---------------|\n")
                    for trend in report.trends[-6:]:
                        f.write(f"| {trend.time_period} | {trend.error_count} | {trend.recovery_success_rate:.1f}% |\n")
                    f.write("\n")
                
                # Patterns
                if report.patterns:
                    f.write("## Error Patterns\n\n")
                    for pattern in report.patterns[:10]:
                        f.write(f"### {pattern.error_signature}\n")
                        f.write(f"- **Occurrences:** {pattern.occurrences}\n")
                        f.write(f"- **First Seen:** {pattern.first_seen}\n")
                        f.write(f"- **Last Seen:** {pattern.last_seen}\n")
                        f.write(f"- **Affected Services:** {', '.join(pattern.affected_services)}\n")
                        f.write(f"- **Suggested Resolution:** {pattern.suggested_resolution}\n\n")
                
                # Recommendations
                if report.recommendations:
                    f.write("## Recommendations\n\n")
                    for i, rec in enumerate(report.recommendations, 1):
                        f.write(f"{i}. {rec}\n")
                    f.write("\n")
            
            log.info(f"Markdown report saved to {report_path}")
            
        except Exception as e:
            log.error(f"Error saving markdown report: {e}")
    
    def _output_json_report(self, report: AnalyticsReport):
        """Output report in JSON format"""
        try:
            report_path = f"reports/error_analytics_{report.report_id}.json"
            Path("reports").mkdir(exist_ok=True)
            
            with open(report_path, 'w') as f:
                json.dump(asdict(report), f, default=str, indent=2)
            
            log.info(f"JSON report saved to {report_path}")
            
        except Exception as e:
            log.error(f"Error saving JSON report: {e}")
    
    def _output_html_report(self, report: AnalyticsReport):
        """Output report in HTML format"""
        try:
            report_path = f"reports/error_analytics_{report.report_id}.html"
            Path("reports").mkdir(exist_ok=True)
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Error Analytics Report</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                    .section {{ margin: 20px 0; }}
                    .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; }}
                    .summary-item {{ background-color: #e8f4f8; padding: 10px; border-radius: 3px; }}
                    table {{ border-collapse: collapse; width: 100%; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Error Analytics Report</h1>
                    <p><strong>Generated:</strong> {report.timestamp}</p>
                    <p><strong>Time Range:</strong> {report.time_range}</p>
                    <p><strong>Report ID:</strong> {report.report_id}</p>
                </div>
                
                <div class="section">
                    <h2>Summary</h2>
                    <div class="summary">
            """
            
            for key, value in report.summary.items():
                html_content += f"""
                        <div class="summary-item">
                            <strong>{key.replace('_', ' ').title()}</strong><br>
                            {value}
                        </div>
                """
            
            html_content += """
                    </div>
                </div>
                
                <div class="section">
                    <h2>Recommendations</h2>
                    <ul>
            """
            
            for rec in report.recommendations:
                html_content += f"<li>{rec}</li>"
            
            html_content += """
                    </ul>
                </div>
            </body>
            </html>
            """
            
            with open(report_path, 'w') as f:
                f.write(html_content)
            
            log.info(f"HTML report saved to {report_path}")
            
        except Exception as e:
            log.error(f"Error saving HTML report: {e}")
    
    def _output_csv_report(self, report: AnalyticsReport):
        """Output report in CSV format"""
        try:
            report_path = f"reports/error_analytics_{report.report_id}.csv"
            Path("reports").mkdir(exist_ok=True)
            
            with open(report_path, 'w') as f:
                # Summary
                f.write("Category,Value\n")
                for key, value in report.summary.items():
                    f.write(f"{key.replace('_', ' ').title()},{value}\n")
                
                # Trends
                if report.trends:
                    f.write("\nTime Period,Error Count,Recovery Rate\n")
                    for trend in report.trends:
                        f.write(f"{trend.time_period},{trend.error_count},{trend.recovery_success_rate:.1f}\n")
                
                # Patterns
                if report.patterns:
                    f.write("\nPattern,Occurrences,First Seen,Last Seen\n")
                    for pattern in report.patterns:
                        f.write(f"{pattern.error_signature},{pattern.occurrences},{pattern.first_seen},{pattern.last_seen}\n")
            
            log.info(f"CSV report saved to {report_path}")
            
        except Exception as e:
            log.error(f"Error saving CSV report: {e}")
    
    def get_analytics_statistics(self) -> Dict[str, Any]:
        """Get analytics system statistics"""
        return {
            **self.stats,
            "trends_available": len(self.trends),
            "correlations_available": len(self.correlations),
            "impacts_analyzed": len(self.impacts),
            "predictions_active": len(self.predictions)
        }
    
    def shutdown(self):
        """Shutdown the analytics system"""
        self.is_active = False
        
        # Wait for analytics thread
        if self.analytics_thread and self.analytics_thread.is_alive():
            self.analytics_thread.join(timeout=5.0)
        
        log.info("Error Analytics System shutdown complete")
