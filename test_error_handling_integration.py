#!/usr/bin/env python3
"""
Integration test for error handling modules.
"""

import sys

sys.path.append('src')

def test_integration():
    """Test integrated error handling system."""
    try:
        from core.error_handling.coordination_error_handler import CoordinationErrorHandler
        from core.error_handling.error_recovery import (
            ErrorRecoveryManager,
            ErrorSeverity,
            create_error_context,
        )

        print('🧪 Testing integrated error handling system...')

        # Test coordination handler
        coord_handler = CoordinationErrorHandler()

        # Test error recovery manager
        recovery_manager = ErrorRecoveryManager()

        # Test circuit breaker registration
        coord_handler.register_circuit_breaker('test_component', failure_threshold=3, recovery_timeout=10)
        print('✅ Circuit breaker registered successfully')

        # Test retry mechanism registration
        coord_handler.register_retry_mechanism('test_component', max_attempts=3, base_delay=0.1, max_delay=1.0)
        print('✅ Retry mechanism registered successfully')

        # Test system health report
        health_report = coord_handler.get_system_health_report()
        print(f'✅ System health: {health_report["status"]}')

        # Test component status
        component_status = coord_handler.get_component_status('test_component')
        print(f'✅ Component status: {component_status["status"]}')

        # Test recovery statistics
        recovery_stats = recovery_manager.get_recovery_statistics()
        print(f'✅ Recovery success rate: {recovery_stats["success_rate"]}%')

        print('🎉 Integrated error handling system test completed successfully!')

        return True

    except Exception as e:
        print(f'❌ Integrated test failed: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_integration()
    sys.exit(0 if success else 1)
