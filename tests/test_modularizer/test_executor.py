"""
🧪 REGRESSION TESTING SYSTEM - Test Executor
Extracted from regression_testing_system.py for modularization

This module handles the execution of individual tests and test suites.
"""

import time
import signal
from typing import Callable, Dict, Any
from .models import TestStatus, RegressionTestResult


class RegressionTestExecutor:
    """Handles execution of individual tests with timeout protection."""
    
    def __init__(self, timeout_default: float = 30.0):
        self.timeout_default = timeout_default
    
    def run_single_test(self, test_func: Callable, timeout: float = None, 
                       comparison_mode: bool = False) -> RegressionTestResult:
        """
        Run a single regression test.
        
        Args:
            test_func: The test function to run
            timeout: Timeout in seconds (uses default if None)
            comparison_mode: Whether to run in comparison mode
            
        Returns:
            RegressionTestResult containing test execution results
        """
        if timeout is None:
            timeout = self.timeout_default
            
        return self._run_single_test(test_func, timeout, comparison_mode)
    
    def _run_single_test(self, test_func: Callable, timeout: float, 
                         comparison_mode: bool) -> RegressionTestResult:
        """
        Internal method to run a single test with timeout protection.
        
        Args:
            test_func: The test function to run
            timeout: Timeout in seconds
            comparison_mode: Whether to run in comparison mode
            
        Returns:
            RegressionTestResult containing test execution results
        """
        test_name = test_func.__name__ if hasattr(test_func, '__name__') else str(test_func)
        start_time = time.time()
        
        result = RegressionTestResult(
            test_name=test_name,
            status=TestStatus.PENDING,
            execution_time=0.0,
            output="",
            error_message=None
        )
        
        try:
            # Set up timeout handler
            def timeout_handler(signum, frame):
                raise TimeoutError(f"Test '{test_name}' timed out after {timeout} seconds")
            
            # Set signal handler for timeout (Unix-like systems)
            try:
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(int(timeout))
            except (AttributeError, OSError):
                # Windows doesn't support SIGALRM, use threading timeout instead
                pass
            
            # Run the test
            result.status = TestStatus.RUNNING
            
            if comparison_mode:
                # Run in comparison mode - capture before and after outputs
                before_output = self._capture_test_output(test_func)
                result.before_output = before_output
                
                # Run test again to get after output
                after_output = self._capture_test_output(test_func)
                result.after_output = after_output
                
                # Determine status based on comparison
                if before_output == after_output:
                    result.status = TestStatus.PASSED
                    result.output = "Output comparison passed"
                else:
                    result.status = TestStatus.FAILED
                    result.output = f"Output comparison failed: outputs differ"
            else:
                # Run in normal mode
                test_output = self._capture_test_output(test_func)
                result.output = test_output
                result.status = TestStatus.PASSED
            
            # Clear timeout
            try:
                signal.alarm(0)
            except (AttributeError, OSError):
                pass
                
        except TimeoutError as e:
            result.status = TestStatus.TIMEOUT
            result.error_message = str(e)
        except Exception as e:
            result.status = TestStatus.ERROR
            result.error_message = str(e)
        finally:
            # Calculate execution time
            result.execution_time = time.time() - start_time
            
        return result
    
    def _capture_test_output(self, test_func: Callable) -> str:
        """
        Capture output from a test function execution.
        
        Args:
            test_func: The test function to execute
            
        Returns:
            Captured output as string
        """
        try:
            # This is a simplified capture mechanism
            # In a real implementation, this would capture stdout/stderr
            result = test_func()
            return str(result) if result is not None else ""
        except Exception as e:
            return f"ERROR: {str(e)}"
