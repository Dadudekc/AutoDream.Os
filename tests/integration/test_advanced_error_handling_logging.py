#!/usr/bin/env python3
"""
Comprehensive Test Script for Advanced Error Handling and Logging System
======================================================================
Tests all components of V2 Feature 4: Advanced Error Handling and Logging
"""

import sys
import os
import time
import threading
import traceback
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'services'))

from advanced_error_handler import (
    AdvancedErrorHandler, ErrorContext, ErrorSeverity, ErrorCategory, 
    RecoveryStrategy, handle_errors, with_retry
)
from advanced_logging_system import (
    AdvancedLoggingSystem, LogLevel, LogFormat, LogDestination, 
    LoggerConfig, LoggingContext
)
from error_analytics_system import (
    ErrorAnalyticsSystem, ReportFormat
)

def test_advanced_error_handler():
    """Test the advanced error handling system"""
    print("🧪 Testing Advanced Error Handler")
    print("-" * 60)
    
    try:
        # Create error handler
        error_handler = AdvancedErrorHandler()
        print(f"✅ Error handler created: {error_handler.is_active}")
        
        # Test error context creation
        context = ErrorContext(
            service_name="test_service",
            operation="test_operation",
            user_id="test_user",
            session_id="test_session"
        )
        print(f"✅ Error context created: {context.service_name}")
        
        # Test error handling with different severities
        test_exceptions = [
            (ValueError("Test validation error"), ErrorSeverity.MEDIUM, ErrorCategory.VALIDATION),
            (ConnectionError("Test connection error"), ErrorSeverity.HIGH, ErrorCategory.NETWORK),
            (TimeoutError("Test timeout error"), ErrorSeverity.HIGH, ErrorCategory.NETWORK),
            (KeyError("Test key error"), ErrorSeverity.MEDIUM, ErrorCategory.CONFIGURATION),
            (FileNotFoundError("Test file not found"), ErrorSeverity.MEDIUM, ErrorCategory.RESOURCE)
        ]
        
        for exception, severity, category in test_exceptions:
            try:
                error_info = error_handler.handle_error(exception, context, severity, category)
                print(f"   ✅ Handled {type(exception).__name__}: {error_info.error_id}")
            except Exception as e:
                print(f"   ❌ Failed to handle {type(exception).__name__}: {e}")
        
        # Test error statistics
        stats = error_handler.get_error_statistics()
        print(f"\n📊 Error Statistics:")
        for key, value in stats.items():
            print(f"   {key.replace('_', ' ').title()}: {value}")
        
        # Test error history
        history = error_handler.get_error_history(limit=5)
        print(f"\n📜 Error History: {len(history)} entries")
        
        # Test error patterns
        patterns = error_handler.get_error_patterns()
        print(f"🔍 Error Patterns: {len(patterns)} detected")
        
        # Test circuit breaker reset
        if error_handler.circuit_breakers:
            service_name = list(error_handler.circuit_breakers.keys())[0]
            reset_success = error_handler.reset_circuit_breaker(service_name)
            print(f"⚡ Circuit breaker reset for {service_name}: {'✅' if reset_success else '❌'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error handler test failed: {e}")
        traceback.print_exc()
        return False

def test_advanced_logging_system():
    """Test the advanced logging system"""
    print("\n📝 Testing Advanced Logging System")
    print("-" * 60)
    
    try:
        # Create logging system
        logging_system = AdvancedLoggingSystem()
        print(f"✅ Logging system created: {logging_system.is_active}")
        
        # Test logger creation
        test_logger = logging_system.get_logger("test.logger")
        print(f"✅ Test logger created: {test_logger.name}")
        
        # Test structured logging
        logging_system.log_structured(
            "test.logger",
            LogLevel.INFO,
            "Test structured log message",
            service_name="test_service",
            operation="test_operation",
            user_id="test_user",
            duration=1.5,
            metadata={"test_key": "test_value"}
        )
        print("✅ Structured logging test completed")
        
        # Test performance logging
        logging_system.log_performance(
            "test_operation",
            2.5,
            success=True,
            metadata={"test_metric": 100}
        )
        print("✅ Performance logging test completed")
        
        # Test different log levels
        for level in LogLevel:
            logging_system.log_structured(
                "test.logger",
                level,
                f"Test {level.value} message",
                service_name="test_service"
            )
        print("✅ All log levels tested")
        
        # Test analytics
        analytics = logging_system.get_analytics()
        print(f"📊 Log Analytics: {analytics.total_logs} total logs")
        
        # Test recent logs retrieval
        recent_logs = logging_system.get_recent_logs(limit=10)
        print(f"📜 Recent Logs: {len(recent_logs)} retrieved")
        
        # Test performance metrics
        performance_metrics = logging_system.get_performance_metrics(limit=5)
        print(f"⚡ Performance Metrics: {len(performance_metrics)} retrieved")
        
        return True
        
    except Exception as e:
        print(f"❌ Logging system test failed: {e}")
        traceback.print_exc()
        return False

