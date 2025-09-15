#!/usr/bin/env python3
"""
Integration Testing Framework Core - V2 Compliant
================================================

Core testing framework components for integration testing.
V2 Compliance: < 400 lines, single responsibility.

Author: Agent-5 (Data Organization Specialist)
Test Type: Integration Testing Framework Core
"""

import json
import traceback
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class TestStatus(Enum):
    """Test execution status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"
    SKIPPED = "skipped"


class TestType(Enum):
    """Test type classification."""
    UNIT = "unit"
    INTEGRATION = "integration"
    API = "api"
    E2E = "e2e"
    PERFORMANCE = "performance"
    SECURITY = "security"
    DEPLOYMENT = "deployment"


@dataclass
class TestResult:
    """Comprehensive test result data structure."""
    test_id: str
    test_name: str
    test_type: TestType
    status: TestStatus
    duration: float
    start_time: datetime
    end_time: datetime | None = None
    error_message: str | None = None
    stack_trace: str | None = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    assertions: List[Dict[str, Any]] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)


@dataclass
class TestSuite:
    """Test suite configuration and execution management."""
    suite_id: str
    name: str
    description: str
    test_type: TestType
    tests: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    environment: Dict[str, Any] = field(default_factory=dict)
    timeout: int = 300  # 5 minutes default
    parallel_execution: bool = False
    retry_count: int = 0


class IntegrationTestFramework:
    """Core integration testing framework."""
    
    def __init__(self, base_url: str = "http://localhost:8000", api_version: str = "v2"):
        self.base_url = base_url.rstrip("/")
        self.api_version = api_version
        self.api_base_url = f"{self.base_url}/{api_version}"
        
        # Test execution tracking
        self.test_results: List[TestResult] = []
        self.test_suites: Dict[str, TestSuite] = {}
        self.execution_context: Dict[str, Any] = {}
        
        # HTTP client with retry logic
        self.session = self._create_http_session()
        
        # Load OpenAPI specification
        self.openapi_spec = self._load_openapi_spec()
    
    def _create_http_session(self) -> requests.Session:
        """Create HTTP session with retry logic and proper configuration."""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            backoff_factor=1,
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set default headers
        session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Swarm-Integration-Test-Framework/2.0.0"
        })
        
        return session
    
    def _load_openapi_spec(self) -> Dict[str, Any]:
        """Load OpenAPI specification for API validation."""
        spec_path = Path("docs/openapi.yaml")
        if not spec_path.exists():
            print(f"Warning: OpenAPI spec not found at {spec_path}")
            return {}
        
        try:
            import yaml
            with open(spec_path, encoding="utf-8") as f:
                return yaml.safe_load(f)
        except ImportError:
            print("Warning: PyYAML not available for OpenAPI spec loading")
            return {}
        except Exception as e:
            print(f"Warning: Failed to load OpenAPI spec: {e}")
            return {}
    
    def register_test_suite(self, suite: TestSuite) -> None:
        """Register a test suite for execution."""
        self.test_suites[suite.suite_id] = suite
        print(f"Registered test suite: {suite.name} ({suite.suite_id})")
    
    def execute_test_suite(self, suite_id: str) -> List[TestResult]:
        """Execute a registered test suite."""
        if suite_id not in self.test_suites:
            raise ValueError(f"Test suite {suite_id} not found")
        
        suite = self.test_suites[suite_id]
        print(f"Executing test suite: {suite.name}")
        
        results = []
        
        # Execute tests (in parallel if configured)
        if suite.parallel_execution:
            # Parallel execution would require asyncio/threading implementation
            pass
        else:
            for test_id in suite.tests:
                result = self._execute_test(test_id, suite)
                results.append(result)
        
        return results
    
    def _execute_test(self, test_id: str, suite: TestSuite) -> TestResult:
        """Execute a single test within a suite."""
        result = TestResult(
            test_id=test_id,
            test_name=f"{suite.name}::{test_id}",
            test_type=suite.test_type,
            status=TestStatus.RUNNING,
            start_time=datetime.now(),
            duration=0.0
        )
        
        try:
            # Execute the actual test logic
            if hasattr(self, f"test_{test_id}"):
                test_method = getattr(self, f"test_{test_id}")
                test_method(result)
                result.status = TestStatus.PASSED
            else:
                raise AttributeError(f"Test method test_{test_id} not found")
                
        except Exception as e:
            result.status = TestStatus.FAILED
            result.error_message = str(e)
            result.stack_trace = traceback.format_exc()
            
        finally:
            result.end_time = datetime.now()
            result.duration = (result.end_time - result.start_time).total_seconds()
        
        self.test_results.append(result)
        return result


# Convenience functions
def create_integration_framework(base_url: str = "http://localhost:8000") -> IntegrationTestFramework:
    """Factory function to create integration test framework instance."""
    return IntegrationTestFramework(base_url)


if __name__ == "__main__":
    # Example usage
    framework = IntegrationTestFramework()
    print("Integration Testing Framework Core initialized")
    print(f"Base URL: {framework.base_url}")
    print(f"API Base URL: {framework.api_base_url}")
