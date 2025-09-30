"""
Agent-7 & Agent-8 Phase 4 Testing Coordination Utils
Utility functions for testing coordination and validation
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from .agent7_agent8_phase4_testing_coordination_core import (
    CoordinationSession,
    CoordinationStatus,
    TestCase,
    TestPriority,
    TestStatus,
    TestSuite,
    TestingMetrics,
    TestingPhase
)


class TestingValidator:
    """Testing validation utilities"""
    
    @staticmethod
    def validate_test_case(test_case: TestCase) -> List[str]:
        """Validate test case"""
        issues = []
        
        if not test_case.test_id:
            issues.append("Test ID must be specified")
        
        if not test_case.name:
            issues.append("Test name must be specified")
        
        if not test_case.description:
            issues.append("Test description must be specified")
        
        if test_case.execution_time < 0:
            issues.append("Execution time cannot be negative")
        
        return issues
    
    @staticmethod
    def validate_test_suite(test_suite: TestSuite) -> List[str]:
        """Validate test suite"""
        issues = []
        
        if not test_suite.suite_id:
            issues.append("Suite ID must be specified")
        
        if not test_suite.name:
            issues.append("Suite name must be specified")
        
        if not test_suite.test_cases:
            issues.append("Test suite must contain test cases")
        
        if test_suite.pass_rate < 0 or test_suite.pass_rate > 100:
            issues.append("Pass rate must be between 0 and 100")
        
        return issues
    
    @staticmethod
    def validate_coordination_session(session: CoordinationSession) -> List[str]:
        """Validate coordination session"""
        issues = []
        
        if not session.session_id:
            issues.append("Session ID must be specified")
        
        if not session.agent7_tasks:
            issues.append("Agent-7 tasks must be specified")
        
        if not session.agent8_tasks:
            issues.append("Agent-8 tasks must be specified")
        
        if not session.shared_resources:
            issues.append("Shared resources must be specified")
        
        return issues


class TestingAnalyzer:
    """Testing analysis utilities"""
    
    @staticmethod
    def analyze_test_performance(test_cases: List[TestCase]) -> Dict[str, Any]:
        """Analyze test performance"""
        if not test_cases:
            return {"error": "No test cases to analyze"}
        
        total_time = sum(t.execution_time for t in test_cases)
        avg_time = total_time / len(test_cases)
        pass_rate = sum(1 for t in test_cases if t.status == TestStatus.PASSED) / len(test_cases)
        
        # Analyze by phase
        phase_stats = {}
        for phase in TestingPhase:
            phase_tests = [t for t in test_cases if t.testing_phase == phase]
            if phase_tests:
                phase_pass_rate = sum(1 for t in phase_tests if t.status == TestStatus.PASSED) / len(phase_tests)
                phase_stats[phase.value] = {
                    "count": len(phase_tests),
                    "pass_rate": phase_pass_rate,
                    "avg_time": sum(t.execution_time for t in phase_tests) / len(phase_tests)
                }
        
        return {
            "total_tests": len(test_cases),
            "total_execution_time": total_time,
            "average_execution_time": avg_time,
            "overall_pass_rate": pass_rate,
            "phase_statistics": phase_stats
        }
    
    @staticmethod
    def identify_bottlenecks(test_cases: List[TestCase]) -> List[str]:
        """Identify testing bottlenecks"""
        bottlenecks = []
        
        # Find slowest tests
        if test_cases:
            max_time = max(t.execution_time for t in test_cases)
            slow_tests = [t.name for t in test_cases if t.execution_time == max_time]
            if slow_tests:
                bottlenecks.append(f"Slowest tests: {', '.join(slow_tests)}")
        
        # Find failed tests
        failed_tests = [t.name for t in test_cases if t.status == TestStatus.FAILED]
        if failed_tests:
            bottlenecks.append(f"Failed tests: {', '.join(failed_tests)}")
        
        # Find high-priority failed tests
        critical_failed = [t.name for t in test_cases if t.status == TestStatus.FAILED and t.priority == TestPriority.CRITICAL]
        if critical_failed:
            bottlenecks.append(f"Critical failed tests: {', '.join(critical_failed)}")
        
        return bottlenecks
    
    @staticmethod
    def analyze_coordination_efficiency(sessions: List[CoordinationSession]) -> Dict[str, Any]:
        """Analyze coordination efficiency"""
        if not sessions:
            return {"error": "No coordination sessions to analyze"}
        
        completed_sessions = [s for s in sessions if s.status == CoordinationStatus.COMPLETED]
        if not completed_sessions:
            return {"error": "No completed coordination sessions"}
        
        avg_success_rate = sum(s.success_rate for s in completed_sessions) / len(completed_sessions)
        avg_duration = sum((s.end_time - s.start_time).total_seconds() for s in completed_sessions) / len(completed_sessions)
        
        return {
            "total_sessions": len(sessions),
            "completed_sessions": len(completed_sessions),
            "average_success_rate": avg_success_rate,
            "average_duration": avg_duration,
            "efficiency_grade": TestingAnalyzer._calculate_efficiency_grade(avg_success_rate)
        }
    
    @staticmethod
    def _calculate_efficiency_grade(success_rate: float) -> str:
        """Calculate efficiency grade"""
        if success_rate >= 90:
            return "A"
        elif success_rate >= 80:
            return "B"
        elif success_rate >= 70:
            return "C"
        elif success_rate >= 60:
            return "D"
        else:
            return "F"


class TestingReporter:
    """Testing reporting utilities"""
    
    @staticmethod
    def generate_test_report(metrics: TestingMetrics) -> str:
        """Generate test execution report"""
        return f"""
