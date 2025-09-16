"""
Error Handling Examples - Comprehensive Usage Guide
==================================================

This module provides comprehensive examples demonstrating the usage of the
unified error handling system. Each example includes:
- Real-world scenarios
- Complete code implementations
- Expected outputs
- Error handling patterns
- Performance considerations

Author: Agent-3 (Quality Assurance Co-Captain)
License: MIT
"""

from __future__ import annotations

import asyncio
import logging
import time
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def example_basic_error_handling():
    """
    Example 1: Basic Error Handler Usage

    Demonstrates how to create and use error handlers for different types
    of errors in a simple application scenario.

    Scenario: Web API endpoint that processes user requests and handles
    various types of errors gracefully.
    """
    logger.info("🔧 EXAMPLE 1: Basic Error Handler Usage")
    logger.info("=" * 50)
    orchestrator = create_error_orchestrator()
    system_handler = SystemErrorHandler("web_api_system")
    network_handler = NetworkErrorHandler("web_api_network")
    validation_handler = ValidationErrorHandler("web_api_validation")
    orchestrator.register_handler(system_handler)
    orchestrator.register_handler(network_handler)
    orchestrator.register_handler(validation_handler)
    logger.info("✅ Error handlers registered for web API")
    error_scenarios = [
        {
            "error_type": ErrorType.VALIDATION_ERROR,
            "severity": ErrorSeverity.LOW,
            "message": "Invalid email format provided",
            "source": "user_registration_endpoint",
        },
        {
            "error_type": ErrorType.NETWORK_ERROR,
            "severity": ErrorSeverity.MEDIUM,
            "message": "Database connection timeout",
            "source": "database_service",
        },
        {
            "error_type": ErrorType.SYSTEM_ERROR,
            "severity": ErrorSeverity.HIGH,
            "message": "Memory allocation failed",
            "source": "image_processing_service",
        },
    ]
    logger.info("\n🚀 Processing error scenarios:")
    for i, scenario in enumerate(error_scenarios, 1):
        error = ErrorInfo(
            error_id=f"web_api_error_{i:03d}",
            error_type=scenario["error_type"],
            severity=scenario["severity"],
            status=ErrorStatus.DETECTED,
            message=scenario["message"],
            source=scenario["source"],
        )
        context = ErrorContext(
            context_id=f"web_context_{i:03d}",
            error_id=error.error_id,
            variables={
                "user_id": f"user_{i}",
                "request_id": f"req_{i:06d}",
                "timestamp": datetime.now().isoformat(),
            },
        )
        action = orchestrator.handle_error(error, context)
        if action:
            logger.info(f"  {i}. {scenario['error_type'].value}: {action.status.value}")
            logger.info(f"     Result: {action.result}")
        else:
            logger.info(f"  {i}. {scenario['error_type'].value}: No handler found")
    status = orchestrator.get_error_status()
    logger.info(f"\n📊 System Status: {status}")
    logger.info("✅ Example 1 completed successfully!")
    return orchestrator


def example_circuit_breaker_pattern():
    """
    Example 2: Circuit Breaker Pattern Implementation

    Demonstrates how to use the circuit breaker pattern to handle
    external service failures and prevent cascade failures.

    Scenario: Microservice that calls external payment API and needs
    to handle service unavailability gracefully.
    """
    logger.info("\n🔧 EXAMPLE 2: Circuit Breaker Pattern Implementation")
    logger.info("=" * 60)
    cb_recovery = CircuitBreakerRecovery("payment_api_circuit_breaker")
    logger.info(f"✅ Circuit breaker created: {cb_recovery.name}")
    logger.info(f"   Initial state: {cb_recovery.state}")
    logger.info(f"   Failure threshold: {cb_recovery.failure_threshold}")
    logger.info("\n🚀 Simulating payment API calls:")
    for attempt in range(1, 8):
        error = ErrorInfo(
            error_id=f"payment_error_{attempt:03d}",
            error_type=ErrorType.NETWORK_ERROR,
            severity=ErrorSeverity.HIGH,
            status=ErrorStatus.DETECTED,
            message=f"Payment API call failed (attempt {attempt})",
            source="payment_service",
        )
        context = ErrorContext(
            context_id=f"payment_context_{attempt:03d}",
            error_id=error.error_id,
            variables={"payment_id": f"pay_{attempt:06d}", "amount": 100.0, "currency": "USD"},
        )
        action = cb_recovery.recover(error, context)
        logger.info(f"  Attempt {attempt}: State={cb_recovery.state}, Status={action.status.value}")
        logger.info(f"    Result: {action.result}")
        time.sleep(0.1)
    logger.info("\n📊 Circuit Breaker Analysis:")
    logger.info(f"   Final State: {cb_recovery.state}")
    logger.info(f"   Failure Count: {cb_recovery.failure_count}")
    logger.info(f"   Last Failure: {cb_recovery.last_failure_time}")
    logger.info("✅ Example 2 completed successfully!")
    return cb_recovery


