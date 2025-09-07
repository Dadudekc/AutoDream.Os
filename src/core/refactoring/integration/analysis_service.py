#!/usr/bin/env python3
"""
Analysis Service - Agent-5
=========================

Service for analyzing refactoring sessions and generating reports.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from .models import (SessionAnalysis, PerformanceAnalysis, BaselineComparison,
                    ExecutiveSummary, PerformanceMetrics, FinalReport, PerformanceStatus)


class AnalysisService:
    """
    Service for analyzing refactoring sessions and generating reports
    
    Provides:
    - Session analysis generation
    - Performance analysis
    - Baseline comparison
    - Report generation
    - Score calculations
    """
    
    def __init__(self, performance_thresholds: Dict[str, float]):
        self.performance_thresholds = performance_thresholds
        self.logger = logging.getLogger(__name__)
        self.logger.info("Analysis Service initialized")
    
    def generate_session_analysis(self, session_context: Any, 
                                metrics_summary: Dict[str, Any]) -> SessionAnalysis:
        """Generate comprehensive analysis of the refactoring session"""
        try:
            analysis = SessionAnalysis(
                session_id=session_context.session_id,
                operation_name=session_context.operation_name,
                target_files=session_context.target_files,
                analysis_timestamp=datetime.now(),
                metrics_summary=metrics_summary,
                code_quality_analysis={},
                performance_analysis={},
                efficiency_analysis={},
                recommendations=[]
            )
            
            # Analyze code quality for each target file
            if hasattr(session_context, 'metrics_system') and session_context.metrics_system:
                for file_path in session_context.target_files:
                    try:
                        quality_metrics = session_context.metrics_system.measure_code_quality(file_path)
                        analysis.code_quality_analysis[file_path] = quality_metrics
                    except Exception as e:
                        self.logger.warning(f"Could not analyze {file_path}: {e}")
                        continue
            
            # Analyze performance metrics
            if "duration" in metrics_summary:
                duration = metrics_summary["duration"]
                analysis.performance_analysis["duration"] = {
                    "value": duration,
                    "unit": "seconds",
                    "status": self._get_performance_status("duration", duration)
                }
            
            # Generate efficiency recommendations
            analysis.recommendations = self._generate_efficiency_recommendations(analysis)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error generating session analysis: {e}")
            return SessionAnalysis(
                session_id="error",
                operation_name="error",
                target_files=[],
                analysis_timestamp=datetime.now(),
                metrics_summary={},
                code_quality_analysis={},
                performance_analysis={},
                efficiency_analysis={},
                recommendations=[f"Error in analysis: {str(e)}"]
            )
    
    def _get_performance_status(self, metric_name: str, value: float) -> str:
        """Get performance status based on thresholds"""
        if metric_name == "duration" and value > self.performance_thresholds["critical_duration"]:
            return PerformanceStatus.CRITICAL.value
        elif metric_name == "duration" and value > self.performance_thresholds["critical_duration"] / 2:
            return PerformanceStatus.WARNING.value
        else:
            return PerformanceStatus.GOOD.value
    
    def _generate_efficiency_recommendations(self, analysis: SessionAnalysis) -> List[str]:
        """Generate efficiency recommendations based on analysis"""
        recommendations = []
        
        # Check code quality metrics
        for file_path, quality_metrics in analysis.code_quality_analysis.items():
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
        if "duration" in analysis.performance_analysis:
            perf_analysis = analysis.performance_analysis["duration"]
            if perf_analysis["status"] == PerformanceStatus.CRITICAL.value:
                recommendations.append("Refactoring duration is critical - optimize workflow and tooling")
            elif perf_analysis["status"] == PerformanceStatus.WARNING.value:
                recommendations.append("Refactoring duration is high - consider process improvements")
        
        if not recommendations:
            recommendations.append("Good refactoring performance - continue current practices")
        
        return recommendations
    
    def compare_against_baselines(self, analysis_results: SessionAnalysis, 
                                baseline_system: Any) -> Dict[str, BaselineComparison]:
        """Compare session results against all active baselines"""
        try:
            baseline_comparisons = {}
            
            if not baseline_system:
                return baseline_comparisons
            
            # Get active baselines
            try:
                active_baselines = baseline_system.get_active_baselines()
            except Exception as e:
                self.logger.warning(f"Could not get active baselines: {e}")
                return baseline_comparisons
            
            # Extract current metrics for comparison
            current_metrics = {}
            
            # Aggregate code quality metrics
            for file_path, quality_metrics in analysis_results.code_quality_analysis.items():
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
                try:
                    comparison = baseline_system.compare_against_baseline(
                        baseline.baseline_id, averaged_metrics
                    )
                    if comparison:
                        baseline_comparisons[baseline.baseline_id] = BaselineComparison(
                            baseline_id=baseline.baseline_id,
                            baseline_name=baseline.name,
                            baseline_type=baseline.baseline_type.value if hasattr(baseline, 'baseline_type') else "unknown",
                            comparison=comparison
                        )
                except Exception as e:
                    self.logger.warning(f"Could not compare against baseline {baseline.baseline_id}: {e}")
                    continue
            
            return baseline_comparisons
            
        except Exception as e:
            self.logger.error(f"Error comparing against baselines: {e}")
            return {}
    
    def generate_final_report(self, session_context: Any, 
                            metrics_summary: Dict[str, Any],
                            analysis_results: SessionAnalysis,
                            baseline_comparison: Dict[str, BaselineComparison]) -> FinalReport:
        """Generate comprehensive final report for the refactoring session"""
        try:
            # Calculate scores
            overall_score = self._calculate_overall_score(analysis_results, baseline_comparison)
            code_quality_score = self._calculate_code_quality_score(analysis_results)
            efficiency_score = self._calculate_efficiency_score(analysis_results)
            improvement_potential = self._calculate_improvement_potential(baseline_comparison)
            
            # Create executive summary
            executive_summary = ExecutiveSummary(
                status="completed",
                overall_score=overall_score,
                key_findings=self._extract_key_findings(analysis_results, baseline_comparison),
                recommendations=analysis_results.recommendations
            )
            
            # Create performance metrics
            performance_metrics = PerformanceMetrics(
                code_quality_score=code_quality_score,
                efficiency_score=efficiency_score,
                improvement_potential=improvement_potential
            )
            
            # Create export data (placeholder)
            export_data = {
                "metrics_export": None,
                "dashboard_export": None,
                "baseline_export": None
            }
            
            final_report = FinalReport(
                report_id=f"refactoring_report_{int(time.time())}",
                session_id=session_context.session_id,
                operation_name=session_context.operation_name,
                target_files=session_context.target_files,
                description=getattr(session_context, 'description', ''),
                timestamp=datetime.now(),
                session_duration=metrics_summary.get("duration", 0),
                executive_summary=executive_summary,
                detailed_analysis=analysis_results,
                baseline_comparison=baseline_comparison,
                performance_metrics=performance_metrics,
                export_data=export_data
            )
            
            return final_report
            
        except Exception as e:
            self.logger.error(f"Error generating final report: {e}")
            # Return a minimal error report
            return FinalReport(
                report_id=f"error_report_{int(time.time())}",
                session_id="error",
                operation_name="error",
                target_files=[],
                description="Error generating report",
                timestamp=datetime.now(),
                session_duration=0,
                executive_summary=ExecutiveSummary(
                    status="error",
                    overall_score=0.0,
                    key_findings=[f"Error: {str(e)}"],
                    recommendations=["Fix the error and retry"]
                ),
                detailed_analysis=analysis_results,
                baseline_comparison={},
                performance_metrics=PerformanceMetrics(
                    code_quality_score=0.0,
                    efficiency_score=0.0,
                    improvement_potential=0.0
                ),
                export_data={}
            )
    
    def _calculate_overall_score(self, analysis_results: SessionAnalysis, 
                                baseline_comparison: Dict[str, BaselineComparison]) -> float:
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
            self.logger.error(f"Error calculating overall score: {e}")
            return 0.0
    
    def _calculate_code_quality_score(self, analysis_results: SessionAnalysis) -> float:
        """Calculate code quality score from analysis results"""
        try:
            quality_scores = []
            
            for file_path, quality_metrics in analysis_results.code_quality_analysis.items():
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
            self.logger.error(f"Error calculating code quality score: {e}")
            return 0.0
    
    def _calculate_efficiency_score(self, analysis_results: SessionAnalysis) -> float:
        """Calculate efficiency score from analysis results"""
        try:
            if "duration" in analysis_results.performance_analysis:
                perf_analysis = analysis_results.performance_analysis["duration"]
                if "value" in perf_analysis:
                    duration = perf_analysis["value"]
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
            self.logger.error(f"Error calculating efficiency score: {e}")
            return 0.0
    
    def _calculate_baseline_score(self, baseline_comparison: Dict[str, BaselineComparison]) -> float:
        """Calculate baseline comparison score"""
        try:
            if not baseline_comparison:
                return 0.7  # Default score if no baselines
            
            scores = []
            for baseline_id, comparison_data in baseline_comparison.items():
                if hasattr(comparison_data, 'comparison') and comparison_data.comparison:
                    comparison = comparison_data.comparison
                    if hasattr(comparison, 'overall_score'):
                        scores.append(comparison.overall_score)
            
            return sum(scores) / len(scores) if scores else 0.7
            
        except Exception as e:
            self.logger.error(f"Error calculating baseline score: {e}")
            return 0.7
    
    def _calculate_improvement_potential(self, baseline_comparison: Dict[str, BaselineComparison]) -> float:
        """Calculate improvement potential based on baseline comparison"""
        try:
            if not baseline_comparison:
                return 0.0
            
            total_potential = 0.0
            baseline_count = 0
            
            for baseline_id, comparison_data in baseline_comparison.items():
                if hasattr(comparison_data, 'comparison') and comparison_data.comparison:
                    comparison = comparison_data.comparison
                    if hasattr(comparison, 'overall_score'):
                        current_score = comparison.overall_score
                        improvement_potential = max(0.0, 1.0 - current_score)
                        total_potential += improvement_potential
                        baseline_count += 1
            
            return total_potential / baseline_count if baseline_count > 0 else 0.0
            
        except Exception as e:
            self.logger.error(f"Error calculating improvement potential: {e}")
            return 0.0
    
    def _extract_key_findings(self, analysis_results: SessionAnalysis, 
                             baseline_comparison: Dict[str, BaselineComparison]) -> List[str]:
        """Extract key findings from analysis and baseline comparison"""
        findings = []
        
        try:
            # Code quality findings
            for file_path, quality_metrics in analysis_results.code_quality_analysis.items():
                if "complexity" in quality_metrics and quality_metrics["complexity"] > 10:
                    findings.append(f"High complexity detected in {file_path}")
                
                if "maintainability_index" in quality_metrics and quality_metrics["maintainability_index"] < 0.6:
                    findings.append(f"Low maintainability in {file_path}")
            
            # Performance findings
            if "duration" in analysis_results.performance_analysis:
                perf_analysis = analysis_results.performance_analysis["duration"]
                if "status" in perf_analysis and perf_analysis["status"] != PerformanceStatus.GOOD.value:
                    findings.append(f"Performance issue: {perf_analysis['status']} refactoring duration")
            
            # Baseline comparison findings
            for baseline_id, comparison_data in baseline_comparison.items():
                if hasattr(comparison_data, 'comparison') and comparison_data.comparison:
                    comparison = comparison_data.comparison
                    if hasattr(comparison, 'improvements') and comparison.improvements:
                        findings.append(f"Improvements against {comparison_data.baseline_name}: {len(comparison.improvements)}")
                    
                    if hasattr(comparison, 'regressions') and comparison.regressions:
                        findings.append(f"Regressions against {comparison_data.baseline_name}: {len(comparison.regressions)}")
            
            return findings if findings else ["No significant issues detected"]
            
        except Exception as e:
            self.logger.error(f"Error extracting key findings: {e}")
            return ["Error analyzing findings"]
