#!/usr/bin/env python3
"""
Refactoring Performance Metrics Integration - Agent-5
====================================================

This module provides a unified interface for all REFACTOR-003 components,
integrating the performance metrics system, dashboard, and baseline measurements.

Features:
- Unified metrics collection and analysis
- Integrated dashboard and baseline management
- Comprehensive reporting and export capabilities
- Automated performance monitoring and alerts
- End-to-end refactoring performance tracking

Author: Agent-5 (REFACTORING MANAGER)
Contract: REFACTOR-003
Status: In Progress
"""

import os
import sys
import json
import logging
import asyncio
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime, timedelta
import traceback

sys.path.append(str(Path(__file__).parent.parent.parent))
from core.managers.base_manager import BaseManager
from core.refactoring.refactoring_performance_metrics import RefactoringPerformanceMetrics
from core.refactoring.performance_dashboard import RefactoringPerformanceDashboard
from core.refactoring.baseline_measurements import RefactoringBaselineMeasurements

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RefactoringMetricsIntegration(BaseManager):
    """
    Unified interface for all REFACTOR-003 components.
    
    This system integrates:
    - Performance metrics collection and analysis
    - Real-time dashboard monitoring
    - Baseline measurements and comparison
    - Automated reporting and alerts
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the integrated refactoring metrics system"""
        super().__init__(config or {})
        self.metrics_system = RefactoringPerformanceMetrics()
        self.dashboard = RefactoringPerformanceDashboard()
        self.baseline_system = RefactoringBaselineMeasurements()
        self.integration_config = self._initialize_integration_config()
        self.active_sessions = {}
        
    def _initialize_integration_config(self) -> Dict[str, Any]:
        """Initialize integration configuration"""
        return {
            "auto_monitoring_enabled": True,
            "monitoring_interval": 60,  # seconds
            "auto_baseline_calibration": True,
            "calibration_threshold": 0.8,
            "alert_integration": True,
            "reporting_enabled": True,
            "export_formats": ["json", "csv"],
            "performance_thresholds": {
                "critical_complexity": 20,
                "critical_maintainability": 0.4,
                "critical_duplication": 0.25,
                "critical_duration": 600
            }
        }
    
    def start_refactoring_session(self, operation_name: str, target_files: List[str],
                                description: str = "") -> str:
        """Start a comprehensive refactoring monitoring session"""
        try:
            # Start metrics session
            session_id = self.metrics_system.start_metrics_session(operation_name, target_files)
            
            # Create session context
            session_context = {
                "session_id": session_id,
                "operation_name": operation_name,
                "target_files": target_files,
                "description": description,
                "start_time": datetime.now(),
                "metrics_system": self.metrics_system,
                "dashboard": self.dashboard,
                "baseline_system": self.baseline_system,
                "status": "active"
            }
            
            self.active_sessions[session_id] = session_context
            
            logger.info(f"Started refactoring session: {session_id} for {operation_name}")
            return session_id
            
        except Exception as e:
            logger.error(f"Error starting refactoring session: {e}")
            raise
    
    def end_refactoring_session(self, session_id: str) -> Dict[str, Any]:
        """End a refactoring session and generate comprehensive report"""
        if session_id not in self.active_sessions:
            raise ValueError(f"Invalid session ID: {session_id}")
        
        try:
            session_context = self.active_sessions[session_id]
            
            # End metrics session
            metrics_summary = self.metrics_system.end_metrics_session(session_id)
            
            # Generate comprehensive analysis
            analysis_results = self._generate_session_analysis(session_context, metrics_summary)
            
            # Update dashboard with results
            self._update_dashboard_with_session(session_context, analysis_results)
            
            # Check against baselines
            baseline_comparison = self._compare_against_baselines(analysis_results)
            
            # Generate final report
            final_report = self._generate_final_report(
                session_context, metrics_summary, analysis_results, baseline_comparison
            )
            
            # Clean up session
            del self.active_sessions[session_id]
            
            logger.info(f"Ended refactoring session: {session_id}")
            return final_report
            
        except Exception as e:
            logger.error(f"Error ending refactoring session {session_id}: {e}")
            raise
    
    def _generate_session_analysis(self, session_context: Dict[str, Any], 
                                 metrics_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive analysis of the refactoring session"""
        try:
            analysis = {
                "session_id": session_context["session_id"],
                "operation_name": session_context["operation_name"],
                "target_files": session_context["target_files"],
                "analysis_timestamp": datetime.now().isoformat(),
                "metrics_summary": metrics_summary,
                "code_quality_analysis": {},
                "performance_analysis": {},
                "efficiency_analysis": {},
                "recommendations": []
            }
            
            # Analyze code quality for each target file
            for file_path in session_context["target_files"]:
                if os.path.exists(file_path):
                    quality_metrics = self.metrics_system.measure_code_quality(file_path)
                    analysis["code_quality_analysis"][file_path] = quality_metrics
            
            # Analyze performance metrics
            if "duration" in metrics_summary:
                duration = metrics_summary["duration"]
                analysis["performance_analysis"]["duration"] = {
                    "value": duration,
                    "unit": "seconds",
                    "status": self._get_performance_status("duration", duration)
                }
            
            # Generate efficiency recommendations
            analysis["recommendations"] = self._generate_efficiency_recommendations(analysis)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error generating session analysis: {e}")
            return {"error": str(e)}
    
    def _get_performance_status(self, metric_name: str, value: float) -> str:
        """Get performance status based on thresholds"""
        thresholds = self.integration_config["performance_thresholds"]
        
        if metric_name == "duration" and value > thresholds["critical_duration"]:
            return "critical"
        elif metric_name == "duration" and value > thresholds["critical_duration"] / 2:
            return "warning"
        else:
            return "good"
    
    def _generate_efficiency_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate efficiency recommendations based on analysis"""
        recommendations = []
        
        # Check code quality metrics
        for file_path, quality_metrics in analysis["code_quality_analysis"].items():
            if "complexity" in quality_metrics:
                complexity = quality_metrics["complexity"]
                if complexity > 15:
                    recommendations.append(f"High complexity in {file_path} - consider breaking down functions")
                elif complexity > 10:
                    recommendations.append(f"Moderate complexity in {file_path} - monitor for improvements")
            
            if "maintainability_index" in quality_metrics:
                maintainability = quality_metrics["maintainability_index"]
                if maintainability < 0.5:
                    recommendations.append(f"Low maintainability in {file_path} - focus on code structure")
                elif maintainability < 0.7:
                    recommendations.append(f"Moderate maintainability in {file_path} - consider refactoring")
            
            if "duplication_percentage" in quality_metrics:
                duplication = quality_metrics["duplication_percentage"]
                if duplication > 0.2:
                    recommendations.append(f"High duplication in {file_path} - extract common functionality")
                elif duplication > 0.1:
                    recommendations.append(f"Moderate duplication in {file_path} - identify reusable patterns")
        
        # Check performance metrics
        if "performance_analysis" in analysis:
            perf_analysis = analysis["performance_analysis"]
            if "duration" in perf_analysis and perf_analysis["duration"]["status"] == "critical":
                recommendations.append("Refactoring duration is critical - optimize workflow and tooling")
            elif "duration" in perf_analysis and perf_analysis["duration"]["status"] == "warning":
                recommendations.append("Refactoring duration is high - consider process improvements")
        
        if not recommendations:
            recommendations.append("Good refactoring performance - continue current practices")
        
        return recommendations
    
    def _update_dashboard_with_session(self, session_context: Dict[str, Any], 
                                     analysis_results: Dict[str, Any]):
        """Update dashboard with session results"""
        try:
            # Create performance alerts if needed
            if self.integration_config["alert_integration"]:
                self._create_performance_alerts(analysis_results)
            
            # Update dashboard metrics
            self.dashboard.get_metrics_overview()
            
        except Exception as e:
            logger.error(f"Error updating dashboard: {e}")
    
    def _create_performance_alerts(self, analysis_results: Dict[str, Any]):
        """Create performance alerts based on analysis results"""
        try:
            # Check code quality metrics
            for file_path, quality_metrics in analysis_results.get("code_quality_analysis", {}).items():
                if "complexity" in quality_metrics:
                    complexity = quality_metrics["complexity"]
                    if complexity > self.integration_config["performance_thresholds"]["critical_complexity"]:
                        self.dashboard.create_alert(
                            title="Critical Code Complexity",
                            message=f"Code complexity {complexity} exceeds critical threshold in {file_path}",
                            severity=self.dashboard.AlertSeverity.CRITICAL,
                            metric_name="code_complexity",
                            threshold_value=self.integration_config["performance_thresholds"]["critical_complexity"],
                            current_value=complexity
                        )
                
                if "maintainability_index" in quality_metrics:
                    maintainability = quality_metrics["maintainability_index"]
                    if maintainability < self.integration_config["performance_thresholds"]["critical_maintainability"]:
                        self.dashboard.create_alert(
                            title="Critical Maintainability Issue",
                            message=f"Maintainability index {maintainability} below critical threshold in {file_path}",
                            severity=self.dashboard.AlertSeverity.CRITICAL,
                            metric_name="maintainability_index",
                            threshold_value=self.integration_config["performance_thresholds"]["critical_maintainability"],
                            current_value=maintainability
                        )
            
            # Check performance metrics
            if "performance_analysis" in analysis_results:
                perf_analysis = analysis_results["performance_analysis"]
                if "duration" in perf_analysis and perf_analysis["duration"]["status"] == "critical":
                    duration = perf_analysis["duration"]["value"]
                    self.dashboard.create_alert(
                        title="Critical Refactoring Duration",
                        message=f"Refactoring duration {duration}s exceeds critical threshold",
                        severity=self.dashboard.AlertSeverity.CRITICAL,
                        metric_name="refactoring_duration",
                        threshold_value=self.integration_config["performance_thresholds"]["critical_duration"],
                        current_value=duration
                    )
                    
        except Exception as e:
            logger.error(f"Error creating performance alerts: {e}")
    
    def _compare_against_baselines(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Compare session results against all active baselines"""
        try:
            baseline_comparisons = {}
            active_baselines = self.baseline_system.get_active_baselines()
            
            # Extract current metrics for comparison
            current_metrics = {}
            
            # Aggregate code quality metrics
            for file_path, quality_metrics in analysis_results.get("code_quality_analysis", {}).items():
                for metric_name, metric_value in quality_metrics.items():
                    if isinstance(metric_value, (int, float)):
                        if metric_name not in current_metrics:
                            current_metrics[metric_name] = []
                        current_metrics[metric_name].append(metric_value)
            
            # Calculate averages for comparison
            averaged_metrics = {}
            for metric_name, values in current_metrics.items():
                if values:
                    averaged_metrics[metric_name] = sum(values) / len(values)
            
            # Compare against each baseline
            for baseline in active_baselines:
                comparison = self.baseline_system.compare_against_baseline(
                    baseline.baseline_id, averaged_metrics
                )
                if comparison:
                    baseline_comparisons[baseline.baseline_id] = {
                        "baseline_name": baseline.name,
                        "baseline_type": baseline.baseline_type.value,
                        "comparison": comparison
                    }
            
            return baseline_comparisons
            
        except Exception as e:
            logger.error(f"Error comparing against baselines: {e}")
            return {"error": str(e)}
    
    def _generate_final_report(self, session_context: Dict[str, Any], 
                              metrics_summary: Dict[str, Any],
                              analysis_results: Dict[str, Any],
                              baseline_comparison: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive final report for the refactoring session"""
        try:
            final_report = {
                "report_id": f"refactoring_report_{int(time.time())}",
                "session_id": session_context["session_id"],
                "operation_name": session_context["operation_name"],
                "target_files": session_context["target_files"],
                "description": session_context.get("description", ""),
                "timestamp": datetime.now().isoformat(),
                "session_duration": metrics_summary.get("duration", 0),
                "executive_summary": {
                    "status": "completed",
                    "overall_score": self._calculate_overall_score(analysis_results, baseline_comparison),
                    "key_findings": self._extract_key_findings(analysis_results, baseline_comparison),
                    "recommendations": analysis_results.get("recommendations", [])
                },
                "detailed_analysis": analysis_results,
                "baseline_comparison": baseline_comparison,
                "performance_metrics": {
                    "code_quality_score": self._calculate_code_quality_score(analysis_results),
                    "efficiency_score": self._calculate_efficiency_score(analysis_results),
                    "improvement_potential": self._calculate_improvement_potential(baseline_comparison)
                },
                "export_data": {
                    "metrics_export": self.metrics_system.export_metrics_data,
                    "dashboard_export": self.dashboard.export_dashboard_data,
                    "baseline_export": self.baseline_system.export_baseline_data
                }
            }
            
            return final_report
            
        except Exception as e:
            logger.error(f"Error generating final report: {e}")
            return {"error": str(e)}
    
    def _calculate_overall_score(self, analysis_results: Dict[str, Any], 
                                baseline_comparison: Dict[str, Any]) -> float:
        """Calculate overall performance score for the refactoring session"""
        try:
            scores = []
            
            # Code quality score
            code_quality_score = self._calculate_code_quality_score(analysis_results)
            scores.append(code_quality_score * 0.4)  # 40% weight
            
            # Efficiency score
            efficiency_score = self._calculate_efficiency_score(analysis_results)
            scores.append(efficiency_score * 0.3)  # 30% weight
            
            # Baseline comparison score
            baseline_score = self._calculate_baseline_score(baseline_comparison)
            scores.append(baseline_score * 0.3)  # 30% weight
            
            return sum(scores) if scores else 0.0
            
        except Exception as e:
            logger.error(f"Error calculating overall score: {e}")
            return 0.0
    
    def _calculate_code_quality_score(self, analysis_results: Dict[str, Any]) -> float:
        """Calculate code quality score from analysis results"""
        try:
            quality_scores = []
            
            for file_path, quality_metrics in analysis_results.get("code_quality_analysis", {}).items():
                file_score = 0.0
                metric_count = 0
                
                if "complexity" in quality_metrics:
                    complexity = quality_metrics["complexity"]
                    if complexity <= 5:
                        file_score += 1.0
                    elif complexity <= 10:
                        file_score += 0.8
                    elif complexity <= 15:
                        file_score += 0.6
                    else:
                        file_score += 0.3
                    metric_count += 1
                
                if "maintainability_index" in quality_metrics:
                    maintainability = quality_metrics["maintainability_index"]
                    file_score += maintainability
                    metric_count += 1
                
                if "duplication_percentage" in quality_metrics:
                    duplication = quality_metrics["duplication_percentage"]
                    if duplication <= 0.05:
                        file_score += 1.0
                    elif duplication <= 0.1:
                        file_score += 0.8
                    elif duplication <= 0.2:
                        file_score += 0.6
                    else:
                        file_score += 0.3
                    metric_count += 1
                
                if metric_count > 0:
                    quality_scores.append(file_score / metric_count)
            
            return sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
            
        except Exception as e:
            logger.error(f"Error calculating code quality score: {e}")
            return 0.0
    
    def _calculate_efficiency_score(self, analysis_results: Dict[str, Any]) -> float:
        """Calculate efficiency score from analysis results"""
        try:
            if "performance_analysis" in analysis_results:
                perf_analysis = analysis_results["performance_analysis"]
                if "duration" in perf_analysis:
                    duration = perf_analysis["duration"]["value"]
                    if duration <= 60:  # 1 minute
                        return 1.0
                    elif duration <= 300:  # 5 minutes
                        return 0.8
                    elif duration <= 600:  # 10 minutes
                        return 0.6
                    else:
                        return 0.3
            
            return 0.7  # Default score
            
        except Exception as e:
            logger.error(f"Error calculating efficiency score: {e}")
            return 0.0
    
    def _calculate_baseline_score(self, baseline_comparison: Dict[str, Any]) -> float:
        """Calculate baseline comparison score"""
        try:
            if not baseline_comparison:
                return 0.7  # Default score if no baselines
            
            scores = []
            for baseline_id, comparison_data in baseline_comparison.items():
                if "comparison" in comparison_data:
                    comparison = comparison_data["comparison"]
                    if hasattr(comparison, 'overall_score'):
                        scores.append(comparison.overall_score)
            
            return sum(scores) / len(scores) if scores else 0.7
            
        except Exception as e:
            logger.error(f"Error calculating baseline score: {e}")
            return 0.7
    
    def _calculate_improvement_potential(self, baseline_comparison: Dict[str, Any]) -> float:
        """Calculate improvement potential based on baseline comparison"""
        try:
            if not baseline_comparison:
                return 0.0
            
            total_potential = 0.0
            baseline_count = 0
            
            for baseline_id, comparison_data in baseline_comparison.items():
                if "comparison" in comparison_data:
                    comparison = comparison_data["comparison"]
                    if hasattr(comparison, 'overall_score'):
                        current_score = comparison.overall_score
                        improvement_potential = max(0.0, 1.0 - current_score)
                        total_potential += improvement_potential
                        baseline_count += 1
            
            return total_potential / baseline_count if baseline_count > 0 else 0.0
            
        except Exception as e:
            logger.error(f"Error calculating improvement potential: {e}")
            return 0.0
    
    def _extract_key_findings(self, analysis_results: Dict[str, Any], 
                             baseline_comparison: Dict[str, Any]) -> List[str]:
        """Extract key findings from analysis and baseline comparison"""
        findings = []
        
        try:
            # Code quality findings
            for file_path, quality_metrics in analysis_results.get("code_quality_analysis", {}).items():
                if "complexity" in quality_metrics and quality_metrics["complexity"] > 10:
                    findings.append(f"High complexity detected in {file_path}")
                
                if "maintainability_index" in quality_metrics and quality_metrics["maintainability_index"] < 0.6:
                    findings.append(f"Low maintainability in {file_path}")
            
            # Performance findings
            if "performance_analysis" in analysis_results:
                perf_analysis = analysis_results["performance_analysis"]
                if "duration" in perf_analysis and perf_analysis["duration"]["status"] != "good":
                    findings.append(f"Performance issue: {perf_analysis['duration']['status']} refactoring duration")
            
            # Baseline comparison findings
            for baseline_id, comparison_data in baseline_comparison.items():
                if "comparison" in comparison_data:
                    comparison = comparison_data["comparison"]
                    if hasattr(comparison, 'improvements') and comparison.improvements:
                        findings.append(f"Improvements against {comparison_data['baseline_name']}: {len(comparison.improvements)}")
                    
                    if hasattr(comparison, 'regressions') and comparison.regressions:
                        findings.append(f"Regressions against {comparison_data['baseline_name']}: {len(comparison.regressions)}")
            
            return findings if findings else ["No significant issues detected"]
            
        except Exception as e:
            logger.error(f"Error extracting key findings: {e}")
            return ["Error analyzing findings"]
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            "integration_status": "active",
            "active_sessions": len(self.active_sessions),
            "metrics_system": self.metrics_system.get_system_health(),
            "dashboard_status": self.dashboard.get_dashboard_status(),
            "baseline_system": self.baseline_system.get_system_status(),
            "configuration": {
                "auto_monitoring": self.integration_config["auto_monitoring_enabled"],
                "alert_integration": self.integration_config["alert_integration"],
                "reporting_enabled": self.integration_config["reporting_enabled"]
            }
        }
    
    def export_comprehensive_report(self, output_path: str, format: str = "json") -> bool:
        """Export comprehensive system report"""
        try:
            if format.lower() == "json":
                export_data = {
                    "export_timestamp": datetime.now().isoformat(),
                    "system_status": self.get_system_status(),
                    "integration_config": self.integration_config,
                    "active_sessions": list(self.active_sessions.keys())
                }
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, default=str)
                
                logger.info(f"Exported comprehensive report to {output_path}")
                return True
                
            else:
                logger.error(f"Unsupported export format: {format}")
                return False
                
        except Exception as e:
            logger.error(f"Error exporting comprehensive report: {e}")
            return False

