#!/usr/bin/env python3
"""
Protocol Reference Enforcer
===========================

Tool to enforce protocol reference requirements for agents.
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ComplianceStatus(Enum):
    """Compliance status enumeration."""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIAL = "partial"
    UNKNOWN = "unknown"


@dataclass
class ProtocolReference:
    """Protocol reference data structure."""
    protocol_name: str
    section: str
    citation: str
    compliance_status: ComplianceStatus
    violation_reason: Optional[str] = None


@dataclass
class ComplianceReport:
    """Compliance report data structure."""
    agent_id: str
    response_id: str
    timestamp: str
    protocol_references: List[ProtocolReference]
    overall_compliance: ComplianceStatus
    violations: List[str]
    recommendations: List[str]


class ProtocolReferenceEnforcer:
    """Enforce protocol reference requirements for agents."""
    
    def __init__(self, protocol_dir: str = "docs"):
        """Initialize the protocol reference enforcer."""
        self.protocol_dir = Path(protocol_dir)
        self.protocol_files = [
            "AGENT_PROTOCOL_SYSTEM.md",
            "AGENT_PROTOCOL_QUICK_REFERENCE.md",
            "PROTOCOL_CREATION_GUIDELINES.md",
            "AGENT_KNOWLEDGE_BASE.md"
        ]
        
    def check_protocol_reference(self, response_text: str, agent_id: str) -> ComplianceReport:
        """Check if response includes proper protocol references."""
        violations = []
        recommendations = []
        protocol_references = []
        
        # Check for protocol citation section
        if "## 📚 **PROTOCOL REFERENCE:**" not in response_text:
            violations.append("Missing protocol reference section")
            recommendations.append("Add '## 📚 **PROTOCOL REFERENCE:**' section to response")
        
        # Check for compliance checklist
        if "## ✅ **COMPLIANCE CHECKLIST:**" not in response_text:
            violations.append("Missing compliance checklist")
            recommendations.append("Add '## ✅ **COMPLIANCE CHECKLIST:**' section to response")
        
        # Check for cycle-based timeline usage
        if "cycle" not in response_text.lower() and ("hour" in response_text.lower() or "day" in response_text.lower() or "week" in response_text.lower()):
            violations.append("Using traditional time units instead of cycle-based timeline")
            recommendations.append("Use cycle-based timeline (288-720 cycles = 1 day)")
        
        # Check for messaging system usage
        if "messaging" in response_text.lower() and "consolidated_messaging_service.py" not in response_text:
            violations.append("Mentioned messaging but didn't use proper messaging system")
            recommendations.append("Use consolidated_messaging_service.py for agent communication")
        
        # Check for protocol citation content
        if "**Primary Protocol:**" not in response_text:
            violations.append("Missing primary protocol citation")
            recommendations.append("Include '**Primary Protocol:**' in protocol reference section")
        
        # Determine overall compliance
        if not violations:
            overall_compliance = ComplianceStatus.COMPLIANT
        elif len(violations) <= 2:
            overall_compliance = ComplianceStatus.PARTIAL
        else:
            overall_compliance = ComplianceStatus.NON_COMPLIANT
        
        # Create protocol references
        if "**Primary Protocol:**" in response_text:
            protocol_references.append(ProtocolReference(
                protocol_name="Agent Protocol System",
                section="Communication Protocols",
                citation="Referenced in response",
                compliance_status=ComplianceStatus.COMPLIANT
            ))
        
        return ComplianceReport(
            agent_id=agent_id,
            response_id=f"response_{agent_id}_{hash(response_text)}",
            timestamp=str(Path().cwd()),
            protocol_references=protocol_references,
            overall_compliance=overall_compliance,
            violations=violations,
            recommendations=recommendations
        )
    
    def generate_compliance_template(self) -> str:
        """Generate a compliance template for responses."""
        return """
## 📚 **PROTOCOL REFERENCE:**
- **Primary Protocol**: [Protocol Name] - [Section]
- **Messaging Protocol**: [Messaging System Requirements]
- **Timeline Protocol**: [Cycle-based Timeline Standards]
- **Compliance Status**: [✅ Compliant / ❌ Non-compliant]

