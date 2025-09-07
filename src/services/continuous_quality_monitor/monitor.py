"""Continuous quality monitoring orchestrator."""
from __future__ import annotations

import threading
import time
from dataclasses import asdict
from typing import Dict, List, Optional, Callable

from .config import load_config
from .checks import QualityTrend, perform_quality_validation, analyze_quality_trends
from .alerting import check_quality_alerts
from .reporting import calculate_quality_grade, export_monitoring_report

from services.quality.models import QualityAlert


class ContinuousQualityMonitor:
    """Monitor code quality, generate alerts, and export reports."""

    def __init__(self, config_path: str = "quality_monitor_config.json"):
        self.config_path = config_path
        self.config = load_config(self.config_path)
        self.quality_gates = None
        self.monitoring_active = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.quality_history: List[Dict] = []
        self.alert_history: List[QualityAlert] = []
        self.trend_analysis: Dict[str, QualityTrend] = {}
        self.alert_callbacks: List[Callable[[QualityAlert], None]] = []

    # ------------------------------------------------------------------
    def start_monitoring(self, directory_path: Optional[str] = None) -> bool:
        """Start continuous quality monitoring for ``directory_path``."""
        if self.monitoring_active:
            print("⚠️  Monitoring already active")
            return False
        if directory_path is None:
            directory_path = "."
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(
            target=self._monitoring_loop, args=(directory_path,), daemon=True
        )
        self.monitor_thread.start()
        return True

    def stop_monitoring(self) -> bool:
        """Stop continuous quality monitoring."""
        if not self.monitoring_active:
            print("⚠️  Monitoring not active")
            return False
        self.monitoring_active = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5)
        return True

    def register_alert_callback(self, callback: Callable[[QualityAlert], None]):
        """Register callback for quality alerts."""
        self.alert_callbacks.append(callback)

    # ------------------------------------------------------------------
    def _monitoring_loop(self, directory_path: str) -> None:
        while self.monitoring_active:
            try:
                result = perform_quality_validation(
                    self.quality_gates, directory_path, self.quality_history
                )
                self.quality_history.append(result)
                self.trend_analysis.update(
                    analyze_quality_trends(self.quality_history, self.config)
                )
                check_quality_alerts(
                    result, self.config, self.alert_history, self.alert_callbacks
                )
                time.sleep(self.config["monitoring"]["interval_seconds"])
            except Exception as exc:  # pragma: no cover - defensive
                print(f"❌ Monitoring error: {exc}")
                time.sleep(60)

    # ------------------------------------------------------------------
    def get_quality_summary(self) -> Dict:
        """Return summarized quality information."""
        if not self.quality_history:
            return {"status": "No quality data available"}
        total_validations = len(self.quality_history)
        successful_validations = len(
            [h for h in self.quality_history if h.get("status") != "error"]
        )
        quality_scores = [
            h.get("quality_score", 0)
            for h in self.quality_history
            if h.get("quality_score")
        ]
        average_score = (
            sum(quality_scores) / len(quality_scores) if quality_scores else 0
        )
        alert_summary = {
            "total_alerts": len(self.alert_history),
            "critical_alerts": len(
                [a for a in self.alert_history if a.severity == "CRITICAL"]
            ),
            "high_alerts": len([a for a in self.alert_history if a.severity == "HIGH"]),
            "medium_alerts": len(
                [a for a in self.alert_history if a.severity == "MEDIUM"]
            ),
            "low_alerts": len([a for a in self.alert_history if a.severity == "LOW"]),
        }
        summary = {
            "monitoring_status": "active" if self.monitoring_active else "inactive",
            "total_validations": total_validations,
            "successful_validations": successful_validations,
            "success_rate": (successful_validations / total_validations * 100)
            if total_validations > 0
            else 0,
            "average_quality_score": average_score,
            "quality_grade": calculate_quality_grade(average_score),
            "recent_trends": {k: asdict(v) for k, v in self.trend_analysis.items()},
            "alert_summary": alert_summary,
            "last_validation": self.quality_history[-1].get("monitor_timestamp")
            if self.quality_history
            else None,
            "monitoring_started": self.quality_history[0].get("monitor_timestamp")
            if self.quality_history
            else None,
        }
        return summary

    def export_monitoring_report(
        self, output_path: str = "continuous_quality_report.json"
    ):
        """Export monitoring report to ``output_path``."""
        summary = self.get_quality_summary()
        return export_monitoring_report(
            output_path,
            self.config,
            self.quality_history,
            self.alert_history,
            self.trend_analysis,
            summary,
        )
