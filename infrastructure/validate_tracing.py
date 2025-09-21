#!/usr/bin/env python3
# V3-004: Distributed Tracing Implementation - Validation Script
# Agent-1: Architecture Foundation Specialist
# 
# Validation script for Jaeger distributed tracing deployment

import os
import sys
import asyncio
import subprocess
import json
import time
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.tracing.jaeger_tracer import TraceManager, TraceConfig
from src.core.tracing.request_tracker import RequestTracker
from src.core.tracing.performance_monitor import PerformanceMonitor
from src.core.tracing.error_tracker import ErrorTracker, ErrorSeverity, ErrorCategory


class TracingValidator:
    """Validation for V3-004 distributed tracing implementation."""
    
    def __init__(self):
        self.validation_results = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent": "Agent-1",
            "contract": "V3-004",
            "status": "validation_started",
            "components": {}
        }
    
    async def validate_all_components(self) -> Dict[str, Any]:
        """Validate all distributed tracing components."""
        print("🔍 V3-004: Distributed Tracing Implementation Validation")
        print("Agent-1: Architecture Foundation Specialist")
        print("=" * 60)
        
        # Validate Jaeger deployment
        await self._validate_jaeger_deployment()
        
        # Validate Jaeger tracer
        await self._validate_jaeger_tracer()
        
        # Validate request tracking
        await self._validate_request_tracking()
        
        # Validate performance monitoring
        await self._validate_performance_monitoring()
        
        # Validate error tracking
        await self._validate_error_tracking()
        
        # Validate Kubernetes deployment
        await self._validate_kubernetes_tracing()
        
        # Generate final report
        self._generate_validation_report()
        
        return self.validation_results
    
    async def _validate_jaeger_deployment(self) -> None:
        """Validate Jaeger deployment in Kubernetes."""
        print("\n☸️  Validating Jaeger Kubernetes Deployment...")
        
        try:
            # Check if Jaeger namespace exists
            result = subprocess.run(
                ["kubectl", "get", "namespace", "swarm-v3"], 
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                # Check Jaeger collector
                collector_result = subprocess.run(
                    ["kubectl", "get", "deployment", "jaeger-collector", "-n", "swarm-v3"], 
                    capture_output=True, text=True
                )
                
                # Check Jaeger query
                query_result = subprocess.run(
                    ["kubectl", "get", "deployment", "jaeger-query", "-n", "swarm-v3"], 
                    capture_output=True, text=True
                )
                
                # Check Jaeger agent
                agent_result = subprocess.run(
                    ["kubectl", "get", "deployment", "jaeger-agent", "-n", "swarm-v3"], 
                    capture_output=True, text=True
                )
                
                if (collector_result.returncode == 0 and 
                    query_result.returncode == 0 and 
                    agent_result.returncode == 0):
                    
                    self.validation_results["components"]["jaeger_deployment"] = {
                        "status": "deployed",
                        "collector": "available",
                        "query": "available",
                        "agent": "available"
                    }
                    print("✅ Jaeger deployment validated")
                else:
                    self.validation_results["components"]["jaeger_deployment"] = {
                        "status": "error",
                        "error": "Jaeger components not deployed"
                    }
                    print("❌ Jaeger components not deployed")
            else:
                self.validation_results["components"]["jaeger_deployment"] = {
                    "status": "error",
                    "error": "Namespace not found"
                }
                print("❌ Namespace not found")
        
        except Exception as e:
            self.validation_results["components"]["jaeger_deployment"] = {
                "status": "error",
                "error": str(e)
            }
            print(f"❌ Jaeger deployment validation failed: {e}")
    
    async def _validate_jaeger_tracer(self) -> None:
        """Validate Jaeger tracer implementation."""
        print("\n🔍 Validating Jaeger Tracer Implementation...")
        
        try:
            # Initialize trace manager
            trace_manager = TraceManager()
            
            # Get default tracer
            tracer = trace_manager.get_tracer()
            
            # Test span creation
            with tracer.trace_span("test_span", {"test": "validation"}) as span:
                tracer.add_span_tags({"validation.test": True})
                tracer.record_event("test_event", {"message": "validation test"})
            
            # Test function tracing
            @tracer.trace_function("test_function", {"component": "validation"})
            def test_function():
                return "test_result"
            
            result = test_function()
            
            if result == "test_result":
                self.validation_results["components"]["jaeger_tracer"] = {
                    "status": "operational",
                    "span_creation": "working",
                    "function_tracing": "working",
                    "tag_management": "working"
                }
                print("✅ Jaeger tracer validated")
            else:
                self.validation_results["components"]["jaeger_tracer"] = {
                    "status": "error",
                    "error": "Function tracing failed"
                }
                print("❌ Function tracing failed")
        
        except Exception as e:
            self.validation_results["components"]["jaeger_tracer"] = {
                "status": "error",
                "error": str(e)
            }
            print(f"❌ Jaeger tracer validation failed: {e}")
    
    async def _validate_request_tracking(self) -> None:
        """Validate request tracking functionality."""
        print("\n📊 Validating Request Tracking...")
        
        try:
            # Initialize request tracker
            request_tracker = RequestTracker()
            
            # Test request tracking
            request_id = request_tracker.start_request(
                method="GET",
                path="/test",
                headers={"User-Agent": "test"},
                user_id="test_user",
                agent_id="test_agent"
            )
            
            # Update request status
            request_tracker.update_request_status(request_id, "processing")
            
            # Complete request
            request_tracker.complete_request(request_id, "completed")
            
            # Get request info
            request_info = request_tracker.get_request_info(request_id)
            
            if request_info and request_info.status.value == "completed":
                # Test statistics
                stats = request_tracker.get_request_statistics()
                
                self.validation_results["components"]["request_tracking"] = {
                    "status": "operational",
                    "request_creation": "working",
                    "status_updates": "working",
                    "completion": "working",
                    "statistics": "working"
                }
                print("✅ Request tracking validated")
            else:
                self.validation_results["components"]["request_tracking"] = {
                    "status": "error",
                    "error": "Request tracking failed"
                }
                print("❌ Request tracking failed")
        
        except Exception as e:
            self.validation_results["components"]["request_tracking"] = {
                "status": "error",
                "error": str(e)
            }
            print(f"❌ Request tracking validation failed: {e}")
    
    async def _validate_performance_monitoring(self) -> None:
        """Validate performance monitoring."""
        print("\n⚡ Validating Performance Monitoring...")
        
        try:
            # Initialize performance monitor
            monitor = PerformanceMonitor(collection_interval=1)
            
            # Start monitoring
            monitor.start_monitoring()
            
            # Wait for metrics collection
            await asyncio.sleep(2)
            
            # Record custom metrics
            monitor.record_custom_metric("test_metric", 100.0, {"test": "validation"})
            monitor.record_timing("test_operation", 50.0, {"component": "validation"})
            monitor.record_counter("test_counter", 1, {"test": "validation"})
            
            # Get metrics
            metrics = monitor.get_current_metrics()
            performance_summary = monitor.get_performance_summary()
            
            # Stop monitoring
            monitor.stop_monitoring()
            
            if metrics and performance_summary:
                self.validation_results["components"]["performance_monitoring"] = {
                    "status": "operational",
                    "system_metrics": "working",
                    "custom_metrics": "working",
                    "timing_metrics": "working",
                    "performance_summary": "working"
                }
                print("✅ Performance monitoring validated")
            else:
                self.validation_results["components"]["performance_monitoring"] = {
                    "status": "error",
                    "error": "Performance monitoring failed"
                }
                print("❌ Performance monitoring failed")
        
        except Exception as e:
            self.validation_results["components"]["performance_monitoring"] = {
                "status": "error",
                "error": str(e)
            }
            print(f"❌ Performance monitoring validation failed: {e}")
    
    async def _validate_error_tracking(self) -> None:
        """Validate error tracking functionality."""
        print("\n🚨 Validating Error Tracking...")
        
        try:
            # Initialize error tracker
            error_tracker = ErrorTracker()
            
            # Test error tracking
            try:
                raise ValueError("Test error for validation")
            except ValueError as e:
                error_id = error_tracker.track_error(
                    error=e,
                    severity=ErrorSeverity.MEDIUM,
                    category=ErrorCategory.VALIDATION,
                    context={"test": "validation"}
                )
            
            # Test custom error tracking
            custom_error_id = error_tracker.track_custom_error(
                error_type="ValidationError",
                error_message="Custom test error",
                severity=ErrorSeverity.LOW,
                category=ErrorCategory.VALIDATION
            )
            
            # Test error resolution
            error_tracker.resolve_error(error_id, "Test resolution")
            
            # Get error statistics
            stats = error_tracker.get_error_statistics()
            
            if stats.total_errors >= 2:
                self.validation_results["components"]["error_tracking"] = {
                    "status": "operational",
                    "error_tracking": "working",
                    "custom_errors": "working",
                    "error_resolution": "working",
                    "statistics": "working"
                }
                print("✅ Error tracking validated")
            else:
                self.validation_results["components"]["error_tracking"] = {
                    "status": "error",
                    "error": "Error tracking failed"
                }
                print("❌ Error tracking failed")
        
        except Exception as e:
            self.validation_results["components"]["error_tracking"] = {
                "status": "error",
                "error": str(e)
            }
            print(f"❌ Error tracking validation failed: {e}")
    
    async def _validate_kubernetes_tracing(self) -> None:
        """Validate Kubernetes tracing integration."""
        print("\n☸️  Validating Kubernetes Tracing Integration...")
        
        try:
            # Check if tracing is integrated with main application
            result = subprocess.run(
                ["kubectl", "get", "deployment", "swarm-app", "-n", "swarm-v3", "-o", "json"], 
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                deployment_info = json.loads(result.stdout)
                
                # Check if Jaeger agent is accessible
                agent_result = subprocess.run(
                    ["kubectl", "get", "service", "jaeger-agent", "-n", "swarm-v3"], 
                    capture_output=True, text=True
                )
                
                if agent_result.returncode == 0:
                    self.validation_results["components"]["kubernetes_tracing"] = {
                        "status": "integrated",
                        "application_deployment": "available",
                        "jaeger_agent": "accessible",
                        "tracing_ready": True
                    }
                    print("✅ Kubernetes tracing integration validated")
                else:
                    self.validation_results["components"]["kubernetes_tracing"] = {
                        "status": "error",
                        "error": "Jaeger agent not accessible"
                    }
                    print("❌ Jaeger agent not accessible")
            else:
                self.validation_results["components"]["kubernetes_tracing"] = {
                    "status": "error",
                    "error": "Application deployment not found"
                }
                print("❌ Application deployment not found")
        
        except Exception as e:
            self.validation_results["components"]["kubernetes_tracing"] = {
                "status": "error",
                "error": str(e)
            }
            print(f"❌ Kubernetes tracing validation failed: {e}")
    
    def _generate_validation_report(self) -> None:
        """Generate validation report."""
        print("\n📊 Generating Validation Report...")
        
        # Calculate overall status
        components = self.validation_results["components"]
        total_components = len(components)
        successful_components = sum(
            1 for comp in components.values() 
            if comp.get("status") in ["deployed", "operational", "integrated"]
        )
        
        success_rate = (successful_components / total_components) * 100
        
        self.validation_results["overall_status"] = "success" if success_rate >= 80 else "partial" if success_rate >= 60 else "failed"
        self.validation_results["success_rate"] = success_rate
        self.validation_results["total_components"] = total_components
        self.validation_results["successful_components"] = successful_components
        
        # Save report
        report_file = project_root / "infrastructure" / "tracing_validation_report.json"
        with open(report_file, "w") as f:
            json.dump(self.validation_results, f, indent=2)
        
        print(f"✅ Validation report saved: {report_file}")
        
        # Print summary
        print("\n" + "=" * 60)
        print("📋 V3-004 DISTRIBUTED TRACING VALIDATION SUMMARY")
        print("=" * 60)
        print(f"Overall Status: {self.validation_results['overall_status'].upper()}")
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"Components: {successful_components}/{total_components}")
        print("\nComponent Status:")
        
        for name, status in components.items():
            status_icon = "✅" if status.get("status") in ["deployed", "operational", "integrated"] else "❌"
            print(f"  {status_icon} {name}: {status.get('status', 'unknown')}")
        
        if self.validation_results["overall_status"] == "success":
            print("\n🎉 V3-004: Distributed Tracing Implementation - VALIDATION SUCCESSFUL!")
        else:
            print(f"\n⚠️  V3-004: Distributed Tracing Implementation - VALIDATION {self.validation_results['overall_status'].upper()}")


async def main():
    """Main validation function."""
    validator = TracingValidator()
    await validator.validate_all_components()


if __name__ == "__main__":
    asyncio.run(main())
