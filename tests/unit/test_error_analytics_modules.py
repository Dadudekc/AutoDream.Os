from datetime import datetime, timedelta
from types import SimpleNamespace

from src.core.error_handler import ErrorSeverity
from src.services.error_analytics import (
    ErrorPatternDetector,
    ErrorTrendAnalyzer,
    ErrorCorrelationAnalyzer,
    ErrorReportGenerator,
)
from src.services.error_analytics_system import ErrorAnalyticsSystem


class DummyErrorHandler:
    def get_error_patterns(self):
        now = datetime.now()
        pattern = SimpleNamespace(
            error_signature="sig1",
            occurrences=12,
            first_seen=now - timedelta(hours=1),
            last_seen=now,
        )
        return [pattern]

    def get_errors_by_pattern(self, signature):
        return [SimpleNamespace(severity=ErrorSeverity.HIGH, category="network")]

    def get_error_history(self, limit=1000):
        now = datetime.now()
        context = SimpleNamespace(service_name="svc")
        return [
            SimpleNamespace(
                timestamp=now - timedelta(minutes=10),
                severity=ErrorSeverity.LOW,
                category="network",
                resolved=True,
                resolution_time=now - timedelta(minutes=5),
                error_type="A",
                context=context,
            ),
            SimpleNamespace(
                timestamp=now - timedelta(minutes=9),
                severity=ErrorSeverity.MEDIUM,
                category="db",
                resolved=True,
                resolution_time=now - timedelta(minutes=4),
                error_type="B",
                context=context,
            ),
            SimpleNamespace(
                timestamp=now - timedelta(minutes=8),
                severity=ErrorSeverity.MEDIUM,
                category="db",
                resolved=True,
                resolution_time=now - timedelta(minutes=3),
                error_type="B",
                context=context,
            ),
        ]


def test_pattern_detector_detects_patterns():
    handler = DummyErrorHandler()
    detector = ErrorPatternDetector(handler)
    patterns = detector.detect_error_patterns()
    assert len(patterns) == 1
    analysis = detector.get_pattern_analysis(patterns[0])
    assert analysis.error_signature == "sig1"
    stats = detector.get_pattern_statistics()
    assert stats["total_patterns"] == 1


def test_trend_analyzer_produces_trends():
    handler = DummyErrorHandler()
    analyzer = ErrorTrendAnalyzer(handler)
    trends = analyzer.analyze_error_trends()
    assert trends
    stats = analyzer.get_trend_statistics()
    assert stats["total_trends"] == len(trends)


def test_correlation_analyzer_detects_correlations():
    handler = DummyErrorHandler()
    analyzer = ErrorCorrelationAnalyzer(handler, {"correlation_threshold": 0.0})
    correlations = analyzer.analyze_error_correlations()
    assert correlations
    stats = analyzer.get_correlation_statistics()
    assert stats["total_correlations"] == len(correlations)


def test_report_generator_creates_report(tmp_path):
    generator = ErrorReportGenerator({"reports_directory": tmp_path})
    report = generator.generate_comprehensive_report(
        patterns=[{"error_signature": "sig1", "occurrences": 1}],
        trends=[{"time_period": "2021-01-01 00:00", "error_count": 1, "trend_direction": "stable", "trend_confidence": 0.5}],
        correlations=[{"primary_error": "A", "correlated_errors": ["B"], "correlation_strength": 0.5, "correlation_type": "temporal"}],
    )
    assert report.summary["total_patterns"] == 1
    assert report.recommendations


def test_error_analytics_system_integration():
    handler = DummyErrorHandler()
    system = ErrorAnalyticsSystem(handler, {"enable_background_thread": False, "analysis_interval": 0})
    report = system.generate_report()
    assert report.summary["total_patterns"] == 1
    stats = system.get_analytics_statistics()
    assert stats["reports_generated"] == 1
    system.shutdown()
