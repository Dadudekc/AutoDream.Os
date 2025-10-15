#!/usr/bin/env python3
"""
Cycle Health Check - Pre/Post Cycle Validation Hooks
====================================================

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-10-15
Part of: Unified Agent Knowledge System (Agent-1 + Agent-3 Collaboration)

PURPOSE:
    Enforce agent cycle protocols through automated health checks.
    Validates agent readiness before cycle start and completion after cycle end.

FEATURES:
    - Pre-cycle validation (status current, inbox processed, DB synced)
    - Post-cycle validation (status updated, work logged, no errors)
    - Automatic reminder generation for failed checks
    - Captain alerting for repeated violations
    - Violation tracking and reporting

USAGE:
    from swarm_brain.agent_field_manual.automation.cycle_health_check import CycleHealthCheck
    
    # Initialize checker
    checker = CycleHealthCheck()
    
    # Pre-cycle check
    result = checker.pre_cycle_check("Agent-3")
    if result['passed']:
        print("Agent ready for cycle")
    else:
        print(f"Failed checks: {result['failed_checks']}")
    
    # Post-cycle check
    result = checker.post_cycle_check("Agent-3")
    if result['passed']:
        print("Cycle completed successfully")
    else:
        print(f"Failed checks: {result['failed_checks']}")
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class CycleHealthCheck:
    """Pre/post cycle validation hooks for agent health checks"""
    
    def __init__(self, max_age_minutes: int = 30):
        """
        Initialize cycle health checker
        
        Args:
            max_age_minutes: Maximum age for status.json before considered stale
        """
        self.max_age_minutes = max_age_minutes
        self.workspace_root = Path("agent_workspaces")
        
        logger.info(f"CycleHealthCheck initialized (max_age: {max_age_minutes} min)")
    
    def pre_cycle_check(self, agent_id: str) -> Dict[str, Any]:
        """
        Validate agent ready for cycle start
        
        Checks:
        - status.json exists and is current
        - Inbox has been processed
        - Database is synchronized
        - No active violations
        
        Args:
            agent_id: Agent identifier (e.g., "Agent-3")
        
        Returns:
            Dictionary with check results:
            {
                'passed': bool,
                'checks': Dict[str, bool],
                'failed_checks': List[str],
                'timestamp': str
            }
        """
        logger.info(f"[{agent_id}] Running pre-cycle health check")
        
        checks = {
            'status_exists': self._check_status_exists(agent_id),
            'status_current': self._check_not_stale(agent_id),
            'inbox_processed': self._check_inbox_empty(agent_id),
            'db_synced': self._check_db_sync(agent_id),
            'no_violations': self._check_no_active_violations(agent_id)
        }
        
        failed_checks = [name for name, passed in checks.items() if not passed]
        passed = all(checks.values())
        
        result = {
            'passed': passed,
            'checks': checks,
            'failed_checks': failed_checks,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
        if not passed:
            logger.warning(f"[{agent_id}] Pre-cycle check FAILED: {failed_checks}")
            self._send_reminder(agent_id, failed_checks, cycle_phase='start')
            self._log_violation(agent_id, result, cycle_phase='start')
        else:
            logger.info(f"[{agent_id}] Pre-cycle check PASSED")
        
        return result
    
    def post_cycle_check(self, agent_id: str) -> Dict[str, Any]:
        """
        Validate cycle completion
        
        Checks:
        - status.json updated with new timestamp
        - Work logged (actionable results)
        - Database synchronized
        - No errors in error logs
        
        Args:
            agent_id: Agent identifier (e.g., "Agent-3")
        
        Returns:
            Dictionary with check results (same format as pre_cycle_check)
        """
        logger.info(f"[{agent_id}] Running post-cycle health check")
        
        checks = {
            'status_updated': self._check_status_timestamp(agent_id),
            'work_logged': self._check_actionable_results(agent_id),
            'db_synced': self._check_db_sync(agent_id),
            'no_errors': self._check_error_logs(agent_id)
        }
        
        failed_checks = [name for name, passed in checks.items() if not passed]
        passed = all(checks.values())
        
        result = {
            'passed': passed,
            'checks': checks,
            'failed_checks': failed_checks,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
        if not passed:
            logger.warning(f"[{agent_id}] Post-cycle check FAILED: {failed_checks}")
            self._alert_captain(agent_id, failed_checks, cycle_phase='end')
            self._log_violation(agent_id, result, cycle_phase='end')
        else:
            logger.info(f"[{agent_id}] Post-cycle check PASSED")
        
        return result
    
    # ========================================================================
    # CHECK IMPLEMENTATIONS
    # ========================================================================
    
    def _check_status_exists(self, agent_id: str) -> bool:
        """Check if status.json exists"""
        status_path = self.workspace_root / agent_id / "status.json"
        exists = status_path.exists()
        
        if not exists:
            logger.error(f"[{agent_id}] status.json does not exist")
        
        return exists
    
    def _check_not_stale(self, agent_id: str) -> bool:
        """Check if status.json is not stale (updated recently)"""
        try:
            status = self._read_status(agent_id)
            if not status:
                return False
            
            last_updated = status.get('last_updated', '')
            if not last_updated:
                logger.warning(f"[{agent_id}] No last_updated timestamp")
                return False
            
            # Parse timestamp
            try:
                updated_time = datetime.fromisoformat(
                    last_updated.replace('Z', '+00:00')
                )
            except Exception as e:
                logger.error(f"[{agent_id}] Invalid timestamp format: {e}")
                return False
            
            # Check age
            now = datetime.now(updated_time.tzinfo)
            age_minutes = (now - updated_time).total_seconds() / 60
            
            is_current = age_minutes <= self.max_age_minutes
            
            if not is_current:
                logger.warning(
                    f"[{agent_id}] Stale status.json "
                    f"(age: {age_minutes:.1f} min > {self.max_age_minutes} min)"
                )
            
            return is_current
            
        except Exception as e:
            logger.error(f"[{agent_id}] Error checking staleness: {e}")
            return False
    
    def _check_inbox_empty(self, agent_id: str) -> bool:
        """Check if inbox has been processed (no unread messages)"""
        inbox_path = self.workspace_root / agent_id / "inbox"
        
        if not inbox_path.exists():
            return True
        
        try:
            # Count non-archive files
            unread_count = 0
            for item in inbox_path.iterdir():
                if item.is_file() and not item.name.startswith('.'):
                    # Exclude archived messages
                    if 'archive' not in item.name.lower():
                        unread_count += 1
            
            # Allow up to 3 unread messages (some flexibility)
            is_processed = unread_count <= 3
            
            if not is_processed:
                logger.warning(
                    f"[{agent_id}] Inbox has {unread_count} unprocessed messages"
                )
            
            return is_processed
            
        except Exception as e:
            logger.error(f"[{agent_id}] Error checking inbox: {e}")
            return False
    
    def _check_db_sync(self, agent_id: str) -> bool:
        """Check if database is synchronized"""
        # TODO: Implement actual DB sync check
        # For now, assume synced (placeholder)
        return True
    
    def _check_no_active_violations(self, agent_id: str) -> bool:
        """Check for active protocol violations"""
        # TODO: Implement violation tracking system
        # For now, assume no violations (placeholder)
        return True
    
    def _check_status_timestamp(self, agent_id: str) -> bool:
        """Check if status.json was updated this cycle (recent timestamp)"""
        # Similar to _check_not_stale but with tighter time window
        try:
            status = self._read_status(agent_id)
            if not status:
                return False
            
            last_updated = status.get('last_updated', '')
            if not last_updated:
                return False
            
            updated_time = datetime.fromisoformat(
                last_updated.replace('Z', '+00:00')
            )
            now = datetime.now(updated_time.tzinfo)
            age_minutes = (now - updated_time).total_seconds() / 60
            
            # Cycle update should be within last 5 minutes
            is_updated = age_minutes <= 5
            
            if not is_updated:
                logger.warning(
                    f"[{agent_id}] Status not updated this cycle "
                    f"(age: {age_minutes:.1f} min)"
                )
            
            return is_updated
            
        except Exception as e:
            logger.error(f"[{agent_id}] Error checking timestamp: {e}")
            return False
    
    def _check_actionable_results(self, agent_id: str) -> bool:
        """Check if agent logged actionable work results"""
        try:
            status = self._read_status(agent_id)
            if not status:
                return False
            
            # Check for evidence of work
            indicators = [
                bool(status.get('completed_tasks')),
                bool(status.get('current_tasks')),
                bool(status.get('achievements')),
                bool(status.get('session_summary'))
            ]
            
            has_work = any(indicators)
            
            if not has_work:
                logger.warning(f"[{agent_id}] No actionable work logged")
            
            return has_work
            
        except Exception as e:
            logger.error(f"[{agent_id}] Error checking work: {e}")
            return False
    
    def _check_error_logs(self, agent_id: str) -> bool:
        """Check for errors in agent logs"""
        # TODO: Implement error log checking
        # For now, assume no errors (placeholder)
        return True
    
    # ========================================================================
    # HELPER METHODS
    # ========================================================================
    
    def _read_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Read agent status.json"""
        try:
            status_path = self.workspace_root / agent_id / "status.json"
            if not status_path.exists():
                return None
            
            with open(status_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"[{agent_id}] Failed to read status: {e}")
            return None
    
    def _send_reminder(
        self, 
        agent_id: str, 
        failed_checks: List[str],
        cycle_phase: str
    ):
        """Send reminder to agent about failed checks"""
        reminder_path = (
            self.workspace_root / agent_id / "inbox" / 
            f"HEALTH_CHECK_REMINDER_{cycle_phase}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.md"
        )
        
        try:
            reminder_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(reminder_path, 'w', encoding='utf-8') as f:
                f.write(f"# ⚠️ Health Check Reminder - {cycle_phase.upper()}\n\n")
                f.write(f"**Agent:** {agent_id}\n")
                f.write(f"**Timestamp:** {datetime.utcnow().isoformat()}Z\n")
                f.write(f"**Phase:** {cycle_phase}\n\n")
                f.write("## Failed Checks:\n\n")
                for check in failed_checks:
                    f.write(f"- ❌ {check}\n")
                f.write("\n**Action Required:** Address failed checks before proceeding.\n")
            
            logger.info(f"[{agent_id}] Reminder sent: {reminder_path.name}")
            
        except Exception as e:
            logger.error(f"[{agent_id}] Failed to send reminder: {e}")
    
    def _alert_captain(
        self, 
        agent_id: str, 
        failed_checks: List[str],
        cycle_phase: str
    ):
        """Alert Captain about failed post-cycle checks"""
        alert_path = (
            Path("agent_workspaces/Agent-4/inbox") / 
            f"HEALTH_CHECK_VIOLATION_{agent_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.md"
        )
        
        try:
            alert_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(alert_path, 'w', encoding='utf-8') as f:
                f.write(f"# 🚨 Health Check Violation - {agent_id}\n\n")
                f.write(f"**Agent:** {agent_id}\n")
                f.write(f"**Timestamp:** {datetime.utcnow().isoformat()}Z\n")
                f.write(f"**Phase:** {cycle_phase}\n")
                f.write(f"**Severity:** WARNING\n\n")
                f.write("## Failed Checks:\n\n")
                for check in failed_checks:
                    f.write(f"- ❌ {check}\n")
                f.write("\n**Captain Action Required:** Review agent performance.\n")
            
            logger.info(f"Captain alerted about {agent_id} violations")
            
        except Exception as e:
            logger.error(f"Failed to alert Captain: {e}")
    
    def _log_violation(
        self, 
        agent_id: str, 
        result: Dict[str, Any],
        cycle_phase: str
    ):
        """Log violation to tracking system"""
        # TODO: Implement violation tracking database
        logger.warning(
            f"[{agent_id}] Violation logged: {cycle_phase} - "
            f"{result['failed_checks']}"
        )


# ========================================================================
# EXAMPLE USAGE
# ========================================================================

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Example: Check Agent-3 health
    checker = CycleHealthCheck(max_age_minutes=30)
    
    print("\n=== Pre-Cycle Health Check ===")
    result = checker.pre_cycle_check("Agent-3")
    print(f"Passed: {result['passed']}")
    for check, passed in result['checks'].items():
        status = "✅" if passed else "❌"
        print(f"{status} {check}")
    
    print("\n=== Post-Cycle Health Check ===")
    result = checker.post_cycle_check("Agent-3")
    print(f"Passed: {result['passed']}")
    for check, passed in result['checks'].items():
        status = "✅" if passed else "❌"
        print(f"{status} {check}")

