#!/usr/bin/env python3
"""
Protocol Reporter - V2 Compliance Module
======================================

Focused module for generating protocol execution reports.

V2 Compliance: < 400 lines, single responsibility, modular design.

Author: Agent-5 (Data Organization Specialist)
Test Type: Protocol Reporting
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class ProtocolReporter:
    """Generates reports for protocol execution results."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.reports_dir = project_root / "runtime" / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def generate_detailed_report(self, results: dict[str, Any]) -> dict[str, Any]:
        """Generate detailed protocol execution report."""
        report = {
            "report_type": "protocol_execution",
            "timestamp": datetime.now().isoformat(),
            "execution_summary": self._generate_execution_summary(results),
            "layer_analysis": self._analyze_layers(results),
            "benchmark_analysis": self._analyze_benchmark(results),
            "recommendations": self._generate_recommendations(results),
            "raw_results": results,
        }

        return report

    def _generate_execution_summary(self, results: dict[str, Any]) -> dict[str, Any]:
        """Generate execution summary."""
        return {
            "status": results.get("coordination_status", "UNKNOWN"),
            "overall_score": results.get("overall_score", 0.0),
            "execution_time": results.get("timestamp", 0.0),
            "has_errors": bool(results.get("error")),
            "error_message": results.get("error", ""),
        }

    def _analyze_layers(self, results: dict[str, Any]) -> dict[str, Any]:
        """Analyze individual layer performance."""
        layer_1 = results.get("layer_1_structural", {})
        layer_2 = results.get("layer_2_functional", {})
        layer_3 = results.get("layer_3_performance", {})

        return {
            "structural_layer": {
                "score": layer_1.get("score", 0.0),
                "files_validated": layer_1.get("files_validated", 0),
                "directories_validated": layer_1.get("directories_validated", 0),
                "errors": layer_1.get("errors", []),
            },
            "functional_layer": {
                "score": layer_2.get("score", 0.0),
                "api_endpoints_validated": layer_2.get("api_endpoints_validated", 0),
                "ui_components_validated": layer_2.get("ui_components_validated", 0),
                "errors": layer_2.get("errors", []),
            },
            "performance_layer": {
                "score": layer_3.get("score", 0.0),
                "load_time_ms": layer_3.get("load_time_ms", 0),
                "memory_usage_mb": layer_3.get("memory_usage_mb", 0),
                "errors": layer_3.get("errors", []),
            },
        }

    def _analyze_benchmark(self, results: dict[str, Any]) -> dict[str, Any]:
        """Analyze benchmark comparison."""
        benchmark = results.get("benchmark_comparison", {})

        return {
            "current_performance": benchmark.get("current_score", 0.0),
            "benchmark_target": benchmark.get("agent_2_benchmark", 0.0),
            "domination_target": benchmark.get("domination_target", 0.0),
            "performance_gap": benchmark.get("gap_to_benchmark", 0.0),
            "domination_gap": benchmark.get("gap_to_domination", 0.0),
            "benchmark_exceeded": benchmark.get("exceeds_benchmark", False),
            "domination_achieved": benchmark.get("achieves_domination", False),
        }

    def _generate_recommendations(self, results: dict[str, Any]) -> list[dict[str, Any]]:
        """Generate improvement recommendations."""
        recommendations = []

        overall_score = results.get("overall_score", 0.0)
        benchmark = results.get("benchmark_comparison", {})

        if overall_score < 80.0:
            recommendations.append(
                {
                    "priority": "high",
                    "category": "overall_performance",
                    "description": "Overall score below 80% - comprehensive improvement needed",
                    "actions": [
                        "Review all layer implementations",
                        "Address structural issues first",
                        "Optimize functional components",
                        "Improve performance metrics",
                    ],
                }
            )

        if not benchmark.get("exceeds_benchmark", False):
            recommendations.append(
                {
                    "priority": "medium",
                    "category": "benchmark_improvement",
                    "description": "Performance below Agent-2 benchmark",
                    "actions": [
                        "Focus on highest-impact optimizations",
                        "Review layer-specific improvements",
                        "Consider architectural changes",
                    ],
                }
            )

        # Layer-specific recommendations
        layer_1 = results.get("layer_1_structural", {})
        if layer_1.get("score", 0.0) < 70.0:
            recommendations.append(
                {
                    "priority": "high",
                    "category": "structural_layer",
                    "description": "Structural layer needs improvement",
                    "actions": [
                        "Validate file structure",
                        "Check import dependencies",
                        "Ensure proper directory organization",
                    ],
                }
            )

        return recommendations

    def save_report(self, report: dict[str, Any], filename: str = None) -> Path:
        """Save detailed report to file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"protocol_report_{timestamp}.json"

        report_path = self.reports_dir / filename

        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        return report_path

    def print_detailed_summary(self, report: dict[str, Any]) -> None:
        """Print detailed report summary."""
        print("\n" + "=" * 70)
        print("📋 DETAILED PROTOCOL EXECUTION REPORT")
        print("=" * 70)

        summary = report.get("execution_summary", {})
        print(f"Status: {summary.get('status', 'UNKNOWN')}")
        print(f"Overall Score: {summary.get('overall_score', 0.0):.1f}%")
        print(f"Execution Time: {summary.get('execution_time', 0.0)}")

        if summary.get("has_errors"):
            print(f"⚠️  Errors: {summary.get('error_message', 'Unknown error')}")

        # Layer analysis
        layers = report.get("layer_analysis", {})
        print("\n📊 LAYER ANALYSIS:")
        for layer_name, layer_data in layers.items():
            print(f"  {layer_name.replace('_', ' ').title()}: {layer_data.get('score', 0.0):.1f}%")

        # Benchmark analysis
        benchmark = report.get("benchmark_analysis", {})
        print("\n🎯 BENCHMARK ANALYSIS:")
        print(f"  Current Performance: {benchmark.get('current_performance', 0.0):.1f}%")
        print(f"  Benchmark Target: {benchmark.get('benchmark_target', 0.0):.1f}%")
        print(f"  Benchmark Exceeded: {benchmark.get('benchmark_exceeded', False)}")
        print(f"  Domination Achieved: {benchmark.get('domination_achieved', False)}")

        # Recommendations
        recommendations = report.get("recommendations", [])
        if recommendations:
            print("\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(recommendations, 1):
                priority = rec.get("priority", "medium")
                description = rec.get("description", "No description")
                print(f"  {i}. [{priority.upper()}] {description}")

        print("=" * 70)