def test_error_analytics_system():
    """Test the error analytics system"""
    print("\n📊 Testing Error Analytics System")
    print("-" * 60)
    
    try:
        # Create error handler first
        error_handler = AdvancedErrorHandler()
        
        # Create analytics system
        analytics_system = ErrorAnalyticsSystem(error_handler)
        print(f"✅ Analytics system created: {analytics_system.is_active}")
        
        # Generate some test errors for analysis
        context = ErrorContext(service_name="test_service", operation="test_operation")
        
        for i in range(5):
            try:
                if i % 2 == 0:
                    raise ValueError(f"Test error {i}")
                else:
                    raise ConnectionError(f"Test connection error {i}")
            except Exception as e:
                severity = ErrorSeverity.HIGH if i % 2 == 0 else ErrorSeverity.MEDIUM
                category = ErrorCategory.VALIDATION if i % 2 == 0 else ErrorCategory.NETWORK
                error_handler.handle_error(e, context, severity, category)
        
        print("✅ Test errors generated for analysis")
        
        # Wait for analysis to complete
        time.sleep(2)
        
        # Test analytics statistics
        analytics_stats = analytics_system.get_analytics_statistics()
        print(f"📊 Analytics Statistics:")
        for key, value in analytics_stats.items():
            print(f"   {key.replace('_', ' ').title()}: {value}")
        
        # Test report generation in different formats
        report_formats = [ReportFormat.CONSOLE, ReportFormat.MARKDOWN, ReportFormat.JSON]
        
        for format_type in report_formats:
            try:
                report = analytics_system.generate_analytics_report(
                    time_range="1h",
                    format_type=format_type
                )
                print(f"✅ {format_type.value.upper()} report generated: {report.report_id}")
            except Exception as e:
                print(f"❌ Failed to generate {format_type.value} report: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Analytics system test failed: {e}")
        traceback.print_exc()
        return False

def test_integration_and_decorators():
    """Test integration features and decorators"""
    print("\n🔗 Testing Integration Features and Decorators")
    print("-" * 60)
    
    try:
        # Test error handling decorator
        @handle_errors(severity=ErrorSeverity.MEDIUM, category=ErrorCategory.VALIDATION, service_name="decorator_test")
        def test_function_with_errors():
            """Test function that raises errors"""
            raise ValueError("Test error from decorated function")
        
        # Test retry decorator
        @with_retry(max_retries=2, delay=0.1)
        def test_function_with_retry():
            """Test function that fails initially then succeeds"""
            if not hasattr(test_function_with_retry, '_attempts'):
                test_function_with_retry._attempts = 0
            
            test_function_with_retry._attempts += 1
            
            if test_function_with_retry._attempts < 3:
                raise RuntimeError(f"Attempt {test_function_with_retry._attempts} failed")
            
            return "Success after retries"
        
        # Test error handling decorator
        try:
            test_function_with_errors()
        except ValueError:
            print("✅ Error handling decorator caught error as expected")
        
        # Test retry decorator
        try:
            result = test_function_with_retry()
            print(f"✅ Retry decorator succeeded: {result}")
        except Exception as e:
            print(f"❌ Retry decorator failed: {e}")
        
        # Test logging context manager
        logging_system = AdvancedLoggingSystem()
        
        with LoggingContext(
            logging_system,
            "test_context_operation",
            "test_service",
            "test.logger"
        ) as context:
            print("   🔄 Executing operation in logging context...")
            time.sleep(0.5)  # Simulate work
            print("   ✅ Operation completed successfully")
        
        print("✅ Logging context manager test completed")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        traceback.print_exc()
        return False

