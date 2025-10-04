#!/usr/bin/env python3
"""
Strategic Consultation Templates
===============================
Template system for Thea strategic consultation.
V2 Compliant: ≤400 lines, focused template management

Author: Agent-7 (Implementation Specialist)
License: MIT
"""

from typing import Any, Dict


# Strategic Consultation Templates
STRATEGIC_TEMPLATES = {
    "priority_guidance": {
        "name": "Priority Guidance",
        "description": "Strategic guidance for task prioritization and resource allocation",
        "context": "project_analysis",
        "output_format": "recommendations",
        "use_cases": [
            "Task prioritization decisions",
            "Resource allocation planning",
            "Sprint planning and backlog management",
            "Agent workload balancing"
        ],
        "input_requirements": [
            "Current project status",
            "Available resources",
            "Timeline constraints",
            "Quality requirements"
        ]
    },
    
    "crisis_response": {
        "name": "Crisis Response",
        "description": "Emergency consultation for critical system issues and crisis management",
        "context": "system_health",
        "output_format": "action_plan",
        "use_cases": [
            "System failures and outages",
            "Security incidents",
            "Performance degradation",
            "Critical bugs and errors"
        ],
        "input_requirements": [
            "Crisis description",
            "Impact assessment",
            "Current system state",
            "Available resources"
        ]
    },
    
    "strategic_planning": {
        "name": "Strategic Planning",
        "description": "Long-term strategic planning and roadmap development",
        "context": "project_roadmap",
        "output_format": "strategic_plan",
        "use_cases": [
            "Long-term project planning",
            "Architecture decisions",
            "Technology stack selection",
            "Team structure planning"
        ],
        "input_requirements": [
            "Project goals and objectives",
            "Current capabilities",
            "Market conditions",
            "Resource constraints"
        ]
    },
    
    "quality_assessment": {
        "name": "Quality Assessment",
        "description": "Quality and compliance assessment with improvement recommendations",
        "context": "quality_metrics",
        "output_format": "assessment_report",
        "use_cases": [
            "Code quality reviews",
            "V2 compliance assessment",
            "Performance evaluation",
            "Security audit"
        ],
        "input_requirements": [
            "Quality metrics data",
            "Compliance requirements",
            "Performance benchmarks",
            "Security standards"
        ]
    },
    
    "architecture_review": {
        "name": "Architecture Review",
        "description": "System architecture analysis and improvement recommendations",
        "context": "system_architecture",
        "output_format": "architecture_analysis",
        "use_cases": [
            "System design reviews",
            "Architecture optimization",
            "Scalability planning",
            "Technical debt assessment"
        ],
        "input_requirements": [
            "Current architecture documentation",
            "Performance requirements",
            "Scalability needs",
            "Technology constraints"
        ]
    },
    
    "team_coordination": {
        "name": "Team Coordination",
        "description": "Agent coordination and team management guidance",
        "context": "swarm_coordination",
        "output_format": "coordination_plan",
        "use_cases": [
            "Agent role assignment",
            "Workflow optimization",
            "Communication protocols",
            "Conflict resolution"
        ],
        "input_requirements": [
            "Team composition",
            "Current workflows",
            "Communication patterns",
            "Performance metrics"
        ]
    },
    
    "performance_optimization": {
        "name": "Performance Optimization",
        "description": "System performance analysis and optimization recommendations",
        "context": "performance_metrics",
        "output_format": "optimization_plan",
        "use_cases": [
            "Performance bottleneck analysis",
            "Resource optimization",
            "Scalability improvements",
            "Efficiency enhancements"
        ],
        "input_requirements": [
            "Performance metrics",
            "System load data",
            "Resource utilization",
            "Performance goals"
        ]
    },
    
    "risk_assessment": {
        "name": "Risk Assessment",
        "description": "Risk analysis and mitigation strategy development",
        "context": "risk_management",
        "output_format": "risk_report",
        "use_cases": [
            "Project risk evaluation",
            "Technical risk analysis",
            "Security risk assessment",
            "Operational risk planning"
        ],
        "input_requirements": [
            "Risk indicators",
            "Historical data",
            "Current vulnerabilities",
            "Impact assessments"
        ]
    }
}


def get_template(template_name: str) -> Dict[str, Any]:
    """Get a specific consultation template."""
    return STRATEGIC_TEMPLATES.get(template_name, {})


def list_templates() -> Dict[str, Dict[str, Any]]:
    """List all available consultation templates."""
    return STRATEGIC_TEMPLATES.copy()


def get_template_names() -> list[str]:
    """Get list of template names."""
    return list(STRATEGIC_TEMPLATES.keys())


def validate_template(template_name: str) -> bool:
    """Validate if a template exists."""
    return template_name in STRATEGIC_TEMPLATES


def get_template_info(template_name: str) -> Dict[str, Any]:
    """Get template information for display."""
    template = get_template(template_name)
    if not template:
        return {}
    
    return {
        "name": template["name"],
        "description": template["description"],
        "use_cases": template["use_cases"],
        "input_requirements": template["input_requirements"]
    }


def format_template_help() -> str:
    """Format template help information for CLI display."""
    help_text = "📚 Available Strategic Consultation Templates:\n\n"
    
    for name, template in STRATEGIC_TEMPLATES.items():
        help_text += f"🎯 {name}\n"
        help_text += f"   Name: {template['name']}\n"
        help_text += f"   Description: {template['description']}\n"
        help_text += f"   Context: {template['context']}\n"
        help_text += f"   Output: {template['output_format']}\n"
        
        if template['use_cases']:
            help_text += f"   Use Cases:\n"
            for use_case in template['use_cases'][:3]:  # Show first 3
                help_text += f"     • {use_case}\n"
            if len(template['use_cases']) > 3:
                help_text += f"     • ... and {len(template['use_cases']) - 3} more\n"
        
        help_text += "\n"
    
    help_text += "💡 Usage Examples:\n"
    help_text += "   python strategic_consultation_cli.py consult --template priority_guidance --question 'What should be our next priority?'\n"
    help_text += "   python strategic_consultation_cli.py consult --template crisis_response --question 'System is experiencing performance issues'\n"
    help_text += "   python strategic_consultation_cli.py consult --template strategic_planning --question 'How should we plan our next development phase?'\n"
    
    return help_text


def main():
    """Test the strategic consultation templates."""
    print("📚 Strategic Consultation Templates Test")
    print("=" * 50)
    
    # Test template listing
    templates = list_templates()
    print(f"✅ Available templates: {len(templates)}")
    
    # Test template validation
    for template_name in ["priority_guidance", "crisis_response", "invalid_template"]:
        is_valid = validate_template(template_name)
        print(f"   • {template_name}: {'✅ Valid' if is_valid else '❌ Invalid'}")
    
    # Test template info
    template_info = get_template_info("priority_guidance")
    if template_info:
        print(f"\n📋 Priority Guidance Template:")
        print(f"   Name: {template_info['name']}")
        print(f"   Description: {template_info['description']}")
        print(f"   Use Cases: {len(template_info['use_cases'])}")
    
    # Test help formatting
    help_text = format_template_help()
    print(f"\n📖 Help text length: {len(help_text)} characters")
    
    print("\n🎉 Strategic Consultation Templates test completed!")


if __name__ == "__main__":
    main()
