#!/usr/bin/env python3
"""
Strategic Consultation Core
==========================
Core logic for Thea strategic consultation system.
V2 Compliant: ≤400 lines, focused consultation functionality

Author: Agent-7 (Implementation Specialist)
License: MIT
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class StrategicConsultationCore:
    """Core strategic consultation functionality for Thea."""

    def __init__(self, project_root: str = "."):
        """Initialize strategic consultation core."""
        self.project_root = Path(project_root)
        self.consultation_dir = self.project_root / "consultations"
        self.templates_dir = self.project_root / "src" / "services" / "thea"

        # Ensure directories exist
        self.consultation_dir.mkdir(exist_ok=True)

        # Load templates
        self.templates = self._load_templates()

        logger.info("StrategicConsultationCore initialized")

    def _load_templates(self) -> dict[str, dict[str, Any]]:
        """Load consultation templates."""
        try:
            templates_file = self.templates_dir / "strategic_consultation_templates.py"
            if templates_file.exists():
                # Import templates dynamically
                import sys

                sys.path.append(str(self.templates_dir))
                from strategic_consultation_templates import STRATEGIC_TEMPLATES

                return STRATEGIC_TEMPLATES
            else:
                return self._get_default_templates()
        except Exception as e:
            logger.warning(f"Failed to load templates: {e}, using defaults")
            return self._get_default_templates()

    def _get_default_templates(self) -> dict[str, dict[str, Any]]:
        """Get default consultation templates."""
        return {
            "priority_guidance": {
                "name": "Priority Guidance",
                "description": "Strategic guidance for task prioritization",
                "context": "project_analysis",
                "output_format": "recommendations",
            },
            "crisis_response": {
                "name": "Crisis Response",
                "description": "Emergency consultation for critical issues",
                "context": "system_health",
                "output_format": "action_plan",
            },
            "strategic_planning": {
                "name": "Strategic Planning",
                "description": "Long-term strategic planning consultation",
                "context": "project_roadmap",
                "output_format": "strategic_plan",
            },
            "quality_assessment": {
                "name": "Quality Assessment",
                "description": "Quality and compliance assessment",
                "context": "quality_metrics",
                "output_format": "assessment_report",
            },
        }

    def consult_command(
        self, question: str, template: str = None, context: str = None
    ) -> dict[str, Any]:
        """Execute strategic consultation command."""
        try:
            logger.info(
                f"Starting consultation: template={template}, question='{question[:50]}...'"
            )

            # Prepare consultation request
            consultation_request = self._prepare_consultation_request(question, template, context)

            # Execute consultation
            consultation_result = self._execute_consultation(consultation_request)

            # Store consultation
            consultation_id = self._store_consultation(consultation_request, consultation_result)

            # Format response
            response = self._format_consultation_response(consultation_result, consultation_id)

            logger.info(f"Consultation completed: {consultation_id}")
            return response

        except Exception as e:
            logger.error(f"Consultation failed: {e}")
            return {"success": False, "error": str(e), "consultation_id": None}

    def _prepare_consultation_request(
        self, question: str, template: str, context: str
    ) -> dict[str, Any]:
        """Prepare consultation request."""
        request = {
            "question": question,
            "template": template or "priority_guidance",
            "context": context or "general",
            "timestamp": datetime.now().isoformat(),
            "request_id": f"consult_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        }

        # Add template context if available
        if template and template in self.templates:
            request["template_info"] = self.templates[template]

        return request

    def _execute_consultation(self, request: dict[str, Any]) -> dict[str, Any]:
        """Execute the consultation logic."""
        # For now, return a structured response
        # In a full implementation, this would integrate with Thea's AI

        question = request["question"]
        template = request["template"]

        # Generate consultation response based on template
        if template == "priority_guidance":
            response = self._generate_priority_guidance(question)
        elif template == "crisis_response":
            response = self._generate_crisis_response(question)
        elif template == "strategic_planning":
            response = self._generate_strategic_planning(question)
        elif template == "quality_assessment":
            response = self._generate_quality_assessment(question)
        else:
            response = self._generate_general_consultation(question)

        return {
            "template": template,
            "question": question,
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "status": "completed",
        }

    def _generate_priority_guidance(self, question: str) -> dict[str, Any]:
        """Generate priority guidance response."""
        return {
            "type": "priority_guidance",
            "recommendations": [
                "Focus on high-impact, low-effort tasks first",
                "Address critical system issues before feature development",
                "Prioritize V2 compliance and quality gates",
                "Consider agent workload balancing",
            ],
            "next_steps": [
                "Review current task backlog",
                "Assess agent availability and capabilities",
                "Implement priority matrix for task selection",
            ],
            "confidence": "high",
        }

    def _generate_crisis_response(self, question: str) -> dict[str, Any]:
        """Generate crisis response."""
        return {
            "type": "crisis_response",
            "severity": "medium",
            "immediate_actions": [
                "Assess system health and stability",
                "Identify root cause of crisis",
                "Implement containment measures",
                "Activate emergency protocols if needed",
            ],
            "recovery_plan": [
                "Document crisis details and timeline",
                "Implement fixes and safeguards",
                "Review and update crisis response procedures",
                "Conduct post-crisis analysis",
            ],
            "confidence": "high",
        }

    def _generate_strategic_planning(self, question: str) -> dict[str, Any]:
        """Generate strategic planning response."""
        return {
            "type": "strategic_planning",
            "vision": "Enhanced swarm coordination and autonomous development",
            "strategic_goals": [
                "Improve agent coordination efficiency",
                "Enhance system reliability and performance",
                "Implement advanced AI-driven development workflows",
                "Strengthen quality assurance and compliance",
            ],
            "roadmap": [
                "Phase 1: System stabilization and optimization",
                "Phase 2: Advanced coordination features",
                "Phase 3: AI-driven autonomous development",
                "Phase 4: Full swarm intelligence implementation",
            ],
            "confidence": "medium",
        }

    def _generate_quality_assessment(self, question: str) -> dict[str, Any]:
        """Generate quality assessment response."""
        return {
            "type": "quality_assessment",
            "overall_quality": "good",
            "strengths": [
                "Strong V2 compliance in core modules",
                "Good separation of concerns",
                "Comprehensive logging and monitoring",
            ],
            "areas_for_improvement": [
                "Reduce function complexity in some modules",
                "Improve test coverage",
                "Optimize performance bottlenecks",
            ],
            "recommendations": [
                "Continue V2 compliance enforcement",
                "Implement automated quality gates",
                "Regular code review and refactoring",
            ],
            "confidence": "high",
        }

    def _generate_general_consultation(self, question: str) -> dict[str, Any]:
        """Generate general consultation response."""
        return {
            "type": "general_consultation",
            "analysis": f"Based on your question: '{question}'",
            "insights": [
                "Consider the broader system context",
                "Evaluate impact on other components",
                "Assess resource requirements and constraints",
            ],
            "suggestions": [
                "Gather more context if needed",
                "Consider multiple solution approaches",
                "Plan for implementation and testing",
            ],
            "confidence": "medium",
        }

    def _store_consultation(self, request: dict[str, Any], result: dict[str, Any]) -> str:
        """Store consultation in database."""
        consultation_id = request["request_id"]

        consultation_record = {
            "id": consultation_id,
            "request": request,
            "result": result,
            "created_at": datetime.now().isoformat(),
        }

        # Store in JSON file
        consultation_file = self.consultation_dir / f"{consultation_id}.json"
        with open(consultation_file, "w") as f:
            json.dump(consultation_record, f, indent=2)

        return consultation_id

    def _format_consultation_response(
        self, result: dict[str, Any], consultation_id: str
    ) -> dict[str, Any]:
        """Format consultation response."""
        return {
            "success": True,
            "consultation_id": consultation_id,
            "template": result["template"],
            "response": result["response"],
            "timestamp": result["timestamp"],
            "status": result["status"],
        }

    def get_consultation_history(self, limit: int = 10) -> list[dict[str, Any]]:
        """Get consultation history."""
        consultations = []

        try:
            consultation_files = sorted(
                self.consultation_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True
            )

            for file_path in consultation_files[:limit]:
                with open(file_path) as f:
                    consultation = json.load(f)
                    consultations.append(consultation)

        except Exception as e:
            logger.error(f"Failed to load consultation history: {e}")

        return consultations

    def get_available_templates(self) -> dict[str, dict[str, Any]]:
        """Get available consultation templates."""
        return self.templates


def consult_command(question: str, template: str = None, context: str = None) -> dict[str, Any]:
    """Convenience function for consultation command."""
    core = StrategicConsultationCore()
    return core.consult_command(question, template, context)


def main():
    """Test the strategic consultation core."""
    print("🎯 Strategic Consultation Core Test")
    print("=" * 50)

    core = StrategicConsultationCore()

    # Test consultation
    result = core.consult_command(
        "What should be our next priority for the project?", template="priority_guidance"
    )

    print(f"✅ Consultation result: {result['success']}")
    print(f"📋 Consultation ID: {result['consultation_id']}")
    print(f"🎯 Template: {result['template']}")

    # Test templates
    templates = core.get_available_templates()
    print(f"\n📚 Available templates: {len(templates)}")
    for name, info in templates.items():
        print(f"   • {name}: {info['name']}")

    print("\n🎉 Strategic Consultation Core test completed!")


if __name__ == "__main__":
    main()
