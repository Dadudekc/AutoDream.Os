"""
Performance Results Processor - Phase-2 V2 Compliance Refactoring
==================================================================

Handles performance-specific result processing.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from __future__ import annotations
from typing import Dict, Any
from .base_results_manager import BaseResultsManager


class PerformanceResultsProcessor(BaseResultsManager):
    """Processes performance-specific results."""

    def _process_result_by_type(
        self, context, result_type: str, result_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process performance results."""
        if result_type == "performance":
            return self._process_performance_result(context, result_data)
        return super()._process_result_by_type(context, result_type, result_data)

    def _process_performance_result(
        self, context, result_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process performance result data."""
        try:
            performance_metrics = result_data.get("metrics", {})
            test_name = result_data.get("test_name", "unknown")
            duration = result_data.get("duration", 0)
            
            # Calculate performance score
            performance_score = self._calculate_performance_score(performance_metrics)
            
            # Analyze performance trends
            performance_analysis = self._analyze_performance_trends(performance_metrics)
            
            return {
                "performance_success": True,
                "test_name": test_name,
                "duration": duration,
                "performance_score": performance_score,
                "performance_analysis": performance_analysis,
                "metrics_processed": len(performance_metrics),
                "original_data": result_data,
            }
            
        except Exception as e:
            context.logger(f"Error processing performance result: {e}")
            return {
                "performance_success": False,
                "error": str(e),
                "original_data": result_data,
            }

    def _calculate_performance_score(self, metrics: Dict[str, Any]) -> float:
        """Calculate overall performance score."""
        try:
            # Base score
            score = 100.0
            
            # CPU usage penalty
            cpu_usage = metrics.get("cpu_usage", 0)
            if cpu_usage > 80:
                score -= (cpu_usage - 80) * 0.5
            
            # Memory usage penalty
            memory_usage = metrics.get("memory_usage", 0)
            if memory_usage > 80:
                score -= (memory_usage - 80) * 0.3
            
            # Response time penalty
            response_time = metrics.get("response_time", 0)
            if response_time > 1000:  # 1 second
                score -= (response_time - 1000) / 100
            
            # Throughput bonus
            throughput = metrics.get("throughput", 0)
            if throughput > 100:
                score += min(throughput - 100, 20) * 0.1
            
            return max(0.0, min(100.0, score))
            
        except Exception:
            return 50.0  # Default score on error

    def _analyze_performance_trends(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance trends."""
        try:
            analysis = {
                "cpu_trend": "stable",
                "memory_trend": "stable", 
                "response_time_trend": "stable",
                "overall_trend": "stable",
            }
            
            # Simple trend analysis based on current values
            cpu_usage = metrics.get("cpu_usage", 0)
            memory_usage = metrics.get("memory_usage", 0)
            response_time = metrics.get("response_time", 0)
            
            if cpu_usage > 70:
                analysis["cpu_trend"] = "high"
            elif cpu_usage < 30:
                analysis["cpu_trend"] = "low"
            
            if memory_usage > 70:
                analysis["memory_trend"] = "high"
            elif memory_usage < 30:
                analysis["memory_trend"] = "low"
            
            if response_time > 500:
                analysis["response_time_trend"] = "slow"
            elif response_time < 100:
                analysis["response_time_trend"] = "fast"
            
            # Overall trend
            high_metrics = sum(1 for trend in analysis.values() if trend == "high")
            if high_metrics >= 2:
                analysis["overall_trend"] = "degrading"
            elif all(trend in ["low", "fast"] for trend in analysis.values() if trend != "stable"):
                analysis["overall_trend"] = "improving"
            
            return analysis
            
        except Exception:
            return {"overall_trend": "unknown"}
