"""FSM Monitoring Helper - Extracted for C-056 | Agent-5"""

import logging
import threading

logger = logging.getLogger(__name__)


class FSMMonitoringHelper:
    """Background monitoring for FSM orchestrator."""

    @staticmethod
    def start_monitoring(orchestrator):
        """Start background monitoring thread."""
        if orchestrator._monitoring:
            logger.warning("Monitoring already started")
            return
        orchestrator._monitoring = True
        orchestrator._stop_event.clear()
        orchestrator._monitor_thread = threading.Thread(
            target=FSMMonitoringHelper._monitor_loop, args=(orchestrator,), daemon=True
        )
        orchestrator._monitor_thread.start()
        logger.info("Background monitoring started")

    @staticmethod
    def stop_monitoring(orchestrator):
        """Stop background monitoring."""
        if not orchestrator._monitoring:
            return
        orchestrator._monitoring = False
        orchestrator._stop_event.set()
        if orchestrator._monitor_thread:
            orchestrator._monitor_thread.join(timeout=5)
        logger.info("Background monitoring stopped")

    @staticmethod
    def _monitor_loop(orchestrator):
        """Background monitoring loop."""
        while not orchestrator._stop_event.is_set():
            FSMMonitoringHelper._check_inboxes(orchestrator)
            orchestrator._stop_event.wait(timeout=10)

    @staticmethod
    def _check_inboxes(orchestrator):
        """Check agent inboxes for reports."""
        try:
            for inbox_path in orchestrator.inbox_root.glob("*"):
                if not inbox_path.is_dir():
                    continue
                for report_file in inbox_path.glob("report_*.json"):
                    try:
                        with open(report_file, encoding="utf-8") as f:
                            import json

                            from .fsm_orchestrator import AgentReport

                            report_data = json.load(f)
                            report = AgentReport(**report_data)
                            orchestrator.process_agent_report(report)
                            report_file.unlink()
                    except Exception as e:
                        logger.error(f"Error processing report {report_file}: {e}")
        except Exception as e:
            logger.error(f"Error checking inboxes: {e}")
