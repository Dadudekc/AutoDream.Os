"""
assessmentstatus.py
Module: assessmentstatus.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:37:06
"""

# AssessmentStatus - Extracted for SRP compliance

class AssessmentStatus(Enum):
    """Assessment status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"



