#!/usr/bin/env python3
"""
Protocol Governance System - Prevents Unnecessary Protocol Creation
Agent-3: Infrastructure & DevOps Specialist
Mission: V3 Infrastructure Deployment
"""

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any


class ProtocolType(Enum):
    """Types of protocols that can be created"""

    GIT_WORKFLOW = "git_workflow"
    CODE_QUALITY = "code_quality"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    DOCUMENTATION = "documentation"
    AGENT_COORDINATION = "agent_coordination"
    EMERGENCY = "emergency"
    TOOL_DEVELOPMENT = "tool_development"
    COMMUNICATION = "communication"
    QUALITY_ASSURANCE = "quality_assurance"


class ProtocolStatus(Enum):
    """Status of protocol proposals"""

    PROPOSED = "proposed"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    IMPLEMENTED = "implemented"
    DEPRECATED = "deprecated"


class RejectionReason(Enum):
    """Reasons for protocol rejection"""

    DUPLICATE = "duplicate"
    UNNECESSARY = "unnecessary"
    OVERCOMPLEX = "overcomplex"
    CONFLICTS = "conflicts"
    INSUFFICIENT_JUSTIFICATION = "insufficient_justification"
    ALREADY_COVERED = "already_covered"
    OUT_OF_SCOPE = "out_of_scope"


@dataclass
class ProtocolProposal:
    """Protocol proposal data structure"""

    proposal_id: str
    title: str
    description: str
    protocol_type: ProtocolType
    proposed_by: str
    justification: str
    existing_solutions: list[str]
    created_at: str
    status: ProtocolStatus
    rejection_reason: RejectionReason | None = None
    review_comments: list[str] = None
    approved_by: str | None = None
    implementation_notes: str | None = None


@dataclass
class ExistingProtocol:
    """Existing protocol reference"""

    name: str
    file_path: str
    description: str
    protocol_type: ProtocolType
    last_updated: str
    coverage_areas: list[str]