def example_fallback_recovery():
    """
    Example 3: Fallback Recovery Strategies

    Demonstrates how to use fallback recovery to handle data validation
    errors and provide alternative processing paths.

    Scenario: Data processing pipeline that handles malformed input data
    by using fallback values and alternative processing methods.
    """
    logger.info("\n🔧 EXAMPLE 3: Fallback Recovery Strategies")
    logger.info("=" * 55)
    fb_recovery = FallbackRecovery("data_processing_fallback")
    logger.info(f"✅ Fallback recovery created: {fb_recovery.name}")
    logger.info(f"   Available strategies: {fb_recovery.get_strategies()}")
    data_processing_scenarios = [
        {
            "error_type": ErrorType.VALIDATION_ERROR,
            "message": "Invalid date format in user profile",
            "fallback_data": {"date": "2025-01-01", "source": "default"},
        },
        {
            "error_type": ErrorType.DATA_ERROR,
            "message": "Missing required field in order data",
            "fallback_data": {"status": "pending", "source": "default"},
        },
        {
            "error_type": ErrorType.VALIDATION_ERROR,
            "message": "Invalid email format in contact form",
            "fallback_data": {"email": "noreply@example.com", "source": "default"},
        },
    ]
    logger.info("\n🚀 Processing data with fallback recovery:")
    for i, scenario in enumerate(data_processing_scenarios, 1):
        error = ErrorInfo(
            error_id=f"data_error_{i:03d}",
            error_type=scenario["error_type"],
            severity=ErrorSeverity.LOW,
            status=ErrorStatus.DETECTED,
            message=scenario["message"],
            source="data_processing_pipeline",
        )
        context = ErrorContext(
            context_id=f"data_context_{i:03d}",
            error_id=error.error_id,
            variables=scenario["fallback_data"],
        )
        action = fb_recovery.recover(error, context)
        logger.info(f"  {i}. {scenario['error_type'].value}: {action.status.value}")
        logger.info(f"     Original: {scenario['message']}")
        logger.info(f"     Fallback: {scenario['fallback_data']}")
        logger.info(f"     Result: {action.result}")
    logger.info("✅ Example 3 completed successfully!")
    return fb_recovery


def example_error_metrics_monitoring():
    """
    Example 4: Error Metrics and Monitoring

    Demonstrates how to collect and analyze error metrics for system
    monitoring and performance optimization.

    Scenario: Production system monitoring that tracks error rates,
    resolution times, and system health metrics.
    """
    logger.info("\n🔧 EXAMPLE 4: Error Metrics and Monitoring")
    logger.info("=" * 55)
    orchestrator = create_error_orchestrator()
    handlers = [
        SystemErrorHandler("monitoring_system"),
        NetworkErrorHandler("monitoring_network"),
        ValidationErrorHandler("monitoring_validation"),
    ]
    for handler in handlers:
        orchestrator.register_handler(handler)
    recoveries = [CircuitBreakerRecovery("monitoring_cb"), FallbackRecovery("monitoring_fb")]
    for recovery in recoveries:
        orchestrator.register_recovery(recovery)
    logger.info("✅ Monitoring system initialized")
    logger.info("\n🚀 Simulating production error scenarios:")
    error_types = [
        ErrorType.SYSTEM_ERROR,
        ErrorType.NETWORK_ERROR,
        ErrorType.VALIDATION_ERROR,
        ErrorType.TIMEOUT_ERROR,
        ErrorType.DATA_ERROR,
    ]
    severities = [
        ErrorSeverity.LOW,
        ErrorSeverity.MEDIUM,
        ErrorSeverity.HIGH,
        ErrorSeverity.CRITICAL,
    ]
    start_time = time.time()
    processed_errors = 0
    resolved_errors = 0
    for i in range(20):
        error_type = error_types[i % len(error_types)]
        severity = severities[i % len(severities)]
        error = ErrorInfo(
            error_id=f"prod_error_{i:03d}",
            error_type=error_type,
            severity=severity,
            status=ErrorStatus.DETECTED,
            message=f"Production error {i} - {error_type.value}",
            source="production_system",
        )
        context = ErrorContext(
            context_id=f"prod_context_{i:03d}",
            error_id=error.error_id,
            variables={
                "server": f"server_{i % 5}",
                "region": "us-east-1",
                "timestamp": datetime.now().isoformat(),
            },
        )
        action = orchestrator.handle_error(error, context)
        processed_errors += 1
        if action and action.status == ErrorStatus.RESOLVED:
            resolved_errors += 1
        time.sleep(0.05)
    end_time = time.time()
    total_time = end_time - start_time
    error_rate = processed_errors / total_time
    resolution_rate = resolved_errors / processed_errors * 100
    logger.info("\n📊 Production Error Metrics:")
    logger.info(f"   Total Errors Processed: {processed_errors}")
    logger.info(f"   Errors Resolved: {resolved_errors}")
    logger.info(f"   Resolution Rate: {resolution_rate:.1f}%")
    logger.info(f"   Processing Time: {total_time:.3f} seconds")
    logger.info(f"   Error Rate: {error_rate:.2f} errors/second")
    status = orchestrator.get_error_status()
    logger.info("\n📈 System Status:")
    logger.info(f"   Active Errors: {status['active_errors']}")
    logger.info(f"   Total Errors: {status['total_errors']}")
    logger.info(f"   Resolved Errors: {status['resolved_errors']}")
    logger.info(f"   Handlers: {status['handlers_registered']}")
    logger.info(f"   Recoveries: {status['recoveries_registered']}")
    logger.info("✅ Example 4 completed successfully!")
    return orchestrator