Phase 4 Testing Report
=====================
Total Tests: {metrics.total_tests}
Passed: {metrics.passed_tests}
Failed: {metrics.failed_tests}
Skipped: {metrics.skipped_tests}
Pass Rate: {metrics.pass_rate:.1f}%
Total Execution Time: {metrics.total_execution_time:.2f}s
Average Execution Time: {metrics.average_execution_time:.2f}s
Coordination Efficiency: {metrics.coordination_efficiency:.1f}%
"""
    
    @staticmethod
    def generate_coordination_report(sessions: List[CoordinationSession]) -> str:
        """Generate coordination report"""
        report = "Agent-7 & Agent-8 Coordination Report\n"
        report += "=====================================\n\n"
        
        for session in sessions:
            report += f"Session: {session.session_id}\n"
            report += f"Phase: {session.phase.value}\n"
            report += f"Status: {session.status.value}\n"
            report += f"Agent-7 Tasks: {len(session.agent7_tasks)}\n"
            report += f"Agent-8 Tasks: {len(session.agent8_tasks)}\n"
            report += f"Shared Resources: {len(session.shared_resources)}\n"
            report += f"Success Rate: {session.success_rate:.1f}%\n"
            
            if session.end_time:
                duration = (session.end_time - session.start_time).total_seconds()
                report += f"Duration: {duration:.2f}s\n"
            
            report += "\n"
        
        return report


class CoordinationTimer:
    """Coordination timing utilities"""
    
    def __init__(self):
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
    
    def start(self):
        """Start timing"""
        self.start_time = datetime.now()
    
    def stop(self) -> float:
        """Stop timing and return elapsed time"""
        self.end_time = datetime.now()
        if self.start_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0
    
    def get_elapsed_time(self) -> float:
        """Get current elapsed time"""
        if self.start_time:
            current_time = datetime.now()
            return (current_time - self.start_time).total_seconds()
        return 0.0


def create_test_case(
    test_id: str,
    name: str,
    description: str,
    testing_phase: TestingPhase,
    priority: TestPriority = TestPriority.MEDIUM,
    assigned_agent: str = "Agent-7"
) -> TestCase:
    """Create a test case"""
    return TestCase(
        test_id=test_id,
        name=name,
        description=description,
        testing_phase=testing_phase,
        priority=priority,
        status=TestStatus.PENDING,
        assigned_agent=assigned_agent,
        execution_time=0.0,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


def format_execution_time(seconds: float) -> str:
    """Format execution time in human-readable format"""
    if seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"