## ✅ **COMPLIANCE CHECKLIST:**
- [ ] Messaging system used correctly
- [ ] Timeline expressed in cycles
- [ ] Communication format follows protocol
- [ ] Escalation procedures followed if needed

## 🚨 **PROTOCOL VIOLATIONS IDENTIFIED:**
[List any protocol violations and corrective actions]

## 🔧 **CORRECTIVE ACTIONS:**
[List corrective actions taken to ensure compliance]
"""
    
    def validate_messaging_usage(self, response_text: str) -> Tuple[bool, str]:
        """Validate proper messaging system usage."""
        if "send message" in response_text.lower() or "message agent" in response_text.lower():
            if "consolidated_messaging_service.py" in response_text:
                return True, "Proper messaging system used"
            else:
                return False, "Mentioned messaging but didn't use proper messaging system"
        return True, "No messaging mentioned"
    
    def validate_timeline_usage(self, response_text: str) -> Tuple[bool, str]:
        """Validate cycle-based timeline usage."""
        if "hour" in response_text.lower() or "day" in response_text.lower() or "week" in response_text.lower():
            if "cycle" in response_text.lower():
                return True, "Cycle-based timeline used correctly"
            else:
                return False, "Using traditional time units instead of cycle-based timeline"
        return True, "No timeline mentioned"
    
    def generate_violation_report(self, report: ComplianceReport) -> str:
        """Generate a violation report."""
        report_text = f"""
# Protocol Compliance Report

**Agent**: {report.agent_id}  
**Response ID**: {report.response_id}  
**Timestamp**: {report.timestamp}  
**Overall Compliance**: {report.overall_compliance.value.upper()}

## 🚨 **VIOLATIONS IDENTIFIED:**
"""
        
        for i, violation in enumerate(report.violations, 1):
            report_text += f"{i}. {violation}\n"
        
        if report.recommendations:
            report_text += "\n## 🔧 **RECOMMENDATIONS:**\n"
            for i, recommendation in enumerate(report.recommendations, 1):
                report_text += f"{i}. {recommendation}\n"
        
        return report_text
    
    def save_compliance_report(self, report: ComplianceReport, output_file: str):
        """Save compliance report to file."""
        report_data = {
            "agent_id": report.agent_id,
            "response_id": report.response_id,
            "timestamp": report.timestamp,
            "overall_compliance": report.overall_compliance.value,
            "violations": report.violations,
            "recommendations": report.recommendations,
            "protocol_references": [
                {
                    "protocol_name": ref.protocol_name,
                    "section": ref.section,
                    "citation": ref.citation,
                    "compliance_status": ref.compliance_status.value
                }
                for ref in report.protocol_references
            ]
        }
        
        with open(output_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        logger.info(f"Compliance report saved to {output_file}")


def main():
    """Main function for protocol reference enforcer."""
    parser = argparse.ArgumentParser(description="Enforce protocol reference requirements")
    parser.add_argument("--check", help="Check protocol compliance of response text")
    parser.add_argument("--agent", help="Agent ID for compliance check")
    parser.add_argument("--template", action="store_true", help="Generate compliance template")
    parser.add_argument("--output", help="Output file for compliance report")
    
    args = parser.parse_args()
    
    enforcer = ProtocolReferenceEnforcer()
    
    if args.template:
        template = enforcer.generate_compliance_template()
        print(template)
        return
    
    if args.check and args.agent:
        # Read response text from file or stdin
        if Path(args.check).exists():
            with open(args.check, 'r') as f:
                response_text = f.read()
        else:
            response_text = args.check
        
        # Check compliance
        report = enforcer.check_protocol_reference(response_text, args.agent)
        
        # Generate report
        violation_report = enforcer.generate_violation_report(report)
        print(violation_report)
        
        # Save report if output file specified
        if args.output:
            enforcer.save_compliance_report(report, args.output)
    
    else:
        print("Usage: python protocol_reference_enforcer.py --check <response_text> --agent <agent_id>")
        print("       python protocol_reference_enforcer.py --template")


if __name__ == "__main__":
    main()


