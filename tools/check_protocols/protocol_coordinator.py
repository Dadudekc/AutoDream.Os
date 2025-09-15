#!/usr/bin/env python3
"""
Protocol Coordinator - V2 Compliance Module
=========================================

Focused module for coordinating check protocol execution.

V2 Compliance: < 400 lines, single responsibility, modular design.

Author: Agent-5 (Data Organization Specialist)
Test Type: Protocol Coordination
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, Any

from .protocol_validator import ProtocolValidator


class ProtocolCoordinator:
    """Coordinates execution of check protocols."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.validator = ProtocolValidator(project_root)
        self.results = {
            "layer_1_consolidation": {},
            "layer_2_performance": {},
            "overall_score": 0.0,
            "benchmark_comparison": {},
            "coordination_status": "AGENT-5_COORDINATION_ACTIVE"
        }

    async def execute_protocols(self) -> Dict[str, Any]:
        """Execute all check protocols."""
        print("🚀 Starting protocol coordination...")
        
        try:
            # Execute triple-check validation
            validation_results = await self.validator.execute_triple_check()
            
            # Update coordination results
            self.results.update(validation_results)
            self.results["coordination_status"] = "COMPLETED"
            
            return self.results
            
        except Exception as e:
            self.results["coordination_status"] = "ERROR"
            self.results["error"] = str(e)
            return self.results

    def save_results(self, results: Dict[str, Any], filename: str = "protocol_results.json") -> Path:
        """Save protocol results to file."""
        results_dir = self.project_root / "runtime"
        results_dir.mkdir(exist_ok=True)
        
        results_path = results_dir / filename
        
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        return results_path

    def print_summary(self, results: Dict[str, Any]) -> None:
        """Print protocol execution summary."""
        print("\n" + "="*60)
        print("📊 PROTOCOL EXECUTION SUMMARY")
        print("="*60)
        
        print(f"Coordination Status: {results.get('coordination_status', 'UNKNOWN')}")
        print(f"Overall Score: {results.get('overall_score', 0.0):.1f}%")
        
        # Benchmark comparison
        benchmark = results.get('benchmark_comparison', {})
        if benchmark:
            print(f"Agent-2 Benchmark: {benchmark.get('agent_2_benchmark', 0.0)}%")
            print(f"Exceeds Benchmark: {benchmark.get('exceeds_benchmark', False)}")
            print(f"Achieves Domination: {benchmark.get('achieves_domination', False)}")
        
        # Layer results
        layer_1 = results.get('layer_1_structural', {})
        layer_2 = results.get('layer_2_functional', {})
        layer_3 = results.get('layer_3_performance', {})
        
        print(f"\nLayer 1 (Structural): {layer_1.get('score', 0.0):.1f}%")
        print(f"Layer 2 (Functional): {layer_2.get('score', 0.0):.1f}%")
        print(f"Layer 3 (Performance): {layer_3.get('score', 0.0):.1f}%")
        
        print("="*60)

    async def run_competitive_mode(self) -> Dict[str, Any]:
        """Run in competitive domination mode."""
        print("🏆 COMPETITIVE DOMINATION MODE ACTIVATED")
        print("Target: Exceed Agent-2's 99%+ benchmark")
        
        results = await self.execute_protocols()
        
        # Check if domination achieved
        benchmark = results.get('benchmark_comparison', {})
        if benchmark.get('achieves_domination', False):
            print("🎯 DOMINATION ACHIEVED! Exceeded 99.5% threshold!")
        elif benchmark.get('exceeds_benchmark', False):
            print("✅ BENCHMARK EXCEEDED! Beat Agent-2's 99% target!")
        else:
            print("⚠️  Benchmark not exceeded. More optimization needed.")
        
        return results
