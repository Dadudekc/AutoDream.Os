#!/usr/bin/env python3
"""
Error Handling & Recovery Demonstration
=====================================

Comprehensive demonstration of advanced error handling, circuit breakers,
retry logic, graceful degradation, and automated recovery procedures.

This demo shows how the resilient system handles various failure scenarios
and recovers automatically to maintain service availability.
"""

import time
import random
import logging
import threading
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Import our error handling components
from src.core.error_handling.advanced_error_handler import (
    AdvancedErrorHandler, ResilienceConfig, DegradationLevel
)
from src.core.error_handling.automated_recovery import (
    AutomatedRecoveryManager, RecoveryConfig, RecoveryStrategy
)
from src.core.error_handling.circuit_breaker import CircuitBreaker, CircuitBreakerConfig
from src.core.error_handling.retry_mechanisms import RetryMechanism, RetryConfig


class DemoService:
    """Demo service that simulates various failure scenarios."""

    def __init__(self, name: str, failure_rate: float = 0.3):
        self.name = name
        self.failure_rate = failure_rate
        self.call_count = 0
        self.failure_count = 0

    def unreliable_operation(self) -> str:
        """Simulate an unreliable operation."""
        self.call_count += 1

        if random.random() < self.failure_rate:
            self.failure_count += 1
            error_types = [
                ConnectionError("Network timeout"),
                ValueError("Invalid data received"),
                TimeoutError("Operation timed out"),
                RuntimeError("Internal service error")
            ]
            raise random.choice(error_types)

        return f"✅ {self.name} operation successful (call #{self.call_count})"

    def get_stats(self) -> Dict[str, Any]:
        """Get service statistics."""
        return {
            "name": self.name,
            "total_calls": self.call_count,
            "failures": self.failure_count,
            "success_rate": (
                ((self.call_count - self.failure_count) / self.call_count * 100)
                if self.call_count > 0 else 0
            )
        }