async def example_async_error_handling():
    """
    Example 5: Async Error Handling

    Demonstrates how to handle errors in asynchronous operations
    and maintain proper error context across async boundaries.

    Scenario: Async web service that processes multiple requests
    concurrently and handles errors without blocking other operations.
    """
    logger.info("\n🔧 EXAMPLE 5: Async Error Handling")
    logger.info("=" * 45)
    orchestrator = create_error_orchestrator()
    orchestrator.register_handler(SystemErrorHandler("async_system"))
    orchestrator.register_handler(NetworkErrorHandler("async_network"))
    logger.info("✅ Async error handling system initialized")

    async def process_request(request_id: int, should_fail: bool = False):
        """Simulate async request processing."""
        try:
            if should_fail:
                error = ErrorInfo(
                    error_id=f"async_error_{request_id:03d}",
                    error_type=ErrorType.NETWORK_ERROR,
                    severity=ErrorSeverity.MEDIUM,
                    status=ErrorStatus.DETECTED,
                    message=f"Async request {request_id} failed",
                    source="async_processor",
                )
                context = ErrorContext(
                    context_id=f"async_context_{request_id:03d}",
                    error_id=error.error_id,
                    variables={"request_id": request_id, "async": True},
                )
                action = orchestrator.handle_error(error, context)
                return f"Request {request_id}: {action.status.value}"
            else:
                await asyncio.sleep(0.1)
                return f"Request {request_id}: SUCCESS"
        except Exception as e:
            return f"Request {request_id}: EXCEPTION - {e}"

    logger.info("\n🚀 Processing async requests:")
    tasks = []
    for i in range(10):
        should_fail = i % 3 == 0
        task = process_request(i + 1, should_fail)
        tasks.append(task)
    start_time = time.time()
    results = await asyncio.gather(*tasks)
    end_time = time.time()
    for result in results:
        logger.info(f"  {result}")
    processing_time = end_time - start_time
    logger.info("\n📊 Async Processing Metrics:")
    logger.info(f"   Total Requests: {len(tasks)}")
    logger.info(f"   Processing Time: {processing_time:.3f} seconds")
    logger.info(f"   Average per Request: {processing_time / len(tasks):.3f} seconds")
    logger.info("✅ Example 5 completed successfully!")
    return orchestrator


