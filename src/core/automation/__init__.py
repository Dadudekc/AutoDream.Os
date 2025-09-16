#!/usr/bin/env python3
"""
Automation Package - Modularized automation system
=================================================

V2-compliant automation system components:
- AutomationMessage: Message handling
- MailboxProcessor: Mailbox processing automation
- TaskClaimer: Task claiming automation

Author: Agent-3 (Infrastructure & DevOps Specialist)
Mission: V2 compliance modularization
License: MIT
"""

from .automation_message import AutomationMessage
from .mailbox_processor import MailboxProcessor
from .task_claimer import TaskClaimer

__all__ = [
    "AutomationMessage",
    "MailboxProcessor", 
    "TaskClaimer"
]
