"""
Service Integration Testing
==========================

Unified service integration testing for V2 services.
Consolidates service testing logic from integration framework.
Target: ≤300 LOC for V2 standards compliance.
"""

import os
import sys
import json
import time
import logging
import asyncio

from src.utils.stability_improvements import stability_manager, safe_import
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union, Callable, Coroutine, Type
from pathlib import Path
from datetime import datetime, timedelta
import traceback
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ServiceStatus(Enum):
    """Service status values."""
    UNKNOWN = "unknown"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


class CommunicationProtocol(Enum):
    """Communication protocol types."""
    HTTP = "http"
    HTTPS = "https"
    GRPC = "grpc"
    WEBSOCKET = "websocket"
    TCP = "tcp"
    UDP = "udp"
    INTERNAL = "internal"


@dataclass
class ServiceEndpoint:
    """Service endpoint information."""
    service_id: str
    name: str
    protocol: CommunicationProtocol
    host: str
    port: int
    path: str = "/"
    timeout: float = 30.0
    retry_count: int = 3
    health_check_enabled: bool = True
    last_health_check: Optional[float] = None
    status: ServiceStatus = ServiceStatus.UNKNOWN


@dataclass
class ServiceTestResult:
    """Result of a service test."""
    test_id: str
    service_id: str
    test_name: str
    status: str
    start_time: float
    end_time: float
    duration: float
    error_message: Optional[str] = None
    metrics: Dict[str, Any] = field(default_factory=dict)
    response_data: Optional[Dict[str, Any]] = None


class MockServiceProvider:
    """Provides mock services for testing."""
    
    def __init__(self):
        self.mock_services: Dict[str, Any] = {}
        self._setup_default_mocks()
    
    def _setup_default_mocks(self):
        """Setup default mock services."""
        self.mock_services["core_coordinator"] = self._create_core_coordinator_mock()
        self.mock_services["api_gateway"] = self._create_api_gateway_mock()
        self.mock_services["service_discovery"] = self._create_service_discovery_mock()
        self.mock_services["integration_monitoring"] = self._create_integration_monitoring_mock()
    
    def _create_core_coordinator_mock(self):
        """Create mock core coordinator service."""
        mock = type('MockCoreCoordinator', (), {})()
        mock.service_id = "core_coordinator"
        mock.name = "Core Coordinator Service"
        mock.status = ServiceStatus.RUNNING
        mock.get_status = lambda: {"status": "running", "health": "healthy"}
        mock.coordinate_services = lambda services: {"result": "success", "services": services}
        return mock
    
    def _create_api_gateway_mock(self):
        """Create mock API gateway service."""
        mock = type('MockAPIGateway', (), {})()
        mock.service_id = "api_gateway"
        mock.name = "V2 API Gateway"
        mock.status = ServiceStatus.RUNNING
        mock.get_status = lambda: {"status": "running", "endpoints": ["/api/v1", "/api/v2"]}
        mock.route_request = lambda path, method: {"result": "success", "path": path, "method": method}
        return mock
    
    def _create_service_discovery_mock(self):
        """Create mock service discovery service."""
        mock = type('MockServiceDiscovery', (), {})()
        mock.service_id = "service_discovery"
        mock.name = "V2 Service Discovery"
        mock.status = ServiceStatus.RUNNING
        mock.get_status = lambda: {"status": "running", "discovered_services": 15}
        mock.discover_services = lambda: ["service1", "service2", "service3"]
        return mock
    
    def _create_integration_monitoring_mock(self):
        """Create mock integration monitoring service."""
        mock = type('MockIntegrationMonitoring', (), {})()
        mock.service_id = "integration_monitoring"
        mock.name = "V2 Integration Monitoring"
        mock.status = ServiceStatus.RUNNING
        mock.get_status = lambda: {"status": "running", "monitored_integrations": 8}
        mock.monitor_integration = lambda integration_id: {"result": "success", "integration_id": integration_id}
        return mock
    
    def get_mock_service(self, service_id: str) -> Optional[Any]:
        """Get a mock service by ID."""
        return self.mock_services.get(service_id)
    
    def register_mock_service(self, service_id: str, mock_service: Any) -> bool:
        """Register a custom mock service."""
        try:
            self.mock_services[service_id] = mock_service
            logger.info(f"Registered mock service: {service_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to register mock service: {e}")
            return False


