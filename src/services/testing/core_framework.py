"""
Core Testing Framework
======================

Unified testing infrastructure for V2 services.
Consolidates core testing components from multiple massive files.
Target: ≤300 LOC for V2 standards compliance.
"""

import os
import sys
import json
import logging
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union, Callable, Coroutine, Type
from pathlib import Path
from datetime import datetime, timedelta
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestStatus(Enum):
    """Status of test execution."""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"
    ERROR = "error"


class TestType(Enum):
    """Types of integration tests."""
    UNIT = "unit"
    INTEGRATION = "integration"
    END_TO_END = "end_to_end"
    PERFORMANCE = "performance"
    LOAD = "load"
    STRESS = "stress"
    SECURITY = "security"
    COMPATIBILITY = "compatibility"


class TestPriority(Enum):
    """Test priority levels."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class TestConfig:
    """Configuration for testing framework."""
    test_timeout: float = 300.0
    max_retries: int = 3
    retry_delay: float = 2.0
    enable_logging: bool = True
    log_level: str = "INFO"
    log_file: Optional[str] = None
    enable_persistence: bool = True
    results_directory: str = "test_results"
    enable_parallel_execution: bool = False
    max_workers: int = 4


@dataclass
class TestResult:
    """Result of a test execution."""
    test_id: str
    test_name: str
    test_type: TestType
    status: TestStatus
    start_time: float
    end_time: float
    duration: float
    error_message: Optional[str] = None
    error_traceback: Optional[str] = None
    metrics: Dict[str, Any] = field(default_factory=dict)
    logs: List[str] = field(default_factory=list)
    assertions_passed: int = 0
    assertions_failed: int = 0
    test_data: Dict[str, Any] = field(default_factory=dict)


class TestLogger:
    """Unified logging system for testing framework."""
    
    def __init__(self, config: TestConfig):
        self.config = config
        self.logger = logging.getLogger("TestFramework")
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration."""
        if not self.config.enable_logging:
            return
        
        level = getattr(logging, self.config.log_level.upper(), logging.INFO)
        self.logger.setLevel(level)
        
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler if specified
        if self.config.log_file:
            file_handler = logging.FileHandler(self.config.log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def info(self, message: str):
        """Log info message."""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message."""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message."""
        self.logger.error(message)
    
    def debug(self, message: str):
        """Log debug message."""
        self.logger.debug(message)


class TestUtilities:
    """Common testing utilities."""
    
    @staticmethod
    def generate_test_id() -> str:
        """Generate unique test ID."""
        return str(uuid.uuid4())
    
    @staticmethod
    def get_timestamp() -> float:
        """Get current timestamp."""
        return time.time()
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """Format duration in human readable format."""
        if seconds < 60:
            return f"{seconds:.2f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}m"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}h"
    
    @staticmethod
    def safe_json_dumps(data: Any) -> str:
        """Safely convert data to JSON string."""
        try:
            return json.dumps(data, default=str, indent=2)
        except Exception:
            return str(data)
    
    @staticmethod
    def create_directory(path: str) -> bool:
        """Create directory if it doesn't exist."""
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Failed to create directory {path}: {e}")
            return False


class TestFramework(ABC):
    """Base testing framework class."""
    
    def __init__(self, config: TestConfig):
        self.config = config
        self.logger = TestLogger(config)
        self.results: List[TestResult] = []
        self.current_test: Optional[TestResult] = None
    
    def setup(self):
        """Setup testing framework."""
        self.logger.info("Setting up testing framework")
        if self.config.enable_persistence:
            TestUtilities.create_directory(self.config.results_directory)
    
    def teardown(self):
        """Teardown testing framework."""
        self.logger.info("Tearing down testing framework")
        if self.config.enable_persistence:
            self._save_results()
    
    def _save_results(self):
        """Save test results to file."""
        try:
            results_file = Path(self.config.results_directory) / f"test_results_{int(time.time())}.json"
            results_data = [result.__dict__ for result in self.results]
            with open(results_file, 'w') as f:
                json.dump(results_data, f, default=str, indent=2)
            self.logger.info(f"Results saved to {results_file}")
        except Exception as e:
            self.logger.error(f"Failed to save results: {e}")
    
    @abstractmethod
    def run_test(self, test_name: str, test_func: Callable, **kwargs) -> TestResult:
        """Run a single test."""
        pass
    
    def get_results_summary(self) -> Dict[str, Any]:
        """Get summary of test results."""
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r.status == TestStatus.PASSED])
        failed_tests = len([r for r in self.results if r.status == TestStatus.FAILED])
        skipped_tests = len([r for r in self.results if r.status == TestStatus.SKIPPED])
        
        return {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "skipped": skipped_tests,
            "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "total_duration": sum(r.duration for r in self.results)
        }

