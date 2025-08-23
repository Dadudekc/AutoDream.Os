#!/usr/bin/env python3
"""
Report Generator - V2 Core Performance System

This module handles performance report generation and recommendations.
Follows V2 coding standards: ≤200 LOC, OOP design, SRP
"""

import uuid
from datetime import datetime
from typing import List, Dict, Any
from .performance_types import (
    SystemPerformanceReport, PerformanceBenchmark, 
    OptimizationTarget, PerformanceLevel
)


class ReportGenerator:
    """Handles performance report generation and recommendations"""
    
    def __init__(self):
        self.logger = None  # Will be set by parent class
    
    def generate_performance_report(
        self,
        benchmarks: List[PerformanceBenchmark],
        overall_level: PerformanceLevel,
        enterprise_score: float,
        optimization_opportunities: List[OptimizationTarget]
    ) -> SystemPerformanceReport:
        """Generate comprehensive performance report"""
        try:
            report_id = str(uuid.uuid4())
            timestamp = datetime.now().isoformat()
            
            # Generate recommendations
            recommendations = self._generate_performance_recommendations(
                benchmarks, overall_level, enterprise_score
            )
            
            return SystemPerformanceReport(
                report_id=report_id,
                timestamp=timestamp,
                overall_performance_level=overall_level,
                benchmark_results=benchmarks,
                optimization_opportunities=optimization_opportunities,
                enterprise_readiness_score=enterprise_score,
                recommendations=recommendations
            )
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to generate performance report: {e}")
            raise
    
    def _generate_performance_recommendations(
        self,
        benchmarks: List[PerformanceBenchmark],
        overall_level: PerformanceLevel,
        enterprise_score: float
    ) -> List[str]:
        """Generate performance improvement recommendations"""
        recommendations = []
        
        # Overall system recommendations
        if overall_level == PerformanceLevel.NOT_READY:
            recommendations.append("System requires significant performance improvements before production use")
        elif overall_level == PerformanceLevel.DEVELOPMENT_READY:
            recommendations.append("System ready for development but needs optimization for production")
        elif overall_level == PerformanceLevel.PRODUCTION_READY:
            recommendations.append("System ready for production with minor optimizations recommended")
        elif overall_level == PerformanceLevel.ENTERPRISE_READY:
            recommendations.append("System meets enterprise performance standards")
        
        # Enterprise readiness recommendations
        if enterprise_score < 0.7:
            recommendations.append("Focus on core performance metrics to improve enterprise readiness")
        elif enterprise_score < 0.85:
            recommendations.append("Optimize remaining performance bottlenecks for full enterprise readiness")
        elif enterprise_score < 0.95:
            recommendations.append("Minor optimizations needed for optimal enterprise performance")
        
        # Benchmark-specific recommendations
        for benchmark in benchmarks:
            if benchmark.performance_level == PerformanceLevel.NOT_READY:
                if benchmark.benchmark_type.value == "response_time":
                    recommendations.append("Optimize response time to meet <100ms target")
                elif benchmark.benchmark_type.value == "throughput":
                    recommendations.append("Increase throughput to meet 1000 ops/sec target")
                elif benchmark.benchmark_type.value == "scalability":
                    recommendations.append("Improve scalability to support 100+ concurrent users")
                elif benchmark.benchmark_type.value == "reliability":
                    recommendations.append("Enhance reliability to achieve 99.9% uptime")
                elif benchmark.benchmark_type.value == "latency":
                    recommendations.append("Reduce latency to meet <50ms target")
        
        # Remove duplicates while preserving order
        unique_recommendations = []
        for rec in recommendations:
            if rec not in unique_recommendations:
                unique_recommendations.append(rec)
        
        return unique_recommendations
    
    def generate_benchmark_summary(self, benchmarks: List[PerformanceBenchmark]) -> Dict[str, Any]:
        """Generate summary statistics for benchmarks"""
        if not benchmarks:
            return {"error": "No benchmarks available"}
        
        try:
            summary = {
                "total_benchmarks": len(benchmarks),
                "successful_benchmarks": 0,
                "failed_benchmarks": 0,
                "performance_levels": {},
                "benchmark_types": {},
                "total_duration": 0.0,
                "average_duration": 0.0
            }
            
            # Count performance levels and types
            for benchmark in benchmarks:
                # Performance level counts
                level = benchmark.performance_level.value
                summary["performance_levels"][level] = summary["performance_levels"].get(level, 0) + 1
                
                # Benchmark type counts
                btype = benchmark.benchmark_type.value
                summary["benchmark_types"][btype] = summary["benchmark_types"].get(btype, 0) + 1
                
                # Duration statistics
                if "error" not in benchmark.metrics:
                    summary["successful_benchmarks"] += 1
                    summary["total_duration"] += benchmark.duration
                else:
                    summary["failed_benchmarks"] += 1
            
            # Calculate averages
            if summary["successful_benchmarks"] > 0:
                summary["average_duration"] = summary["total_duration"] / summary["successful_benchmarks"]
            
            return summary
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to generate benchmark summary: {e}")
            return {"error": f"Failed to generate summary: {e}"}
    
    def format_report_for_display(self, report: SystemPerformanceReport) -> str:
        """Format performance report for human-readable display"""
        try:
            lines = []
            lines.append("=" * 60)
            lines.append("PERFORMANCE VALIDATION REPORT")
            lines.append("=" * 60)
            lines.append(f"Report ID: {report.report_id}")
            lines.append(f"Timestamp: {report.timestamp}")
            lines.append(f"Overall Performance: {report.overall_performance_level.value.upper()}")
            lines.append(f"Enterprise Readiness: {report.enterprise_readiness_score:.1%}")
            lines.append("")
            
            # Benchmark results
            lines.append("BENCHMARK RESULTS:")
            lines.append("-" * 30)
            for benchmark in report.benchmark_results:
                lines.append(f"• {benchmark.benchmark_type.value.title()}: {benchmark.performance_level.value}")
                if "error" not in benchmark.metrics:
                    for key, value in benchmark.metrics.items():
                        lines.append(f"  - {key}: {value}")
                else:
                    lines.append(f"  - Error: {benchmark.metrics['error']}")
            lines.append("")
            
            # Optimization opportunities
            if report.optimization_opportunities:
                lines.append("OPTIMIZATION OPPORTUNITIES:")
                lines.append("-" * 30)
                for opp in report.optimization_opportunities:
                    lines.append(f"• {opp.value.replace('_', ' ').title()}")
                lines.append("")
            
            # Recommendations
            if report.recommendations:
                lines.append("RECOMMENDATIONS:")
                lines.append("-" * 30)
                for rec in report.recommendations:
                    lines.append(f"• {rec}")
                lines.append("")
            
            lines.append("=" * 60)
            return "\n".join(lines)
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to format report: {e}")
            return f"Error formatting report: {e}"

