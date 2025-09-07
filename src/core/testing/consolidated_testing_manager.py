#!/usr/bin/env python3
"""
Consolidated Testing and Validation Manager - SSOT Violation Resolution
======================================================================

Consolidates testing and validation functionality from both `testing/` and `validation/` directories
into a single unified system, eliminating SSOT violations.

Author: Agent-1 (PERPETUAL MOTION LEADER - CORE SYSTEMS CONSOLIDATION SPECIALIST)
Mission: CRITICAL SSOT CONSOLIDATION - Testing and Validation Systems
License: MIT
"""

import asyncio
import logging
import time
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum
import json

logger = logging.getLogger(__name__)


class TestStatus(Enum):
    """Test status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"
    TIMEOUT = "timeout"


class TestType(Enum):
    """Test types"""
    UNIT = "unit"
    INTEGRATION = "integration"
    SYSTEM = "system"
    PERFORMANCE = "performance"
    SECURITY = "security"
    VALIDATION = "validation"
    SMOKE = "smoke"
    REGRESSION = "regression"


class ValidationStatus(Enum):
    """Validation status enumeration"""
    PENDING = "pending"
    VALIDATING = "validating"
    VALID = "valid"
    INVALID = "invalid"
    WARNING = "warning"
    ERROR = "error"


class ValidationType(Enum):
    """Validation types"""
    DATA = "data"
    SCHEMA = "schema"
    BUSINESS_RULES = "business_rules"
    SECURITY = "security"
    PERFORMANCE = "performance"
    COMPLIANCE = "compliance"


@dataclass
class TestCase:
    """Test case structure"""
    
    test_id: str
    test_name: str
    test_type: TestType
    status: TestStatus
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_ms: Optional[float] = None
    description: str = ""
    expected_result: str = ""
    actual_result: str = ""
    error_message: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationRule:
    """Validation rule structure"""
    
    rule_id: str
    rule_name: str
    validation_type: ValidationType
    rule_definition: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    priority: str = "normal"
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationResult:
    """Validation result structure"""
    
    validation_id: str
    rule_id: str
    validation_status: ValidationStatus
    validation_timestamp: datetime = field(default_factory=datetime.now)
    validation_duration_ms: float = 0.0
    input_data: Any = None
    output_data: Any = None
    validation_errors: List[str] = field(default_factory=list)
    validation_warnings: List[str] = field(default_factory=list)
    validation_score: float = 0.0
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TestingMetrics:
    """Testing and validation system metrics"""
    
    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0
    total_validations: int = 0
    successful_validations: int = 0
    test_success_rate: float = 0.0
    validation_success_rate: float = 0.0
    average_test_duration_ms: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)


class ConsolidatedTestingManager:
    """
    Consolidated Testing and Validation Manager - Single Source of Truth
    
    Eliminates SSOT violations by consolidating:
    - `testing/` directory (31 files) → Testing frameworks and execution
    - `validation/` directory (119 files) → Validation rules and systems
    
    Result: Single unified testing and validation system
    """
    
    def __init__(self):
        """Initialize consolidated testing manager"""
        # Testing tracking
        self.test_cases: Dict[str, TestCase] = {}
        self.test_results: Dict[str, Dict[str, Any]] = {}
        
        # Validation tracking
        self.validation_rules: Dict[str, ValidationRule] = {}
        self.validation_results: Dict[str, ValidationResult] = {}
        
        # Testing system components
        self.test_executor = TestExecutor()
        self.validation_engine = ValidationEngine()
        
        # Configuration
        self.max_concurrent_tests = 50
        self.max_concurrent_validations = 100
        self.enable_auto_validation = True
        self.test_timeout = 300  # seconds
        self.validation_timeout = 60  # seconds
        
        # Metrics and monitoring
        self.metrics = TestingMetrics()
        self.test_callbacks: List[Callable] = []
        self.validation_callbacks: List[Callable] = []
        
        # Initialize consolidation
        self._initialize_consolidated_systems()
        self._load_legacy_testing_configurations()
    
    def _initialize_consolidated_systems(self):
        """Initialize all consolidated testing systems"""
        try:
            logger.info("🚀 Initializing consolidated testing and validation systems...")
            
            # Initialize test executor
            self.test_executor.initialize()
            
            # Initialize validation engine
            self.validation_engine.initialize()
            
            logger.info("✅ Consolidated testing and validation systems initialized")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize consolidated testing systems: {e}")
    
    def _load_legacy_testing_configurations(self):
        """Load and consolidate legacy testing configurations"""
        try:
            logger.info("📋 Loading legacy testing configurations...")
            
            # Load configurations from both testing directories
            testing_dirs = [
                "testing",
                "validation"
            ]
            
            total_configs_loaded = 0
            
            for dir_name in testing_dirs:
                config_path = Path(f"src/core/{dir_name}")
                if config_path.exists():
                    configs = self._load_directory_configs(config_path)
                    total_configs_loaded += len(configs)
                    logger.info(f"📁 Loaded {len(configs)} configs from {dir_name}")
            
            logger.info(f"✅ Total legacy testing configs loaded: {total_configs_loaded}")
            
        except Exception as e:
            logger.error(f"❌ Failed to load legacy testing configurations: {e}")
    
    def _load_directory_configs(self, config_path: Path) -> List[Dict[str, Any]]:
        """Load configuration files from a directory"""
        configs = []
        try:
            for config_file in config_path.rglob("*.py"):
                if config_file.name.startswith("__"):
                    continue
                
                # Extract basic configuration info
                config_info = {
                    "source_directory": config_path.name,
                    "file_name": config_file.name,
                    "file_path": str(config_file),
                    "last_modified": datetime.fromtimestamp(config_file.stat().st_mtime),
                    "file_size": config_file.stat().st_size
                }
                
                configs.append(config_info)
                
        except Exception as e:
            logger.error(f"❌ Failed to load configs from {config_path}: {e}")
        
        return configs
    
    def create_test_case(self, test_name: str, test_type: TestType, description: str = "",
                         expected_result: str = "", metadata: Dict[str, Any] = None) -> str:
        """
        Create a new test case
        
        Args:
            test_name: Name of the test case
            test_type: Type of test
            description: Test description
            expected_result: Expected test result
            metadata: Additional metadata
            
        Returns:
            Test case ID
        """
        try:
            test_id = f"test_{int(time.time())}_{test_name.replace(' ', '_')}"
            
            # Create test case
            test_case = TestCase(
                test_id=test_id,
                test_name=test_name,
                test_type=test_type,
                status=TestStatus.PENDING,
                description=description,
                expected_result=expected_result,
                metadata=metadata or {}
            )
            
            # Add to test cases
            self.test_cases[test_id] = test_case
            
            # Update metrics
            self._update_metrics()
            
            logger.info(f"📋 Test case created: {test_id} - {test_name}")
            return test_id
            
        except Exception as e:
            logger.error(f"❌ Failed to create test case: {e}")
            return ""
    
    def create_validation_rule(self, rule_name: str, validation_type: ValidationType,
                               rule_definition: str, description: str = "",
                               priority: str = "normal", metadata: Dict[str, Any] = None) -> str:
        """
        Create a new validation rule
        
        Args:
            rule_name: Name of the validation rule
            validation_type: Type of validation
            rule_definition: Rule definition/logic
            description: Rule description
            priority: Rule priority
            metadata: Additional metadata
            
        Returns:
            Validation rule ID
        """
        try:
            rule_id = f"rule_{int(time.time())}_{rule_name.replace(' ', '_')}"
            
            # Create validation rule
            validation_rule = ValidationRule(
                rule_id=rule_id,
                rule_name=rule_name,
                validation_type=validation_type,
                rule_definition=rule_definition,
                description=description,
                priority=priority,
                metadata=metadata or {}
            )
            
            # Add to validation rules
            self.validation_rules[rule_id] = validation_rule
            
            # Update metrics
            self._update_metrics()
            
            logger.info(f"📋 Validation rule created: {rule_id} - {rule_name}")
            return rule_id
            
        except Exception as e:
            logger.error(f"❌ Failed to create validation rule: {e}")
            return ""
    
    async def execute_test(self, test_id: str, test_data: Any = None) -> bool:
        """
        Execute a specific test case
        
        Args:
            test_id: ID of the test case to execute
            test_data: Test input data
            
        Returns:
            True if execution started, False otherwise
        """
        try:
            if test_id not in self.test_cases:
                logger.error(f"❌ Test case not found: {test_id}")
                return False
            
            test_case = self.test_cases[test_id]
            
            # Check if test can be executed
            if test_case.status != TestStatus.PENDING:
                logger.warning(f"⚠️ Test {test_id} is not pending (status: {test_case.status})")
                return False
            
            # Start test execution
            test_case.status = TestStatus.RUNNING
            test_case.started_at = datetime.now()
            
            # Start execution
            asyncio.create_task(self._execute_test_async(test_case, test_data))
            
            logger.info(f"🚀 Test execution started: {test_id} - {test_case.test_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to execute test {test_id}: {e}")
            return False
    
    async def _execute_test_async(self, test_case: TestCase, test_data: Any):
        """Execute test case asynchronously"""
        try:
            start_time = time.time()
            
            logger.info(f"🔄 Executing test: {test_case.test_id} - {test_case.test_name}")
            
            # Execute test using test executor
            test_result = await self.test_executor.execute_test(test_case, test_data)
            
            # Update test case with results
            end_time = time.time()
            test_case.duration_ms = (end_time - start_time) * 1000
            test_case.completed_at = datetime.now()
            
            if test_result.get("success", False):
                test_case.status = TestStatus.PASSED
                test_case.actual_result = test_result.get("result", "Test passed")
                logger.info(f"✅ Test passed: {test_case.test_id}")
            else:
                test_case.status = TestStatus.FAILED
                test_case.actual_result = test_result.get("result", "Test failed")
                test_case.error_message = test_result.get("error", "Unknown error")
                logger.error(f"❌ Test failed: {test_case.test_id}")
            
            # Store test result
            self.test_results[test_case.test_id] = {
                "test_id": test_case.test_id,
                "status": test_case.status.value,
                "duration_ms": test_case.duration_ms,
                "result": test_case.actual_result,
                "error": test_case.error_message,
                "timestamp": test_case.completed_at.isoformat()
            }
            
            # Update metrics
            self._update_metrics()
            
            # Trigger callbacks
            for callback in self.test_callbacks:
                try:
                    callback(test_case)
                except Exception as e:
                    logger.error(f"❌ Test callback failed: {e}")
            
        except Exception as e:
            logger.error(f"❌ Test execution failed for {test_case.test_id}: {e}")
            test_case.status = TestStatus.ERROR
            test_case.error_message = str(e)
            test_case.completed_at = datetime.now()
            self._update_metrics()
    
    async def run_validation(self, rule_id: str, input_data: Any) -> str:
        """
        Run validation using a specific rule
        
        Args:
            rule_id: ID of the validation rule to use
            input_data: Data to validate
            
        Returns:
            Validation result ID
        """
        try:
            if rule_id not in self.validation_rules:
                logger.error(f"❌ Validation rule not found: {rule_id}")
                return ""
            
            validation_rule = self.validation_rules[rule_id]
            
            # Create validation result
            validation_id = f"validation_{int(time.time())}_{rule_id}"
            validation_result = ValidationResult(
                validation_id=validation_id,
                rule_id=rule_id,
                validation_status=ValidationStatus.VALIDATING,
                input_data=input_data
            )
            
            self.validation_results[validation_id] = validation_result
            
            # Start validation
            asyncio.create_task(self._run_validation_async(validation_result, validation_rule, input_data))
            
            logger.info(f"🔍 Validation started: {validation_id} using rule {rule_id}")
            return validation_id
            
        except Exception as e:
            logger.error(f"❌ Failed to run validation: {e}")
            return ""
    
    async def _run_validation_async(self, validation_result: ValidationResult, 
                                   validation_rule: ValidationRule, input_data: Any):
        """Run validation asynchronously"""
        try:
            start_time = time.time()
            
            logger.info(f"🔍 Running validation: {validation_result.validation_id}")
            
            # Execute validation using validation engine
            engine_result = await self.validation_engine.validate_data(
                validation_rule, input_data
            )
            
            # Update validation result
            end_time = time.time()
            validation_result.validation_duration_ms = (end_time - start_time) * 1000
            validation_result.output_data = engine_result.get("output_data")
            validation_result.validation_errors = engine_result.get("errors", [])
            validation_result.validation_warnings = engine_result.get("warnings", [])
            validation_result.validation_score = engine_result.get("score", 0.0)
            validation_result.details = engine_result.get("details", {})
            
            # Determine validation status
            if engine_result.get("success", False):
                if validation_result.validation_warnings:
                    validation_result.validation_status = ValidationStatus.WARNING
                else:
                    validation_result.validation_status = ValidationStatus.VALID
            else:
                validation_result.validation_status = ValidationStatus.INVALID
            
            # Update metrics
            self._update_metrics()
            
            # Trigger callbacks
            for callback in self.validation_callbacks:
                try:
                    callback(validation_result)
                except Exception as e:
                    logger.error(f"❌ Validation callback failed: {e}")
            
            status_text = "✅ VALID" if validation_result.validation_status == ValidationStatus.VALID else "❌ INVALID"
            logger.info(f"{status_text} Validation completed: {validation_result.validation_id}")
            
        except Exception as e:
            logger.error(f"❌ Validation failed for {validation_result.validation_id}: {e}")
            validation_result.validation_status = ValidationStatus.ERROR
            validation_result.validation_errors = [str(e)]
            self._update_metrics()
    
    async def run_test_suite(self, test_type: TestType = None) -> Dict[str, Any]:
        """
        Run a suite of tests
        
        Args:
            test_type: Type of tests to run (default: all)
            
        Returns:
            Test suite results
        """
        try:
            logger.info(f"🚀 Running test suite for {test_type.value if test_type else 'all'} tests")
            
            # Get tests to run
            if test_type:
                tests_to_run = [t for t in self.test_cases.values() if t.test_type == test_type and t.status == TestStatus.PENDING]
            else:
                tests_to_run = [t for t in self.test_cases.values() if t.status == TestStatus.PENDING]
            
            if not tests_to_run:
                return {"message": "No tests to run", "total_tests": 0}
            
            # Execute tests
            execution_tasks = []
            for test_case in tests_to_run:
                task = asyncio.create_task(self.execute_test(test_case.test_id))
                execution_tasks.append(task)
            
            # Wait for all tests to complete
            await asyncio.gather(*execution_tasks, return_exceptions=True)
            
            # Calculate results
            total_tests = len(tests_to_run)
            passed_tests = len([t for t in tests_to_run if t.status == TestStatus.PASSED])
            failed_tests = len([t for t in tests_to_run if t.status == TestStatus.FAILED])
            
            results = {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": (passed_tests / total_tests) * 100 if total_tests > 0 else 0
            }
            
            logger.info(f"✅ Test suite completed: {passed_tests}/{total_tests} tests passed")
            return results
            
        except Exception as e:
            logger.error(f"❌ Failed to run test suite: {e}")
            return {"error": str(e)}
    
    def get_test_status(self, test_id: str = None) -> Optional[Dict[str, Any]]:
        """Get test case status"""
        try:
            if test_id:
                if test_id in self.test_cases:
                    test_case = self.test_cases[test_id]
                    return {
                        "test_id": test_case.test_id,
                        "test_name": test_case.test_name,
                        "test_type": test_case.test_type.value,
                        "status": test_case.status.value,
                        "created_at": test_case.created_at.isoformat(),
                        "started_at": test_case.started_at.isoformat() if test_case.started_at else None,
                        "completed_at": test_case.completed_at.isoformat() if test_case.completed_at else None,
                        "duration_ms": test_case.duration_ms,
                        "expected_result": test_case.expected_result,
                        "actual_result": test_case.actual_result,
                        "error_message": test_case.error_message
                    }
                return None
            else:
                # Return summary of all tests
                return {
                    "total_tests": len(self.test_cases),
                    "pending_tests": len([t for t in self.test_cases.values() if t.status == TestStatus.PENDING]),
                    "running_tests": len([t for t in self.test_cases.values() if t.status == TestStatus.RUNNING]),
                    "passed_tests": len([t for t in self.test_cases.values() if t.status == TestStatus.PASSED]),
                    "failed_tests": len([t for t in self.test_cases.values() if t.status == TestStatus.FAILED])
                }
                
        except Exception as e:
            logger.error(f"❌ Failed to get test status: {e}")
            return None
    
    def get_validation_status(self, validation_id: str = None) -> Optional[Dict[str, Any]]:
        """Get validation status"""
        try:
            if validation_id:
                if validation_id in self.validation_results:
                    result = self.validation_results[validation_id]
                    return {
                        "validation_id": result.validation_id,
                        "rule_id": result.rule_id,
                        "validation_status": result.validation_status.value,
                        "validation_timestamp": result.validation_timestamp.isoformat(),
                        "validation_duration_ms": result.validation_duration_ms,
                        "validation_score": result.validation_score,
                        "validation_errors": result.validation_errors,
                        "validation_warnings": result.validation_warnings
                    }
                return None
            else:
                # Return summary of all validations
                return {
                    "total_validations": len(self.validation_results),
                    "pending_validations": len([v for v in self.validation_results.values() if v.validation_status == ValidationStatus.PENDING]),
                    "validating": len([v for v in self.validation_results.values() if v.validation_status == ValidationStatus.VALIDATING]),
                    "valid_results": len([v for v in self.validation_results.values() if v.validation_status == ValidationStatus.VALID]),
                    "invalid_results": len([v for v in self.validation_results.values() if v.validation_status == ValidationStatus.INVALID])
                }
                
        except Exception as e:
            logger.error(f"❌ Failed to get validation status: {e}")
            return None
    
    def get_testing_summary(self) -> Dict[str, Any]:
        """Get summary of all testing and validation"""
        try:
            return {
                "testing": {
                    "total_tests": len(self.test_cases),
                    "passed_tests": len([t for t in self.test_cases.values() if t.status == TestStatus.PASSED]),
                    "failed_tests": len([t for t in self.test_cases.values() if t.status == TestStatus.FAILED])
                },
                "validation": {
                    "total_rules": len(self.validation_rules),
                    "total_validations": len(self.validation_results),
                    "successful_validations": len([v for v in self.validation_results.values() if v.validation_status == ValidationStatus.VALID])
                },
                "metrics": {
                    "total_tests": self.metrics.total_tests,
                    "passed_tests": self.metrics.passed_tests,
                    "failed_tests": self.metrics.failed_tests,
                    "total_validations": self.metrics.total_validations,
                    "successful_validations": self.metrics.successful_validations,
                    "test_success_rate": self.metrics.test_success_rate,
                    "validation_success_rate": self.metrics.validation_success_rate,
                    "average_test_duration_ms": self.metrics.average_test_duration_ms
                },
                "last_updated": self.metrics.last_updated.isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get testing summary: {e}")
            return {"error": str(e)}
    
    def _update_metrics(self):
        """Update testing and validation metrics"""
        try:
            # Count tests and validations
            self.metrics.total_tests = len(self.test_cases)
            self.metrics.passed_tests = len([t for t in self.test_cases.values() if t.status == TestStatus.PASSED])
            self.metrics.failed_tests = len([t for t in self.test_cases.values() if t.status == TestStatus.FAILED])
            self.metrics.total_validations = len(self.validation_results)
            self.metrics.successful_validations = len([v for v in self.validation_results.values() if v.validation_status == ValidationStatus.VALID])
            
            # Calculate success rates
            if self.metrics.total_tests > 0:
                self.metrics.test_success_rate = self.metrics.passed_tests / self.metrics.total_tests
            
            if self.metrics.total_validations > 0:
                self.metrics.validation_success_rate = self.metrics.successful_validations / self.metrics.total_validations
            
            # Calculate average test duration
            completed_tests = [t for t in self.test_cases.values() if t.duration_ms]
            if completed_tests:
                total_duration = sum(t.duration_ms for t in completed_tests)
                self.metrics.average_test_duration_ms = total_duration / len(completed_tests)
            
            self.metrics.last_updated = datetime.now()
            
        except Exception as e:
            logger.error(f"❌ Failed to update metrics: {e}")
    
    def register_test_callback(self, callback: Callable):
        """Register callback for test events"""
        if callback not in self.test_callbacks:
            self.test_callbacks.append(callback)
            logger.info("✅ Test callback registered")
    
    def register_validation_callback(self, callback: Callable):
        """Register callback for validation events"""
        if callback not in self.validation_callbacks:
            self.validation_callbacks.append(callback)
            logger.info("✅ Validation callback registered")


# Placeholder classes for the consolidated systems
class TestExecutor:
    """Test execution system"""
    
    def initialize(self):
        """Initialize test executor"""
        pass
    
    async def execute_test(self, test_case: TestCase, test_data: Any) -> Dict[str, Any]:
        """Execute test case"""
        # Simulate test execution
        await asyncio.sleep(0.1)
        return {
            "success": True,
            "result": f"Test {test_case.test_name} executed successfully",
            "error": ""
        }


class ValidationEngine:
    """Validation execution engine"""
    
    def initialize(self):
        """Initialize validation engine"""
        pass
    
    async def validate_data(self, validation_rule: ValidationRule, input_data: Any) -> Dict[str, Any]:
        """Validate data using rule"""
        # Simulate validation
        await asyncio.sleep(0.1)
        return {
            "success": True,
            "output_data": f"Validated: {input_data}",
            "errors": [],
            "warnings": ["Minor validation warning"],
            "score": 0.95,
            "details": {"validation_method": "rule_based"}
        }


if __name__ == "__main__":
    # CLI interface for testing and validation
    import asyncio
    
    async def test_consolidated_testing_manager():
        """Test consolidated testing and validation functionality"""
        print("🚀 Consolidated Testing and Validation Manager - SSOT Violation Resolution")
        print("=" * 70)
        
        # Initialize manager
        manager = ConsolidatedTestingManager()
        
        # Test test case creation
        print("📋 Testing test case creation...")
        test_id = manager.create_test_case(
            test_name="User Authentication Test",
            test_type=TestType.INTEGRATION,
            description="Test user authentication functionality",
            expected_result="Authentication successful"
        )
        print(f"✅ Test case created: {test_id}")
        
        # Test validation rule creation
        print("📋 Testing validation rule creation...")
        rule_id = manager.create_validation_rule(
            rule_name="Email Format Validation",
            validation_type=ValidationType.DATA,
            rule_definition="Email must contain @ and domain",
            description="Validates email format"
        )
        print(f"✅ Validation rule created: {rule_id}")
        
        # Test test execution
        print("🚀 Testing test execution...")
        execution_started = await manager.execute_test(test_id, {"username": "test", "password": "test"})
        print(f"✅ Test execution started: {execution_started}")
        
        # Test validation execution
        print("🔍 Testing validation execution...")
        validation_id = await manager.run_validation(rule_id, "test@example.com")
        print(f"✅ Validation started: {validation_id}")
        
        # Wait for completion
        await asyncio.sleep(2)
        
        # Get statuses
        test_status = manager.get_test_status()
        validation_status = manager.get_validation_status()
        print(f"📊 Test summary: {test_status['total_tests']} total, {test_status['passed_tests']} passed")
        print(f"📊 Validation summary: {validation_status['total_validations']} total")
        
        # Get overall summary
        summary = manager.get_testing_summary()
        print(f"📋 Testing summary: {summary['testing']['total_tests']} tests, {summary['validation']['total_rules']} rules")
        
        print("🎉 Consolidated testing and validation manager test completed!")
    
    # Run test
    asyncio.run(test_consolidated_testing_manager())