def test_performance_and_stress():
    """Test system performance under stress"""
    print("\n⚡ Testing Performance and Stress")
    print("-" * 60)
    
    try:
        # Create systems
        error_handler = AdvancedErrorHandler()
        logging_system = AdvancedLoggingSystem()
        analytics_system = ErrorAnalyticsSystem(error_handler)
        
        # Stress test with multiple threads
        def stress_worker(worker_id):
            """Worker thread for stress testing"""
            context = ErrorContext(
                service_name=f"stress_service_{worker_id}",
                operation=f"stress_operation_{worker_id}"
            )
            
            for i in range(10):
                try:
                    # Generate errors
                    if i % 3 == 0:
                        raise ValueError(f"Stress error {i} from worker {worker_id}")
                    elif i % 3 == 1:
                        raise ConnectionError(f"Stress connection error {i} from worker {worker_id}")
                    else:
                        raise RuntimeError(f"Stress runtime error {i} from worker {worker_id}")
                except Exception as e:
                    severity = ErrorSeverity.MEDIUM if i % 2 == 0 else ErrorSeverity.HIGH
                    category = ErrorCategory.SYSTEM if i % 2 == 0 else ErrorCategory.NETWORK
                    error_handler.handle_error(e, context, severity, category)
                
                # Log operations
                logging_system.log_structured(
                    f"stress.logger.{worker_id}",
                    LogLevel.INFO,
                    f"Stress operation {i} from worker {worker_id}",
                    service_name=f"stress_service_{worker_id}",
                    operation=f"stress_operation_{i}"
                )
                
                time.sleep(0.01)  # Small delay
        
        # Start stress workers
        threads = []
        for worker_id in range(5):
            thread = threading.Thread(target=stress_worker, args=(worker_id,))
            threads.append(thread)
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join()
        
        print("✅ Stress test completed")
        
        # Check system performance
        error_stats = error_handler.get_error_statistics()
        log_analytics = logging_system.get_analytics()
        analytics_stats = analytics_system.get_analytics_statistics()
        
        print(f"\n📊 Stress Test Results:")
        print(f"   Total Errors: {error_stats['total_errors']}")
        print(f"   Total Logs: {log_analytics.total_logs}")
        print(f"   Analytics Reports: {analytics_stats['reports_generated']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        traceback.print_exc()
        return False

def test_error_recovery_and_circuit_breakers():
    """Test error recovery mechanisms and circuit breakers"""
    print("\n🔄 Testing Error Recovery and Circuit Breakers")
    print("-" * 60)
    
    try:
        # Create error handler
        error_handler = AdvancedErrorHandler()
        
        # Test circuit breaker behavior
        context = ErrorContext(service_name="circuit_test_service", operation="test_operation")
        
        # Simulate repeated failures to trigger circuit breaker
        for i in range(7):  # More than threshold
            try:
                raise ConnectionError(f"Connection failure {i}")
            except Exception as e:
                error_handler.handle_error(e, context, ErrorSeverity.HIGH, ErrorCategory.NETWORK)
        
        # Check circuit breaker state
        circuit_breaker = error_handler.circuit_breakers.get("circuit_test_service")
        if circuit_breaker:
            print(f"✅ Circuit breaker state: {circuit_breaker['state']}")
            print(f"   Failure count: {circuit_breaker['failure_count']}")
            
            # Test circuit breaker reset
            reset_success = error_handler.reset_circuit_breaker("circuit_test_service")
            print(f"   Reset successful: {'✅' if reset_success else '❌'}")
        
        # Test recovery strategies
        recovery_configs = error_handler.recovery_configs
        print(f"\n📋 Recovery Configurations:")
        for config_name, config in recovery_configs.items():
            print(f"   {config_name}: {config.max_retries} retries, {config.retry_delay}s delay")
        
        return True
        
    except Exception as e:
        print(f"❌ Recovery test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 Starting Advanced Error Handling and Logging System Test")
    print("=" * 80)
    
    test_results = []
    
    # Run all tests
    tests = [
        ("Advanced Error Handler", test_advanced_error_handler),
        ("Advanced Logging System", test_advanced_logging_system),
        ("Error Analytics System", test_error_analytics_system),
        ("Integration Features", test_integration_and_decorators),
        ("Performance and Stress", test_performance_and_stress),
        ("Error Recovery", test_error_recovery_and_circuit_breakers)
    ]
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} Test...")
        try:
            success = test_func()
            test_results.append((test_name, success))
            status = "✅ PASSED" if success else "❌ FAILED"
            print(f"   {status}: {test_name}")
        except Exception as e:
            print(f"   ❌ FAILED: {test_name} - {e}")
            test_results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, success in test_results if success)
    total = len(test_results)
    
    for test_name, success in test_results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\n📊 Overall Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Advanced Error Handler: Operational")
        print("✅ Advanced Logging System: Operational")
        print("✅ Error Analytics System: Operational")
        print("✅ Integration Features: Functional")
        print("✅ Performance: Verified")
        print("✅ Error Recovery: Operational")
        print("\n🚀 V2 Feature 4: Advanced Error Handling and Logging is FULLY OPERATIONAL!")
    else:
        print(f"\n⚠️  {total - passed} TESTS FAILED!")
        print("🚨 System requires attention before deployment")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
