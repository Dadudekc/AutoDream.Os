#!/usr/bin/env python3
"""
Project Update Messaging System - V2 Compliant
==============================================

Automated project update messaging system for agent coordination.
Handles project status updates, milestone notifications, and system changes.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from .models.messaging_models import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority, UnifiedMessageTag
from .service import MessagingService

logger = logging.getLogger(__name__)


class ProjectUpdateSystem:
    """Automated project update messaging system."""
    
    def __init__(self, messaging_service: MessagingService):
        """Initialize project update system."""
        self.messaging_service = messaging_service
        self.update_history_file = Path("data/project_update_history.json")
        self.update_history_file.parent.mkdir(exist_ok=True)
        
    def send_project_update(
        self,
        update_type: str,
        title: str,
        description: str,
        affected_agents: Optional[List[str]] = None,
        priority: str = "NORMAL",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, bool]:
        """
        Send project update to relevant agents.
        
        Args:
            update_type: Type of update (milestone, status, system_change, etc.)
            title: Update title
            description: Detailed description
            affected_agents: List of agents to notify (None = all agents)
            priority: Message priority
            metadata: Additional metadata
        """
        # Create update message
        message_content = self._format_update_message(update_type, title, description, metadata)
        
        # Determine recipients
        if affected_agents is None:
            affected_agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
        
        # Send messages
        results = {}
        for agent in affected_agents:
            try:
                success = self.messaging_service.send(
                    agent_id=agent,
                    content=message_content,
                    priority=priority,
                    tag="PROJECT_UPDATE"
                )
                results[agent] = success
                
                if success:
                    logger.info(f"Project update sent to {agent}: {title}")
                else:
                    logger.error(f"Failed to send project update to {agent}: {title}")
                    
            except Exception as e:
                logger.error(f"Error sending project update to {agent}: {e}")
                results[agent] = False
        
        # Record update in history
        self._record_update(update_type, title, description, affected_agents, results)
        
        return results
    
    def send_milestone_notification(
        self,
        milestone: str,
        description: str,
        completion_percentage: int,
        next_steps: Optional[List[str]] = None
    ) -> Dict[str, bool]:
        """Send milestone completion notification."""
        metadata = {
            "milestone": milestone,
            "completion_percentage": completion_percentage,
            "next_steps": next_steps or []
        }
        
        return self.send_project_update(
            update_type="milestone",
            title=f"Milestone Achieved: {milestone}",
            description=description,
            priority="HIGH",
            metadata=metadata
        )
    
    def send_system_status_update(
        self,
        system_name: str,
        status: str,
        details: str,
        health_metrics: Optional[Dict[str, Any]] = None
    ) -> Dict[str, bool]:
        """Send system status update."""
        metadata = {
            "system_name": system_name,
            "status": status,
            "health_metrics": health_metrics or {}
        }
        
        return self.send_project_update(
            update_type="system_status",
            title=f"System Update: {system_name} - {status}",
            description=details,
            priority="NORMAL",
            metadata=metadata
        )
    
    def send_v2_compliance_update(
        self,
        compliance_status: str,
        files_checked: int,
        violations_found: int,
        details: str
    ) -> Dict[str, bool]:
        """Send V2 compliance update."""
        metadata = {
            "compliance_status": compliance_status,
            "files_checked": files_checked,
            "violations_found": violations_found
        }
        
        priority = "HIGH" if violations_found > 0 else "NORMAL"
        
        return self.send_project_update(
            update_type="v2_compliance",
            title=f"V2 Compliance Update: {compliance_status}",
            description=details,
            priority=priority,
            metadata=metadata
        )
    
    def send_documentation_cleanup_update(
        self,
        files_removed: int,
        files_kept: int,
        cleanup_summary: str
    ) -> Dict[str, bool]:
        """Send documentation cleanup update."""
        metadata = {
            "files_removed": files_removed,
            "files_kept": files_kept,
            "cleanup_type": "documentation"
        }
        
        return self.send_project_update(
            update_type="documentation_cleanup",
            title=f"Documentation Cleanup Complete: {files_removed} files removed",
            description=cleanup_summary,
            priority="NORMAL",
            metadata=metadata
        )
    
    def send_feature_announcement(
        self,
        feature_name: str,
        description: str,
        affected_agents: Optional[List[str]] = None,
        usage_instructions: Optional[str] = None
    ) -> Dict[str, bool]:
        """Send new feature announcement."""
        metadata = {
            "feature_name": feature_name,
            "usage_instructions": usage_instructions or ""
        }
        
        return self.send_project_update(
            update_type="feature_announcement",
            title=f"New Feature Available: {feature_name}",
            description=description,
            affected_agents=affected_agents,
            priority="HIGH",
            metadata=metadata
        )
    
    def _format_update_message(
        self,
        update_type: str,
        title: str,
        description: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Format project update message."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message = f"""📋 PROJECT UPDATE - {update_type.upper()}
============================================================
📅 Timestamp: {timestamp}
📝 Title: {title}
📄 Description: {description}"""
        
        if metadata:
            message += "\n\n📊 Metadata:"
            for key, value in metadata.items():
                if isinstance(value, list):
                    value = ", ".join(str(v) for v in value)
                message += f"\n  • {key}: {value}"
        
        message += "\n\n📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory"
        message += "\n============================================================"
        
        return message
    
    def _record_update(
        self,
        update_type: str,
        title: str,
        description: str,
        affected_agents: List[str],
        results: Dict[str, bool]
    ) -> None:
        """Record update in history file."""
        try:
            # Load existing history
            history = []
            if self.update_history_file.exists():
                with open(self.update_history_file, 'r') as f:
                    history = json.load(f)
            
            # Add new update
            update_record = {
                "timestamp": datetime.now().isoformat(),
                "update_type": update_type,
                "title": title,
                "description": description,
                "affected_agents": affected_agents,
                "delivery_results": results,
                "success_count": sum(1 for success in results.values() if success),
                "total_count": len(results)
            }
            
            history.append(update_record)
            
            # Keep only last 100 updates
            if len(history) > 100:
                history = history[-100:]
            
            # Save history
            with open(self.update_history_file, 'w') as f:
                json.dump(history, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to record update in history: {e}")
    
    def get_update_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent update history."""
        try:
            if not self.update_history_file.exists():
                return []
            
            with open(self.update_history_file, 'r') as f:
                history = json.load(f)
            
            return history[-limit:] if limit else history
            
        except Exception as e:
            logger.error(f"Failed to load update history: {e}")
            return []
    
    def get_update_statistics(self) -> Dict[str, Any]:
        """Get update statistics."""
        try:
            history = self.get_update_history(limit=0)  # Get all history
            
            if not history:
                return {"total_updates": 0, "success_rate": 0.0}
            
            total_updates = len(history)
            total_deliveries = sum(record.get("total_count", 0) for record in history)
            successful_deliveries = sum(record.get("success_count", 0) for record in history)
            
            success_rate = (successful_deliveries / total_deliveries * 100) if total_deliveries > 0 else 0.0
            
            # Count by update type
            update_types = {}
            for record in history:
                update_type = record.get("update_type", "unknown")
                update_types[update_type] = update_types.get(update_type, 0) + 1
            
            return {
                "total_updates": total_updates,
                "total_deliveries": total_deliveries,
                "successful_deliveries": successful_deliveries,
                "success_rate": round(success_rate, 2),
                "update_types": update_types
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate update statistics: {e}")
            return {"error": str(e)}