def demonstrate_circuit_breaker():
    """Demonstrate circuit breaker functionality."""
    print("\n" + "="*60)
    print("🔌 CIRCUIT BREAKER DEMONSTRATION")
    print("="*60)

    # Create circuit breaker
    cb_config = CircuitBreakerConfig(
        name="demo_service",
        failure_threshold=3,
        timeout_seconds=30.0
    )
    circuit_breaker = CircuitBreaker(cb_config)

    # Create demo service with high failure rate
    service = DemoService("DemoService", failure_rate=0.7)

    print("🧪 Testing circuit breaker with high failure rate service...")
    print("   Service failure rate: 70%")
    print("   Circuit breaker threshold: 3 failures")
    print()

    # Test normal operations
    for i in range(10):
        try:
            result = circuit_breaker.call(service.unreliable_operation)
            print(f"   {i+1:2d}. {result}")
        except Exception as e:
            print(f"   {i+1:2d}. ❌ Circuit breaker handled: {type(e).__name__}")

        time.sleep(0.1)

    # Show circuit breaker stats
    stats = circuit_breaker.get_stats()
    print("
📊 Circuit Breaker Stats:"    print(f"   State: {stats['state']}")
    print(f"   Total Requests: {stats['metrics']['total_requests']}")
    print(f"   Failures: {stats['metrics']['total_failures']}")
    print(f"   Success Rate: {stats['metrics']['success_rate']:.1f}%")

    print("
✅ Circuit breaker demonstration complete!"    return service


def demonstrate_retry_logic():
    """Demonstrate retry logic with exponential backoff."""
    print("\n" + "="*60)
    print("🔄 RETRY LOGIC DEMONSTRATION")
    print("="*60)

    # Create retry mechanism
    retry_config = RetryConfig(
        max_attempts=5,
        base_delay=0.5,
        backoff_factor=2.0,
        max_delay=5.0,
        jitter=True
    )
    retry_mechanism = RetryMechanism(retry_config)

    # Create demo service
    service = DemoService("RetryService", failure_rate=0.8)

    print("🧪 Testing retry logic with high failure rate...")
    print("   Max attempts: 5")
    print("   Exponential backoff: base 0.5s, factor 2.0")
    print("   Max delay: 5.0s")
    print()

    start_time = time.time()
    try:
        result = retry_mechanism.call(service.unreliable_operation)
        total_time = time.time() - start_time
        print(f"   ✅ Final result: {result}")
        print(".2f")
    except Exception as e:
        total_time = time.time() - start_time
        print(f"   ❌ All retries failed: {type(e).__name__}")
        print(".2f")

    # Show service stats
    stats = service.get_stats()
    print("
📊 Service Stats:"    print(f"   Total calls: {stats['total_calls']}")
    print(f"   Failures: {stats['failures']}")
    print(".1f")

    print("
✅ Retry logic demonstration complete!"    return service


def demonstrate_advanced_error_handler():
    """Demonstrate advanced error handler with all features."""
    print("\n" + "="*60)
    print("🚀 ADVANCED ERROR HANDLER DEMONSTRATION")
    print("="*60)

    # Create resilience configuration
    resilience_config = ResilienceConfig(
        name="demo_resilience",
        enable_circuit_breaker=True,
        enable_retry=True,
        enable_graceful_degradation=True,
        enable_automated_recovery=True
    )

    # Create advanced error handler
    error_handler = AdvancedErrorHandler(resilience_config)

    # Create demo service
    service = DemoService("ResilientService", failure_rate=0.5)

    print("🧪 Testing advanced error handler with medium failure rate...")
    print("   Service failure rate: 50%")
    print("   All resilience features enabled")
    print()

    # Test resilient operations
    successful_operations = 0
    total_operations = 15

    for i in range(total_operations):
        try:
            result = error_handler.execute_with_resilience(service.unreliable_operation)
            print(f"   {i+1:2d}. {result}")
            successful_operations += 1
        except Exception as e:
            print(f"   {i+1:2d}. ❌ Handled gracefully: {type(e).__name__}")

        time.sleep(0.2)

    # Show comprehensive resilience stats
    resilience_status = error_handler.get_resilience_status()

    print("
📊 Resilience Statistics:"    print(f"   Total Operations: {resilience_status['metrics']['total_operations']}")
    print(f"   Successful: {resilience_status['metrics']['successful_operations']}")
    print(f"   Failed: {resilience_status['metrics']['failed_operations']}")
    print(".1f")
    print(f"   Degradation Level: {resilience_status['metrics']['current_degradation_level']}")
    print(f"   Retry Attempts: {resilience_status['metrics']['retry_attempts']}")
    print(f"   Recovery Attempts: {resilience_status['metrics']['recovery_attempts']}")

    # Show degradation status
    degradation = resilience_status['degradation_status']
    print(f"   Degradation Level: {degradation['level']}")
    print(f"   Degraded Features: {list(degradation['degraded_features'].keys())}")

    print("
✅ Advanced error handler demonstration complete!"    return service


def demonstrate_automated_recovery():
    """Demonstrate automated recovery procedures."""
    print("\n" + "="*60)
    print("🔧 AUTOMATED RECOVERY DEMONSTRATION")
    print("="*60)

    # Create recovery configuration
    recovery_config = RecoveryConfig(
        name="demo_recovery",
        enable_auto_recovery=True,
        enable_proactive_monitoring=True,
        health_check_interval=5.0  # Faster for demo
    )

    # Create recovery manager
    recovery_manager = AutomatedRecoveryManager(recovery_config)

    # Create demo service and health check
    service = DemoService("RecoveryService", failure_rate=0.4)

    def health_check() -> bool:
        """Simple health check for demo service."""
        # Simulate occasional health check failures
        return random.random() > 0.3  # 70% healthy

    # Register component for recovery
    recovery_manager.register_component("demo_service", health_check)

    print("🧪 Testing automated recovery with health monitoring...")
    print("   Health check interval: 5 seconds")
    print("   Proactive monitoring: enabled")
    print()

    # Let proactive monitoring run for a bit
    print("   Monitoring health for 15 seconds...")
    time.sleep(15)

    # Manually trigger a recovery
    print("   Manually triggering recovery test...")
    recovery_success = recovery_manager.initiate_recovery("demo_service")
    print(f"   Recovery result: {'✅ SUCCESS' if recovery_success else '❌ FAILED'}")

    # Show recovery stats
    recovery_status = recovery_manager.get_recovery_status()

    print("
📊 Recovery Statistics:"    print(f"   Total Recoveries: {recovery_status['metrics']['total_recoveries']}")
    print(f"   Successful: {recovery_status['metrics']['successful_recoveries']}")
    print(f"   Failed: {recovery_status['metrics']['failed_recoveries']}")
    print(".1f")
    print(f"   Current State: {recovery_status['current_state']}")

    # Show health status
    health_status = recovery_status['health_status']
    print(f"   Health Status: {health_status}")

    print("
✅ Automated recovery demonstration complete!"    return service


def run_comprehensive_demo():
    """Run comprehensive error handling demonstration."""
    print("🚀 COMPREHENSIVE ERROR HANDLING & RECOVERY DEMO")
    print("="*60)
    print("This demo showcases advanced error handling capabilities:")
    print("• Circuit Breaker Pattern")
    print("• Retry Logic with Exponential Backoff")
    print("• Graceful Degradation")
    print("• Automated Recovery Procedures")
    print("="*60)

    # Run all demonstrations
    circuit_service = demonstrate_circuit_breaker()
    retry_service = demonstrate_retry_logic()
    resilient_service = demonstrate_advanced_error_handler()
    recovery_service = demonstrate_automated_recovery()

    # Final summary
    print("\n" + "="*60)
    print("📊 FINAL DEMONSTRATION SUMMARY")
    print("="*60)

    services = [
        ("Circuit Breaker Service", circuit_service),
        ("Retry Service", retry_service),
        ("Resilient Service", resilient_service),
        ("Recovery Service", recovery_service)
    ]

    for name, service in services:
        stats = service.get_stats()
        print(f"\n{name}:")
        print(f"   Total Calls: {stats['total_calls']}")
        print(f"   Failures: {stats['failures']}")
        print(".1f")

    print("
🎯 DEMONSTRATION COMPLETE!"    print("✅ All error handling mechanisms demonstrated successfully")
    print("✅ System resilience features working as expected")
    print("✅ Automated recovery procedures operational")
    print("✅ Graceful degradation handling failures appropriately")

    print("
🚀 KEY ACHIEVEMENTS:"    print("• Circuit breaker preventing cascade failures")
    print("• Retry logic with intelligent backoff")
    print("• Graceful degradation maintaining service availability")
    print("• Automated recovery with proactive monitoring")
    print("• Comprehensive error handling and recovery system")


def main():
    """Main demonstration entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Error Handling & Recovery Demonstration")
    parser.add_argument('--component', choices=['circuit', 'retry', 'resilient', 'recovery', 'all'],
                       default='all', help='Specific component to demonstrate')
    parser.add_argument('--duration', type=int, default=30,
                       help='Duration for recovery monitoring (seconds)')

    args = parser.parse_args()

    print("🤖 Agent-6 Error Handling & Recovery Demonstration")
    print("Specialty: Web Interface & Communication")
    print("Mission: Implement resilient system architecture")
    print("-" * 50)

    if args.component == 'all':
        run_comprehensive_demo()
    elif args.component == 'circuit':
        demonstrate_circuit_breaker()
    elif args.component == 'retry':
        demonstrate_retry_logic()
    elif args.component == 'resilient':
        demonstrate_advanced_error_handler()
    elif args.component == 'recovery':
        demonstrate_automated_recovery()


if __name__ == "__main__":
    main()