class ProtocolGovernanceSystem:
    """System to prevent unnecessary protocol creation"""

    def __init__(
        self, protocols_dir: str = "docs", proposals_file: str = "protocol_proposals.json"
    ):
        self.protocols_dir = Path(protocols_dir)
        self.proposals_file = Path(proposals_file)
        self.existing_protocols = self._load_existing_protocols()
        self.proposals = self._load_proposals()

    def _load_existing_protocols(self) -> list[ExistingProtocol]:
        """Load all existing protocols from the docs directory"""
        protocols = []

        # Known protocol files
        protocol_files = [
            (
                "AGENT_PROTOCOL_SYSTEM.md",
                ProtocolType.AGENT_COORDINATION,
                "Comprehensive agent workflow protocols",
            ),
            (
                "AGENT_PROTOCOL_QUICK_REFERENCE.md",
                ProtocolType.AGENT_COORDINATION,
                "Quick reference for agent protocols",
            ),
            (
                "CAPTAIN_AUTONOMOUS_PROTOCOL.md",
                ProtocolType.AGENT_COORDINATION,
                "Captain autonomous operation protocols",
            ),
            (
                "CAPTAIN_ONBOARDING_GUIDE.md",
                ProtocolType.AGENT_COORDINATION,
                "Captain onboarding procedures",
            ),
            ("AGENT_KNOWLEDGE_BASE.md", ProtocolType.DOCUMENTATION, "Knowledge base and solutions"),
            (
                "TOOL_ECOSYSTEM_ANALYSIS.md",
                ProtocolType.TOOL_DEVELOPMENT,
                "Tool development guidelines",
            ),
            (
                "AGENT_WORKFLOW_AUTOMATION.md",
                ProtocolType.AGENT_COORDINATION,
                "Workflow automation protocols",
            ),
            (
                "GITHUB_AGENT_CLIENT.md",
                ProtocolType.TOOL_DEVELOPMENT,
                "GitHub integration protocols",
            ),
        ]

        for filename, protocol_type, description in protocol_files:
            file_path = self.protocols_dir / filename
            if file_path.exists():
                protocols.append(
                    ExistingProtocol(
                        name=filename.replace(".md", "").replace("_", " ").title(),
                        file_path=str(file_path),
                        description=description,
                        protocol_type=protocol_type,
                        last_updated=self._get_file_modified_time(file_path),
                        coverage_areas=self._extract_coverage_areas(file_path),
                    )
                )

        return protocols

    def _get_file_modified_time(self, file_path: Path) -> str:
        """Get file modification time"""
        try:
            timestamp = file_path.stat().st_mtime
            return datetime.fromtimestamp(timestamp).isoformat()
        except:
            return datetime.now().isoformat()

    def _extract_coverage_areas(self, file_path: Path) -> list[str]:
        """Extract coverage areas from protocol file"""
        try:
            content = file_path.read_text(encoding="utf-8")
            # Look for section headers to identify coverage areas
            coverage_areas = []
            for line in content.split("\n"):
                if line.startswith("## ") and "PROTOCOL" in line.upper():
                    coverage_areas.append(line.replace("## ", "").strip())
            return coverage_areas
        except:
            return []

    def _load_proposals(self) -> list[ProtocolProposal]:
        """Load existing protocol proposals"""
        if self.proposals_file.exists():
            try:
                with open(self.proposals_file) as f:
                    data = json.load(f)
                    return [ProtocolProposal(**proposal) for proposal in data]
            except:
                return []
        return []

    def _save_proposals(self):
        """Save protocol proposals to file"""
        with open(self.proposals_file, "w") as f:
            data = [asdict(proposal) for proposal in self.proposals]
            json.dump(data, f, indent=2, default=str)

    def propose_protocol(
        self,
        title: str,
        description: str,
        protocol_type: ProtocolType,
        proposed_by: str,
        justification: str,
    ) -> dict[str, Any]:
        """Propose a new protocol with governance checks"""

        # Check for duplicates and unnecessary protocols
        validation_result = self._validate_proposal(
            title, description, protocol_type, justification
        )

        if not validation_result["approved"]:
            return {
                "status": "rejected",
                "reason": validation_result["reason"],
                "suggestions": validation_result["suggestions"],
                "existing_solutions": validation_result["existing_solutions"],
            }

        # Create proposal
        proposal_id = f"PROTOCOL_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{proposed_by}"

        proposal = ProtocolProposal(
            proposal_id=proposal_id,
            title=title,
            description=description,
            protocol_type=protocol_type,
            proposed_by=proposed_by,
            justification=justification,
            existing_solutions=validation_result["existing_solutions"],
            created_at=datetime.now().isoformat(),
            status=ProtocolStatus.PROPOSED,
            review_comments=[],
        )

        self.proposals.append(proposal)
        self._save_proposals()

        return {
            "status": "proposed",
            "proposal_id": proposal_id,
            "next_steps": "Awaiting review by protocol governance team",
            "existing_solutions": validation_result["existing_solutions"],
        }

    def _validate_proposal(
        self, title: str, description: str, protocol_type: ProtocolType, justification: str
    ) -> dict[str, Any]:
        """Validate protocol proposal against existing protocols"""

        # Check for duplicates
        duplicate_check = self._check_duplicates(title, description, protocol_type)
        if duplicate_check["is_duplicate"]:
            return {
                "approved": False,
                "reason": RejectionReason.DUPLICATE,
                "suggestions": [
                    "Use existing protocol",
                    "Extend existing protocol",
                    "Reference existing protocol",
                ],
                "existing_solutions": duplicate_check["existing_solutions"],
            }

        # Check for unnecessary complexity
        if self._is_unnecessarily_complex(description, justification):
            return {
                "approved": False,
                "reason": RejectionReason.OVERCOMPLEX,
                "suggestions": [
                    "Simplify the approach",
                    "Break into smaller protocols",
                    "Use existing tools",
                ],
                "existing_solutions": [],
            }

        # Check if already covered
        coverage_check = self._check_coverage(protocol_type, description)
        if coverage_check["already_covered"]:
            return {
                "approved": False,
                "reason": RejectionReason.ALREADY_COVERED,
                "suggestions": [
                    "Reference existing protocol",
                    "Extend existing protocol",
                    "Use existing solution",
                ],
                "existing_solutions": coverage_check["existing_solutions"],
            }

        # Check justification quality
        if not self._has_strong_justification(justification):
            return {
                "approved": False,
                "reason": RejectionReason.INSUFFICIENT_JUSTIFICATION,
                "suggestions": [
                    "Provide specific use cases",
                    "Document pain points",
                    "Show measurable benefits",
                ],
                "existing_solutions": [],
            }

        return {
            "approved": True,
            "existing_solutions": self._find_relevant_protocols(protocol_type),
        }

    def _check_duplicates(
        self, title: str, description: str, protocol_type: ProtocolType
    ) -> dict[str, Any]:
        """Check for duplicate protocols"""
        existing_solutions = []

        for protocol in self.existing_protocols:
            # Check title similarity
            if self._calculate_similarity(title.lower(), protocol.name.lower()) > 0.7:
                existing_solutions.append(f"{protocol.name} ({protocol.file_path})")

            # Check description similarity
            if self._calculate_similarity(description.lower(), protocol.description.lower()) > 0.6:
                existing_solutions.append(f"{protocol.name} ({protocol.file_path})")

            # Check type match
            if protocol.protocol_type == protocol_type:
                existing_solutions.append(f"{protocol.name} ({protocol.file_path})")

        return {
            "is_duplicate": len(existing_solutions) > 0,
            "existing_solutions": list(set(existing_solutions)),
        }

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity using simple word overlap"""
        words1 = set(text1.split())
        words2 = set(text2.split())

        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union)

    def _is_unnecessarily_complex(self, description: str, justification: str) -> bool:
        """Check if proposal is unnecessarily complex"""
        # Simple heuristics for complexity
        complexity_indicators = [
            len(description) > 1000,  # Very long description
            "multiple" in description.lower() and "protocols" in description.lower(),
            "comprehensive" in description.lower() and "framework" in description.lower(),
            justification.count("because") > 3,  # Too many justifications
            "complex" in description.lower() or "complicated" in description.lower(),
        ]

        return sum(complexity_indicators) >= 2

    def _check_coverage(self, protocol_type: ProtocolType, description: str) -> dict[str, Any]:
        """Check if area is already covered by existing protocols"""
        existing_solutions = []

        for protocol in self.existing_protocols:
            if protocol.protocol_type == protocol_type:
                # Check if description overlaps with coverage areas
                for area in protocol.coverage_areas:
                    if self._calculate_similarity(description.lower(), area.lower()) > 0.5:
                        existing_solutions.append(f"{protocol.name} - {area}")

        return {
            "already_covered": len(existing_solutions) > 0,
            "existing_solutions": existing_solutions,
        }

    def _has_strong_justification(self, justification: str) -> bool:
        """Check if justification is strong enough"""
        if len(justification) < 50:
            return False

        strong_indicators = [
            "pain point" in justification.lower(),
            "problem" in justification.lower(),
            "issue" in justification.lower(),
            "need" in justification.lower(),
            "requirement" in justification.lower(),
            "improve" in justification.lower(),
            "efficiency" in justification.lower(),
            "quality" in justification.lower(),
        ]

        return sum(strong_indicators) >= 2

    def _find_relevant_protocols(self, protocol_type: ProtocolType) -> list[str]:
        """Find relevant existing protocols"""
        relevant = []
        for protocol in self.existing_protocols:
            if protocol.protocol_type == protocol_type:
                relevant.append(f"{protocol.name} ({protocol.file_path})")
        return relevant

    def get_protocol_inventory(self) -> dict[str, Any]:
        """Get inventory of all existing protocols"""
        inventory = {
            "total_protocols": len(self.existing_protocols),
            "by_type": {},
            "recent_updates": [],
            "coverage_analysis": {},
        }

        # Group by type
        for protocol in self.existing_protocols:
            protocol_type = protocol.protocol_type.value
            if protocol_type not in inventory["by_type"]:
                inventory["by_type"][protocol_type] = []
            inventory["by_type"][protocol_type].append(
                {
                    "name": protocol.name,
                    "file_path": protocol.file_path,
                    "last_updated": protocol.last_updated,
                    "coverage_areas": protocol.coverage_areas,
                }
            )

        # Recent updates (last 30 days)
        cutoff_date = datetime.now() - timedelta(days=30)
        for protocol in self.existing_protocols:
            try:
                last_updated = datetime.fromisoformat(protocol.last_updated)
                if last_updated > cutoff_date:
                    inventory["recent_updates"].append(
                        {
                            "name": protocol.name,
                            "last_updated": protocol.last_updated,
                            "type": protocol.protocol_type.value,
                        }
                    )
            except:
                continue

        # Coverage analysis
        all_coverage_areas = []
        for protocol in self.existing_protocols:
            all_coverage_areas.extend(protocol.coverage_areas)

        coverage_counts = {}
        for area in all_coverage_areas:
            coverage_counts[area] = coverage_counts.get(area, 0) + 1

        inventory["coverage_analysis"] = coverage_counts

        return inventory

    def suggest_alternatives(self, protocol_type: ProtocolType, description: str) -> list[str]:
        """Suggest alternatives to creating new protocol"""
        suggestions = []

        # Find existing protocols of same type
        same_type_protocols = [
            p for p in self.existing_protocols if p.protocol_type == protocol_type
        ]

        if same_type_protocols:
            suggestions.append(f"Consider extending existing {protocol_type.value} protocols:")
            for protocol in same_type_protocols:
                suggestions.append(f"  - {protocol.name} ({protocol.file_path})")

        # Suggest using existing tools
        if protocol_type == ProtocolType.TOOL_DEVELOPMENT:
            suggestions.append("Consider using existing tools in tools/ directory")

        # Suggest knowledge base
        suggestions.append("Check AGENT_KNOWLEDGE_BASE.md for existing solutions")

        # Suggest quick reference
        suggestions.append("Use AGENT_PROTOCOL_QUICK_REFERENCE.md for quick answers")

        return suggestions


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="Protocol Governance System")
    parser.add_argument("--propose", action="store_true", help="Propose a new protocol")
    parser.add_argument("--inventory", action="store_true", help="Show protocol inventory")
    parser.add_argument("--validate", action="store_true", help="Validate existing protocols")
    parser.add_argument("--title", help="Protocol title")
    parser.add_argument("--description", help="Protocol description")
    parser.add_argument("--type", help="Protocol type", choices=[t.value for t in ProtocolType])
    parser.add_argument("--justification", help="Justification for protocol")
    parser.add_argument("--proposed-by", help="Agent proposing protocol")

    args = parser.parse_args()

    governance = ProtocolGovernanceSystem()

    if args.inventory:
        inventory = governance.get_protocol_inventory()
        print("📋 PROTOCOL INVENTORY")
        print("=" * 50)
        print(f"Total Protocols: {inventory['total_protocols']}")
        print(f"Recent Updates: {len(inventory['recent_updates'])}")
        print("\n📊 By Type:")
        for protocol_type, protocols in inventory["by_type"].items():
            print(f"  {protocol_type}: {len(protocols)}")
        print("\n🔄 Recent Updates:")
        for update in inventory["recent_updates"]:
            print(f"  - {update['name']} ({update['last_updated']})")

    elif args.propose:
        if not all([args.title, args.description, args.type, args.justification, args.proposed_by]):
            print(
                "❌ ERROR: All fields required for proposal: --title, --description, --type, --justification, --proposed-by"
            )
            return

        protocol_type = ProtocolType(args.type)
        result = governance.propose_protocol(
            args.title, args.description, protocol_type, args.proposed_by, args.justification
        )

        print("📋 PROTOCOL PROPOSAL RESULT")
        print("=" * 50)
        print(f"Status: {result['status'].upper()}")

        if result["status"] == "rejected":
            print(f"Reason: {result['reason'].value}")
            print("\n💡 Suggestions:")
            for suggestion in result["suggestions"]:
                print(f"  - {suggestion}")
            if result["existing_solutions"]:
                print("\n🔍 Existing Solutions:")
                for solution in result["existing_solutions"]:
                    print(f"  - {solution}")
        else:
            print(f"Proposal ID: {result['proposal_id']}")
            print(f"Next Steps: {result['next_steps']}")

    else:
        print("📋 PROTOCOL GOVERNANCE SYSTEM")
        print("=" * 50)
        print("Available commands:")
        print("  --inventory     Show protocol inventory")
        print("  --propose       Propose new protocol")
        print("  --validate      Validate existing protocols")
        print("\nExample:")
        print("  python protocol_governance_system.py --inventory")
        print(
            "  python protocol_governance_system.py --propose --title 'New Protocol' --description 'Description' --type git_workflow --justification 'Need for standardization' --proposed-by Agent-3"
        )


if __name__ == "__main__":
    main()
