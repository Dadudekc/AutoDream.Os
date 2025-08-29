#!/usr/bin/env python3
"""
Emergency Documentation - Component of Emergency Response System
==============================================================

Responsible for emergency event logging, documentation, and report generation.
Extracted from EmergencyResponseSystem to follow Single Responsibility Principle.

Author: Agent-7 (Class Hierarchy Refactoring)
Contract: MODULAR-002: Class Hierarchy Refactoring (400 pts)
License: MIT
"""

import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum

from ..base_manager import BaseManager
from .docs.generator import generate_report_content
from .docs.distribution import save_document_to_file


logger = logging.getLogger(__name__)


class DocumentType(Enum):
    """Types of emergency documentation"""

    EVENT_LOG = "event_log"
    RESPONSE_TIMELINE = "response_timeline"
    RECOVERY_VALIDATION = "recovery_validation"
    LESSONS_LEARNED = "lessons_learned"
    INCIDENT_REPORT = "incident_report"
    STATUS_UPDATE = "status_update"


class DocumentPriority(Enum):
    """Document priority levels"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class EmergencyEvent:
    """Emergency event data structure for documentation"""

    event_id: str
    timestamp: datetime
    event_type: str
    description: str
    source: str
    severity: str
    affected_components: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)


@dataclass
class ResponseTimeline:
    """Response action timeline for documentation"""

    timeline_id: str
    emergency_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    actions: List[Dict[str, Any]] = field(default_factory=list)
    milestones: List[Dict[str, Any]] = field(default_factory=list)
    duration: Optional[timedelta] = None


@dataclass
class RecoveryValidation:
    """Recovery validation results for documentation"""

    validation_id: str
    recovery_id: str
    timestamp: datetime
    criteria_tested: List[str] = field(default_factory=list)
    results: Dict[str, bool] = field(default_factory=dict)
    overall_success: bool = False
    notes: str = ""
    validator: str = ""


@dataclass
class LessonsLearned:
    """Lessons learned documentation"""

    lesson_id: str
    emergency_id: str
    timestamp: datetime
    category: str
    description: str
    impact: str
    recommendations: List[str] = field(default_factory=list)
    implementation_priority: DocumentPriority = DocumentPriority.MEDIUM
    assigned_to: Optional[str] = None
    status: str = "open"


@dataclass
class EmergencyDocument:
    """Emergency document metadata"""

    document_id: str
    document_type: DocumentType
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    author: str
    priority: DocumentPriority
    tags: List[str] = field(default_factory=list)
    related_emergencies: List[str] = field(default_factory=list)
    file_path: Optional[str] = None


class EmergencyDocumentation(BaseManager):
    """
    Emergency Documentation - Single responsibility: Emergency documentation and reporting

    This component is responsible for:
    - Emergency event logging and tracking
    - Response timeline documentation
    - Recovery validation reporting
    - Lessons learned documentation
    - Report generation and export
    """

    def __init__(self, config_path: str = "config/emergency_documentation.json"):
        """Initialize emergency documentation system"""
        super().__init__(
            manager_name="EmergencyDocumentation",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True,
        )

        # Documentation storage
        self.emergency_events: List[EmergencyEvent] = []
        self.response_timelines: List[ResponseTimeline] = []
        self.recovery_validations: List[RecoveryValidation] = []
        self.lessons_learned: List[LessonsLearned] = []
        self.documents: List[EmergencyDocument] = []

        # Configuration
        self.documentation_path = Path("emergency_documentation")
        self.auto_save_interval = 300  # 5 minutes
        self.max_events_retained = 1000
        self.max_documents_retained = 500

        # Load configuration and setup
        self._load_documentation_config()
        self._setup_documentation_directory()

        self.logger.info("✅ Emergency Documentation system initialized successfully")

    def _load_documentation_config(self):
        """Load documentation configuration"""
        try:
            config = self.get_config()

            # Load configuration settings
            self.documentation_path = Path(
                config.get("documentation_path", "emergency_documentation")
            )
            self.auto_save_interval = config.get("auto_save_interval", 300)
            self.max_events_retained = config.get("max_events_retained", 1000)
            self.max_documents_retained = config.get("max_documents_retained", 500)

        except Exception as e:
            self.logger.error(f"Failed to load documentation config: {e}")

    def _setup_documentation_directory(self):
        """Setup documentation directory structure"""
        try:
            # Create main documentation directory
            self.documentation_path.mkdir(exist_ok=True)

            # Create subdirectories for different document types
            (self.documentation_path / "events").mkdir(exist_ok=True)
            (self.documentation_path / "timelines").mkdir(exist_ok=True)
            (self.documentation_path / "validations").mkdir(exist_ok=True)
            (self.documentation_path / "lessons").mkdir(exist_ok=True)
            (self.documentation_path / "reports").mkdir(exist_ok=True)

            self.logger.info(
                f"✅ Documentation directory structure created: {self.documentation_path}"
            )

        except Exception as e:
            self.logger.error(f"Failed to setup documentation directory: {e}")

    def log_emergency_event(
        self,
        event_type: str,
        description: str,
        source: str,
        severity: str = "medium",
        affected_components: Optional[List[str]] = None,
        details: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
    ) -> str:
        """Log an emergency event"""
        try:
            event_id = f"event_{int(time.time())}_{len(self.emergency_events)}"

            event = EmergencyEvent(
                event_id=event_id,
                timestamp=datetime.now(),
                event_type=event_type,
                description=description,
                source=source,
                severity=severity,
                affected_components=affected_components or [],
                details=details or {},
                tags=tags or [],
            )

            self.emergency_events.append(event)

            # Maintain event limit
            if len(self.emergency_events) > self.max_events_retained:
                self.emergency_events.pop(0)

            # Record event
            self.record_event(
                "emergency_event_logged",
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "severity": severity,
                    "timestamp": event.timestamp.isoformat(),
                },
            )

            self.logger.info(f"📝 Emergency event logged: {event_type} - {description}")
            return event_id

        except Exception as e:
            self.logger.error(f"Failed to log emergency event: {e}")
            return ""

    def create_response_timeline(self, emergency_id: str) -> str:
        """Create a response timeline for an emergency"""
        try:
            timeline_id = f"timeline_{emergency_id}_{int(time.time())}"

            timeline = ResponseTimeline(
                timeline_id=timeline_id,
                emergency_id=emergency_id,
                start_time=datetime.now(),
            )

            self.response_timelines.append(timeline)

            self.logger.info(f"📅 Response timeline created: {timeline_id}")
            return timeline_id

        except Exception as e:
            self.logger.error(f"Failed to create response timeline: {e}")
            return ""

    def add_timeline_action(
        self,
        timeline_id: str,
        action: str,
        description: str,
        timestamp: Optional[datetime] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Add an action to a response timeline"""
        try:
            timeline = self._get_timeline(timeline_id)
            if not timeline:
                return False

            action_data = {
                "action": action,
                "description": description,
                "timestamp": timestamp or datetime.now(),
                "details": details or {},
            }

            timeline.actions.append(action_data)

            self.logger.info(f"📝 Timeline action added: {action}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to add timeline action: {e}")
            return False

    def add_timeline_milestone(
        self,
        timeline_id: str,
        milestone: str,
        description: str,
        timestamp: Optional[datetime] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Add a milestone to a response timeline"""
        try:
            timeline = self._get_timeline(timeline_id)
            if not timeline:
                return False

            milestone_data = {
                "milestone": milestone,
                "description": description,
                "timestamp": timestamp or datetime.now(),
                "details": details or {},
            }

            timeline.milestones.append(milestone_data)

            self.logger.info(f"🎯 Timeline milestone added: {milestone}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to add timeline milestone: {e}")
            return False

    def complete_timeline(self, timeline_id: str) -> bool:
        """Mark a response timeline as completed"""
        try:
            timeline = self._get_timeline(timeline_id)
            if not timeline:
                return False

            timeline.end_time = datetime.now()
            timeline.duration = timeline.end_time - timeline.start_time

            self.logger.info(
                f"✅ Timeline completed: {timeline_id} (Duration: {timeline.duration})"
            )
            return True

        except Exception as e:
            self.logger.error(f"Failed to complete timeline: {e}")
            return False

    def log_recovery_validation(
        self,
        recovery_id: str,
        criteria_tested: List[str],
        results: Dict[str, bool],
        overall_success: bool,
        notes: str = "",
        validator: str = "",
    ) -> str:
        """Log recovery validation results"""
        try:
            validation_id = f"validation_{recovery_id}_{int(time.time())}"

            validation = RecoveryValidation(
                validation_id=validation_id,
                recovery_id=recovery_id,
                timestamp=datetime.now(),
                criteria_tested=criteria_tested,
                results=results,
                overall_success=overall_success,
                notes=notes,
                validator=validator,
            )

            self.recovery_validations.append(validation)

            self.logger.info(
                f"✅ Recovery validation logged: {validation_id} (Success: {overall_success})"
            )
            return validation_id

        except Exception as e:
            self.logger.error(f"Failed to log recovery validation: {e}")
            return ""

    def add_lesson_learned(
        self,
        emergency_id: str,
        category: str,
        description: str,
        impact: str,
        recommendations: Optional[List[str]] = None,
        priority: DocumentPriority = DocumentPriority.MEDIUM,
        assigned_to: Optional[str] = None,
    ) -> str:
        """Add a lesson learned from an emergency"""
        try:
            lesson_id = f"lesson_{emergency_id}_{int(time.time())}"

            lesson = LessonsLearned(
                lesson_id=lesson_id,
                emergency_id=emergency_id,
                timestamp=datetime.now(),
                category=category,
                description=description,
                impact=impact,
                recommendations=recommendations or [],
                implementation_priority=priority,
                assigned_to=assigned_to,
            )

            self.lessons_learned.append(lesson)

            self.logger.info(f"📚 Lesson learned added: {category} - {description}")
            return lesson_id

        except Exception as e:
            self.logger.error(f"Failed to add lesson learned: {e}")
            return ""

    def create_document(
        self,
        document_type: DocumentType,
        title: str,
        content: str,
        author: str,
        priority: DocumentPriority = DocumentPriority.MEDIUM,
        tags: Optional[List[str]] = None,
        related_emergencies: Optional[List[str]] = None,
    ) -> str:
        """Create an emergency document"""
        try:
            document_id = f"doc_{document_type.value}_{int(time.time())}"

            document = EmergencyDocument(
                document_id=document_id,
                document_type=document_type,
                title=title,
                content=content,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                author=author,
                priority=priority,
                tags=tags or [],
                related_emergencies=related_emergencies or [],
            )

            self.documents.append(document)

            # Maintain document limit
            if len(self.documents) > self.max_documents_retained:
                self.documents.pop(0)

            # Save document to file via distribution module
            save_document_to_file(self.documentation_path, document)

            self.logger.info(f"📄 Document created: {title} ({document_type.value})")
            return document_id

        except Exception as e:
            self.logger.error(f"Failed to create document: {e}")
            return ""

    def generate_emergency_report(
        self,
        emergency_id: str,
        include_timeline: bool = True,
        include_validation: bool = True,
        include_lessons: bool = True,
    ) -> str:
        """Generate a comprehensive emergency report"""
        try:
            # Find related events
            related_events = [
                e
                for e in self.emergency_events
                if emergency_id in e.event_id or emergency_id in e.tags
            ]

            # Find related timeline
            related_timeline = next(
                (t for t in self.response_timelines if t.emergency_id == emergency_id),
                None,
            )

            # Find related validations
            related_validations = [
                v for v in self.recovery_validations if v.recovery_id == emergency_id
            ]

            # Find related lessons
            related_lessons = [
                l for l in self.lessons_learned if l.emergency_id == emergency_id
            ]

            # Generate report content using template generator
            report_content = generate_report_content(
                emergency_id,
                related_events,
                related_timeline,
                related_validations,
                related_lessons,
            )

            # Create document
            document_id = self.create_document(
                document_type=DocumentType.INCIDENT_REPORT,
                title=f"Emergency Report - {emergency_id}",
                content=report_content,
                author="EmergencyDocumentation",
                priority=DocumentPriority.HIGH,
                tags=["emergency_report", "automated"],
                related_emergencies=[emergency_id],
            )

            self.logger.info(f"📊 Emergency report generated: {emergency_id}")
            return document_id

        except Exception as e:
            self.logger.error(f"Failed to generate emergency report: {e}")
            return ""

    def _get_timeline(self, timeline_id: str) -> Optional[ResponseTimeline]:
        """Get a timeline by ID"""
        return next(
            (t for t in self.response_timelines if t.timeline_id == timeline_id), None
        )

    def get_emergency_events(
        self,
        emergency_id: Optional[str] = None,
        event_type: Optional[str] = None,
        severity: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get emergency events with optional filtering"""
        try:
            filtered_events = self.emergency_events

            if emergency_id:
                filtered_events = [
                    e
                    for e in filtered_events
                    if emergency_id in e.event_id or emergency_id in e.tags
                ]

            if event_type:
                filtered_events = [
                    e for e in filtered_events if e.event_type == event_type
                ]

            if severity:
                filtered_events = [e for e in filtered_events if e.severity == severity]

            return [
                {
                    "event_id": e.event_id,
                    "timestamp": e.timestamp.isoformat(),
                    "event_type": e.event_type,
                    "description": e.description,
                    "source": e.source,
                    "severity": e.severity,
                    "affected_components": e.affected_components,
                    "details": e.details,
                    "tags": e.tags,
                }
                for e in filtered_events
            ]

        except Exception as e:
            self.logger.error(f"Failed to get emergency events: {e}")
            return []

    def get_documentation_summary(self) -> Dict[str, Any]:
        """Get documentation system summary"""
        try:
            return {
                "total_events": len(self.emergency_events),
                "total_timelines": len(self.response_timelines),
                "total_validations": len(self.recovery_validations),
                "total_lessons": len(self.lessons_learned),
                "total_documents": len(self.documents),
                "documentation_path": str(self.documentation_path),
                "auto_save_interval": self.auto_save_interval,
                "max_events_retained": self.max_events_retained,
                "max_documents_retained": self.max_documents_retained,
            }

        except Exception as e:
            self.logger.error(f"Failed to get documentation summary: {e}")
            return {"error": str(e)}

    def health_check(self) -> Dict[str, Any]:
        """Health check for the emergency documentation system"""
        try:
            return {
                "is_healthy": True,
                "total_events": len(self.emergency_events),
                "total_timelines": len(self.response_timelines),
                "total_validations": len(self.recovery_validations),
                "total_lessons": len(self.lessons_learned),
                "total_documents": len(self.documents),
                "documentation_directory_exists": self.documentation_path.exists(),
                "documentation_directory_writable": self.documentation_path.is_dir(),
            }

        except Exception as e:
            return {"is_healthy": False, "error": str(e)}


# Export the main classes
__all__ = [
    "EmergencyDocumentation",
    "EmergencyEvent",
    "ResponseTimeline",
    "RecoveryValidation",
    "LessonsLearned",
    "EmergencyDocument",
    "DocumentType",
    "DocumentPriority",
]