async def demo_refactoring_metrics_integration():
    """Demonstrate the integrated refactoring metrics system"""
    print("🚀 Refactoring Performance Metrics Integration Demo")
    print("=" * 50)
    
    # Initialize the integrated system
    integration = RefactoringMetricsIntegration()
    
    # Get system status
    status = integration.get_system_status()
    print(f"Integration Status: {status['integration_status']}")
    print(f"Active Sessions: {status['active_sessions']}")
    
    # Start a refactoring session
    session_id = integration.start_refactoring_session(
        "code_quality_improvement",
        ["src/core/refactoring/refactoring_performance_metrics.py"],
        "Improving code quality metrics for refactoring performance system"
    )
    print(f"Started Session: {session_id}")
    
    # Simulate some work
    await asyncio.sleep(2)
    
    # End the session and get comprehensive report
    final_report = integration.end_refactoring_session(session_id)
    
    print(f"Session Report ID: {final_report['report_id']}")
    print(f"Overall Score: {final_report['executive_summary']['overall_score']:.2f}")
    print(f"Key Findings: {len(final_report['executive_summary']['key_findings'])}")
    print(f"Recommendations: {len(final_report['executive_summary']['recommendations'])}")
    
    # Export comprehensive report
    export_success = integration.export_comprehensive_report(
        "refactoring_metrics_integration_report.json"
    )
    print(f"Report Export: {'Success' if export_success else 'Failed'}")
    
    print("\n✅ Integration Demo completed successfully!")

if __name__ == "__main__":
    asyncio.run(demo_refactoring_metrics_integration())