class CommunicationValidator:
    """Validates service communication."""
    
    def __init__(self):
        self.validation_rules: Dict[str, Callable] = {}
        self._setup_default_rules()
    
    def _setup_default_rules(self):
        """Setup default validation rules."""
        self.validation_rules["response_time"] = self._validate_response_time
        self.validation_rules["status_code"] = self._validate_status_code
        self.validation_rules["response_format"] = self._validate_response_format
        self.validation_rules["error_handling"] = self._validate_error_handling
    
    def validate_communication(self, service_id: str, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate service communication."""
        validation_results = {}
        
        for rule_name, rule_func in self.validation_rules.items():
            try:
                result = rule_func(test_data)
                validation_results[rule_name] = result
            except Exception as e:
                validation_results[rule_name] = {"valid": False, "error": str(e)}
        
        return validation_results
    
    def _validate_response_time(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        response_time = test_data.get("response_time", 0)
        max_acceptable_time = test_data.get("max_response_time", 5.0)
        return {
            "valid": response_time <= max_acceptable_time,
            "actual_time": response_time,
            "max_acceptable": max_acceptable_time,
            "message": f"Response time: {response_time:.2f}s (max: {max_acceptable_time}s)"
        }
    
    def _validate_status_code(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        status_code = test_data.get("status_code", 0)
        expected_codes = test_data.get("expected_status_codes", [200, 201])
        return {
            "valid": status_code in expected_codes,
            "actual_code": status_code,
            "expected_codes": expected_codes,
            "message": f"Status code: {status_code} (expected: {expected_codes})"
        }
    
    def _validate_response_format(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        response_data = test_data.get("response_data", {})
        expected_keys = test_data.get("expected_keys", [])
        if not expected_keys:
            return {"valid": True, "message": "No format validation required"}
        missing_keys = [key for key in expected_keys if key not in response_data]
        return {
            "valid": len(missing_keys) == 0,
            "missing_keys": missing_keys,
            "expected_keys": expected_keys,
            "message": f"Format validation: {'✓' if len(missing_keys) == 0 else '✗'}"
        }
    
    def _validate_error_handling(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        error_occurred = test_data.get("error_occurred", False)
        expected_error = test_data.get("expected_error", False)
        error_message = test_data.get("error_message", "")
        if expected_error and not error_occurred:
            return {"valid": False, "message": "Expected error did not occur"}
        elif not expected_error and error_occurred:
            return {"valid": False, "message": f"Unexpected error: {error_message}"}
        else:
            return {"valid": True, "message": "Error handling validation passed"}


class DataFlowTester:
    """Tests data flow between services."""
    
    def __init__(self):
        self.flow_validators: Dict[str, Callable] = {}
        self._setup_default_validators()
    
    def _setup_default_validators(self):
        """Setup default data flow validators."""
        self.flow_validators["data_integrity"] = self._validate_data_integrity
        self.flow_validators["data_transformation"] = self._validate_data_transformation
        self.flow_validators["data_routing"] = self._validate_data_routing
    
    def test_data_flow(self, flow_id: str, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Test data flow between services."""
        flow_results = {}
        
        for validator_name, validator_func in self.flow_validators.items():
            try:
                result = validator_func(test_data)
                flow_results[validator_name] = result
            except Exception as e:
                flow_results[validator_name] = {"valid": False, "error": str(e)}
        
        return flow_results
    
    def _validate_data_integrity(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data = test_data.get("input_data", {})
        output_data = test_data.get("output_data", {})
        if not input_data or not output_data:
            return {"valid": False, "message": "Missing input or output data"}
        input_keys, output_keys = set(input_data.keys()), set(output_data.keys())
        lost_keys, added_keys = input_keys - output_keys, output_keys - input_keys
        return {
            "valid": len(lost_keys) == 0,
            "lost_keys": list(lost_keys),
            "added_keys": list(added_keys),
            "message": f"Data integrity: {'✓' if len(lost_keys) == 0 else '✗'}"
        }
    
    def _validate_data_transformation(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        transformation_rules = test_data.get("transformation_rules", {})
        actual_transformations = test_data.get("actual_transformations", {})
        if not transformation_rules:
            return {"valid": True, "message": "No transformation rules specified"}
        validation_results = {rule_name: {"valid": actual_transformations.get(rule_name) == expected_result, "expected": expected_result, "actual": actual_transformations.get(rule_name)} for rule_name, expected_result in transformation_rules.items()}
        all_valid = all(result["valid"] for result in validation_results.values())
        return {"valid": all_valid, "transformations": validation_results, "message": f"Data transformation: {'✓' if all_valid else '✗'}"}
    
    def _validate_data_routing(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        expected_routes = test_data.get("expected_routes", [])
        actual_routes = test_data.get("actual_routes", [])
        if not expected_routes:
            return {"valid": True, "message": "No routing validation required"}
        missing_routes = [route for route in expected_routes if route not in actual_routes]
        unexpected_routes = [route for route in actual_routes if route not in expected_routes]
        return {"valid": len(missing_routes) == 0 and len(unexpected_routes) == 0, "missing_routes": missing_routes, "unexpected_routes": unexpected_routes, "message": f"Data routing: {'✓' if len(missing_routes) == 0 else '✗'}"}


class ServiceIntegrationTester:
    """Main service integration testing class."""
    
    def __init__(self):
        self.mock_provider = MockServiceProvider()
        self.communication_validator = CommunicationValidator()
        self.data_flow_tester = DataFlowTester()
        self.test_results: List[ServiceTestResult] = []
    
    def test_service_communication(self, service_id: str, test_config: Dict[str, Any]) -> ServiceTestResult:
        """Test service communication."""
        start_time = time.time()
        test_id = f"comm_test_{int(start_time)}"
        
        try:
            # Get mock service
            mock_service = self.mock_provider.get_mock_service(service_id)
            if not mock_service:
                raise ValueError(f"Mock service not found: {service_id}")
            
            # Test communication
            test_data = self._execute_communication_test(mock_service, test_config)
            
            # Validate communication
            validation_results = self.communication_validator.validate_communication(service_id, test_data)
            
            # Create test result
            end_time = time.time()
            result = ServiceTestResult(
                test_id=test_id,
                service_id=service_id,
                test_name=f"Communication Test - {service_id}",
                status="passed" if all(v.get("valid", False) for v in validation_results.values()) else "failed",
                start_time=start_time,
                end_time=end_time,
                duration=end_time - start_time,
                metrics=validation_results,
                response_data=test_data
            )
            
            self.test_results.append(result)
            return result
            
        except Exception as e:
            end_time = time.time()
            result = ServiceTestResult(
                test_id=test_id,
                service_id=service_id,
                test_name=f"Communication Test - {service_id}",
                status="error",
                start_time=start_time,
                end_time=end_time,
                duration=end_time - start_time,
                error_message=str(e)
            )
            
            self.test_results.append(result)
            return result
    
    def test_data_flow(self, flow_id: str, test_config: Dict[str, Any]) -> Dict[str, Any]:
        """Test data flow between services."""
        return self.data_flow_tester.test_data_flow(flow_id, test_config)
    
    def _execute_communication_test(self, mock_service: Any, test_config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a communication test with mock service."""
        test_data = {
            "response_time": 0.1,  # Mock response time
            "status_code": 200,
            "response_data": {},
            "error_occurred": False,
            "max_response_time": test_config.get("max_response_time", 5.0),
            "expected_status_codes": test_config.get("expected_status_codes", [200, 201]),
            "expected_keys": test_config.get("expected_keys", [])
        }
        
        # Simulate service call
        try:
            if hasattr(mock_service, 'get_status'):
                result = mock_service.get_status()
                test_data["response_data"] = result
                test_data["expected_keys"] = list(result.keys()) if isinstance(result, dict) else []
        except Exception as e:
            test_data["error_occurred"] = True
            test_data["error_message"] = str(e)
        
        return test_data
    
    def get_test_results(self) -> List[ServiceTestResult]:
        """Get all test results."""
        return self.test_results
    
    def get_test_summary(self) -> Dict[str, Any]:
        """Get summary of test results."""
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r.status == "passed"])
        failed_tests = len([r for r in self.test_results if r.status == "failed"])
        error_tests = len([r for r in self.test_results if r.status == "error"])
        
        return {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "errors": error_tests,
            "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0
        }
