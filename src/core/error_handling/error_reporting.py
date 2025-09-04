#!/usr/bin/env python3
"""
Error Reporting Module - Agent Cellphone V2
=====================================

Error reporting and logging system for comprehensive error tracking.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from ..core.unified_import_system import logging


logger = logging.getLogger(__name__)


class ErrorReport:
    """Represents a comprehensive error report."""

    def __init__(self, component: str, time_range: timedelta = timedelta(hours=24)):
        """Initialize error report."""
        self.component = component
        self.time_range = time_range
        self.start_time = datetime.now() - time_range
        self.errors: List[ErrorContext] = []
        self.error_counts: Dict[str, int] = defaultdict(int)
        self.severity_counts: Dict[ErrorSeverity, int] = defaultdict(int)

    def add_error(self, error: ErrorContext):
        """Add an error to the report."""
        if error.timestamp >= self.start_time:
            self.errors.append(error)
            self.error_counts[error.operation] += 1
            self.severity_counts[error.severity] += 1

    def get_summary(self) -> Dict[str, Any]:
        """Get error report summary."""
        return {
            "component": self.component,
            "time_range_hours": self.time_range.total_seconds() / 3600,
            "total_errors": len(self.errors),
            "unique_operations": len(self.error_counts),
            "severity_breakdown": dict(self.severity_counts),
            "most_common_operations": sorted(
                self.error_counts.items(), key=lambda x: x[1], reverse=True
            )[:5],
        }

    def get_detailed_report(self) -> Dict[str, Any]:
        """Get detailed error report."""
        return {
            "summary": self.get_summary(),
            "recent_errors": [
                {
                    "operation": error.operation,
                    "severity": error.severity.value,
                    "timestamp": error.timestamp.isoformat(),
                    "retry_count": error.retry_count,
                    "details": error.details,
                }
                for error in sorted(
                    self.errors, key=lambda x: x.timestamp, reverse=True
                )[:10]
            ],
            "error_patterns": self._analyze_patterns(),
        }

    def _analyze_patterns(self) -> Dict[str, Any]:
        """Analyze error patterns."""
        if not self.errors:
            return {"patterns_found": 0}

        # Group errors by operation and severity
        patterns = defaultdict(lambda: defaultdict(int))

        for error in self.errors:
            patterns[error.operation][error.severity.value] += 1

        # Find patterns with high frequency
        significant_patterns = []
        for operation, severity_counts in patterns.items():
            total_for_operation = sum(severity_counts.values())
            if total_for_operation >= 3:  # Consider it a pattern if >= 3 occurrences
                significant_patterns.append(
                    {
                        "operation": operation,
                        "total_occurrences": total_for_operation,
                        "severity_distribution": dict(severity_counts),
                    }
                )

        return {
            "patterns_found": len(significant_patterns),
            "significant_patterns": sorted(
                significant_patterns, key=lambda x: x["total_occurrences"], reverse=True
            ),
        }


class ErrorReporter:
    """Handles error reporting and logging."""

    def __init__(self, log_directory: str = "logs/errors"):
        """Initialize error reporter."""
        self.log_directory = get_unified_utility().Path(log_directory)
        self.log_directory.mkdir(parents=True, exist_ok=True)
        self.reports: Dict[str, ErrorReport] = {}
        self.error_buffer: List[ErrorContext] = []

    def report_error(self, error: ErrorContext):
        """Report an error for tracking and analysis."""
        self.error_buffer.append(error)

        # Create component report if it doesn't exist
        if error.component not in self.reports:
            self.reports[error.component] = ErrorReport(error.component)

        self.reports[error.component].add_error(error)

        # Log the error
        self._log_error(error)

        # Flush buffer if it gets too large
        if len(self.error_buffer) >= 100:
            self.flush_buffer()

    def _log_error(self, error: ErrorContext):
        """Log error to file and console."""
        log_message = (
            f"[{error.timestamp.isoformat()}] {error.severity.value} - "
            f"{error.component}.{error.operation}: {error.details}"
        )

        if error.severity == ErrorSeverity.CRITICAL:
            get_logger(__name__).critical(log_message)
        elif error.severity == ErrorSeverity.HIGH:
            get_logger(__name__).error(log_message)
        elif error.severity == ErrorSeverity.MEDIUM:
            get_logger(__name__).warning(log_message)
        else:
            get_logger(__name__).info(log_message)

    def generate_report(
        self, component: str = None, time_range: timedelta = timedelta(hours=24)
    ) -> Dict[str, Any]:
        """Generate error report."""
        if component and component in self.reports:
            # Update the report with any new errors in buffer
            for error in self.error_buffer:
                if error.component == component:
                    self.reports[component].add_error(error)

            return self.reports[component].get_detailed_report()
        else:
            # Generate system-wide report
            system_report = {
                "timestamp": datetime.now().isoformat(),
                "components": {},
                "system_summary": {
                    "total_components": len(self.reports),
                    "total_errors": sum(
                        len(report.errors) for report in self.reports.values()
                    ),
                },
            }

            for comp_name, report in self.reports.items():
                system_report["components"][comp_name] = report.get_summary()

            return system_report

    def flush_buffer(self):
        """Flush error buffer to persistent storage."""
        if not self.error_buffer:
            return

        # Write buffered errors to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        buffer_file = self.log_directory / f"error_buffer_{timestamp}.json"

        try:
            with open(buffer_file, "w") as f:
                write_json(
                    {
                        "timestamp": datetime.now().isoformat(), "errors": [
                            {
                                "operation": error.operation,
                                "component": error.component,
                                "severity": error.severity.value,
                                "timestamp": error.timestamp.isoformat(),
                                "retry_count": error.retry_count,
                                "details": error.details,
                            }
                            for error in self.error_buffer
                        ],
                    },
                    f,
                    indent=2,
                )

            get_logger(__name__).info(f"Flushed {len(self.error_buffer)} errors to {buffer_file}")
            self.error_buffer.clear()

        except Exception as e:
            get_logger(__name__).error(f"Failed to flush error buffer: {e}")

    def cleanup_old_logs(self, max_age_days: int = 30):
        """Clean up old error log files."""
        cutoff_date = datetime.now() - timedelta(days=max_age_days)

        cleaned_count = 0
        for log_file in self.log_directory.glob("*.json"):
            if log_file.stat().st_mtime < cutoff_date.timestamp():
                log_file.unlink()
                cleaned_count += 1

        if cleaned_count > 0:
            get_logger(__name__).info(f"Cleaned up {cleaned_count} old error log files")

        return cleaned_count

    def get_error_trends(self, component: str = None, days: int = 7) -> Dict[str, Any]:
        """Get error trends over time."""
        if component and component not in self.reports:
            return {"error": f"No data available for component: {component}"}

        # Analyze trends across specified time period
        trends = defaultdict(lambda: defaultdict(int))
        start_date = datetime.now() - timedelta(days=days)

        errors_to_analyze = []
        if component:
            errors_to_analyze = self.reports[component].errors
        else:
            for report in self.reports.values():
                errors_to_analyze.extend(report.errors)

        for error in errors_to_analyze:
            if error.timestamp >= start_date:
                date_key = error.timestamp.date().isoformat()
                trends[date_key][error.severity.value] += 1

        return {
            "component": component or "system_wide",
            "days_analyzed": days,
            "daily_trends": dict(trends),
            "trend_summary": self._summarize_trends(dict(trends)),
        }

    def _summarize_trends(self, trends: Dict[str, Dict[str, int]]) -> Dict[str, Any]:
        """Summarize error trends."""
        if not get_unified_validator().validate_required(trends):
            return {"trend": "stable", "change_percent": 0}

        # Calculate trend direction
        dates = sorted(trends.keys())
        if len(dates) < 2:
            return {"trend": "insufficient_data", "change_percent": 0}

        # Compare first half with second half
        mid_point = len(dates) // 2
        first_half = dates[:mid_point]
        second_half = dates[mid_point:]

        first_half_total = sum(
            sum(severities.values())
            for date in first_half
            for severities in [trends[date]]
        )

        second_half_total = sum(
            sum(severities.values())
            for date in second_half
            for severities in [trends[date]]
        )

        if first_half_total == 0:
            change_percent = float("inf") if second_half_total > 0 else 0
        else:
            change_percent = (
                (second_half_total - first_half_total) / first_half_total
            ) * 100

        if change_percent > 20:
            trend = "increasing"
        elif change_percent < -20:
            trend = "decreasing"
        else:
            trend = "stable"

        return {
            "trend": trend,
            "change_percent": round(change_percent, 2),
            "first_half_total": first_half_total,
            "second_half_total": second_half_total,
        }


# Global error reporter instance
error_reporter = ErrorReporter()


def report_error(error: ErrorContext):
    """Convenience function to report an error."""
    error_reporter.report_error(error)


def get_error_report(component: str = None) -> Dict[str, Any]:
    """Convenience function to get error report."""
    return error_reporter.generate_report(component)