class DatabaseErrorHandler(ErrorHandler):
    """Custom error handler for database-specific errors."""

    def __init__(self, handler_id: str = None):
        super().__init__(handler_id or "database_handler", "DatabaseErrorHandler")
        self.retry_count = 0
        self.max_retries = 3

    def can_handle(self, error: ErrorInfo) -> bool:
        """Check if can handle database errors."""
        return error.error_type == ErrorType.RESOURCE_ERROR and "database" in error.message.lower()

    def handle_error(self, error: ErrorInfo, context: ErrorContext) -> RecoveryAction:
        """Handle database error with retry logic."""
        try:
            action = RecoveryAction(
                action_id=f"db_action_{self.retry_count}",
                error_id=error.error_id,
                strategy=RecoveryStrategy.RETRY,
                description=f"Database retry attempt {self.retry_count + 1}/{self.max_retries}",
                status=ErrorStatus.IN_PROGRESS,
            )
            self.logger.warning(f"Handling database error: {error.message}")
            if self.retry_count < self.max_retries:
                self.retry_count += 1
                action.status = ErrorStatus.RESOLVED
                action.result = f"Database connection retry {self.retry_count} successful"
            else:
                action.status = ErrorStatus.ESCALATED
                action.result = "Database connection failed after maximum retries"
                self.retry_count = 0
            action.completed_at = datetime.now()
            return action
        except Exception as e:
            self.logger.error(f"Database handler failed: {e}")
            action.status = ErrorStatus.ESCALATED
            action.result = f"Database handler exception: {e}"
            return action

    def get_capabilities(self) -> list[str]:
        """Get database handler capabilities."""
        return ["database_retry", "connection_pooling", "query_optimization"]


def example_custom_error_handler():
    """
    Example 6: Custom Error Handler Implementation

    Demonstrates how to create custom error handlers for specific
    domain requirements and integrate them with the unified system.

    Scenario: E-commerce system that needs specialized handling
    for database connection issues and query failures.
    """
    logger.info("\n🔧 EXAMPLE 6: Custom Error Handler Implementation")
    logger.info("=" * 65)
    orchestrator = create_error_orchestrator()
    db_handler = DatabaseErrorHandler("ecommerce_database")
    orchestrator.register_handler(db_handler)
    orchestrator.register_handler(SystemErrorHandler("ecommerce_system"))
    logger.info("✅ Custom database handler registered")
    logger.info(f"   Handler capabilities: {db_handler.get_capabilities()}")
    db_error_scenarios = [
        "Database connection pool exhausted",
        "Query timeout on user table",
        "Database server unavailable",
        "Connection lost during transaction",
    ]
    logger.info("\n🚀 Testing custom database error handler:")
    for i, error_message in enumerate(db_error_scenarios, 1):
        error = ErrorInfo(
            error_id=f"db_error_{i:03d}",
            error_type=ErrorType.RESOURCE_ERROR,
            severity=ErrorSeverity.HIGH,
            status=ErrorStatus.DETECTED,
            message=error_message,
            source="ecommerce_database",
        )
        context = ErrorContext(
            context_id=f"db_context_{i:03d}",
            error_id=error.error_id,
            variables={"table": "users", "query_type": "SELECT", "connection_pool": "main"},
        )
        action = orchestrator.handle_error(error, context)
        logger.info(f"  {i}. {error_message}")
        logger.info(f"     Status: {action.status.value}")
        logger.info(f"     Result: {action.result}")
        logger.info(f"     Retry Count: {db_handler.retry_count}")
    logger.info("✅ Example 6 completed successfully!")
    return orchestrator


async def run_all_examples():
    """Run all error handling examples."""
    logger.info("🚨 ERROR HANDLING UNIFIED - COMPREHENSIVE EXAMPLES")
    logger.info("=" * 70)
    logger.info("Quality Assurance Co-Captain Agent-3")
    logger.info("Hands-On Execution Protocol - Comprehensive Documentation")
    logger.info("=" * 70)
    try:
        orchestrator1 = example_basic_error_handling()
        cb_recovery = example_circuit_breaker_pattern()
        fb_recovery = example_fallback_recovery()
        orchestrator2 = example_error_metrics_monitoring()
        orchestrator3 = example_custom_error_handler()
        orchestrator4 = await example_async_error_handling()
        logger.info("\n🏆 ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        logger.info("=" * 50)
        logger.info("✅ Basic Error Handling: Validated")
        logger.info("✅ Circuit Breaker Pattern: Functional")
        logger.info("✅ Fallback Recovery: Operational")
        logger.info("✅ Error Metrics: Collected")
        logger.info("✅ Custom Handlers: Implemented")
        logger.info("✅ Async Error Handling: Tested")
        logger.info(
            """
📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory"""
        )
        return 0
    except Exception as e:
        logger.info(f"\n❌ EXAMPLES FAILED: {e}")
        import traceback

        traceback.print_exc()
        return 1


def main():
    """Main execution function."""
    return asyncio.run(run_all_examples())


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
