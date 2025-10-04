#!/usr/bin/env python3
"""
Strategic Consultation CLI
=========================
Command-line interface for Thea strategic consultation system.
V2 Compliant: ≤400 lines, focused CLI functionality

Author: Agent-7 (Implementation Specialist)
License: MIT
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from strategic_consultation_core import consult_command
from strategic_consultation_templates import (
    format_template_help,
    get_template_info,
    list_templates,
    validate_template
)


def consult_command_handler(args: argparse.Namespace) -> int:
    """Handle consult command."""
    print("🤖 Thea Strategic Consultation")
    print("=" * 50)
    
    # Validate template if provided
    if args.template and not validate_template(args.template):
        print(f"❌ Invalid template: {args.template}")
        print("💡 Use 'python strategic_consultation_cli.py help' to see available templates")
        return 1
    
    # Execute consultation
    try:
        result = consult_command(
            question=args.question,
            template=args.template,
            context=args.context
        )
        
        if result["success"]:
            print(f"✅ Consultation completed successfully!")
            print(f"📋 Consultation ID: {result['consultation_id']}")
            print(f"🎯 Template: {result['template']}")
            print(f"⏰ Timestamp: {result['timestamp']}")
            
            # Display response
            response = result["response"]
            print(f"\n📊 Consultation Response:")
            print(f"Type: {response.get('type', 'N/A')}")
            
            if "recommendations" in response:
                print(f"\n💡 Recommendations:")
                for i, rec in enumerate(response["recommendations"], 1):
                    print(f"   {i}. {rec}")
            
            if "immediate_actions" in response:
                print(f"\n🚨 Immediate Actions:")
                for i, action in enumerate(response["immediate_actions"], 1):
                    print(f"   {i}. {action}")
            
            if "strategic_goals" in response:
                print(f"\n🎯 Strategic Goals:")
                for i, goal in enumerate(response["strategic_goals"], 1):
                    print(f"   {i}. {goal}")
            
            if "confidence" in response:
                confidence_icon = "🟢" if response["confidence"] == "high" else "🟡" if response["confidence"] == "medium" else "🔴"
                print(f"\n{confidence_icon} Confidence: {response['confidence']}")
            
            return 0
        else:
            print(f"❌ Consultation failed: {result.get('error', 'Unknown error')}")
            return 1
            
    except Exception as e:
        print(f"❌ Consultation error: {e}")
        return 1


def status_report_command_handler(args: argparse.Namespace) -> int:
    """Handle status-report command."""
    print("📊 Thea Consultation Status Report")
    print("=" * 50)
    
    try:
        from strategic_consultation_core import StrategicConsultationCore
        
        core = StrategicConsultationCore()
        
        # Get consultation history
        history = core.get_consultation_history(limit=5)
        
        print(f"📋 Recent Consultations: {len(history)}")
        
        if history:
            for consultation in history:
                request = consultation["request"]
                result = consultation["result"]
                
                print(f"\n🔍 {request['request_id']}")
                print(f"   Template: {request['template']}")
                print(f"   Question: {request['question'][:60]}{'...' if len(request['question']) > 60 else ''}")
                print(f"   Status: {result['status']}")
                print(f"   Time: {request['timestamp']}")
        else:
            print("   No consultations found")
        
        # Get available templates
        templates = core.get_available_templates()
        print(f"\n📚 Available Templates: {len(templates)}")
        for name, info in templates.items():
            print(f"   • {name}: {info['name']}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Status report error: {e}")
        return 1


def emergency_command_handler(args: argparse.Namespace) -> int:
    """Handle emergency command."""
    print("🚨 Thea Emergency Consultation")
    print("=" * 50)
    
    # Use crisis response template for emergency
    try:
        result = consult_command(
            question=args.issue,
            template="crisis_response",
            context="emergency"
        )
        
        if result["success"]:
            print(f"✅ Emergency consultation completed!")
            print(f"📋 Consultation ID: {result['consultation_id']}")
            
            # Display emergency response
            response = result["response"]
            print(f"\n🚨 Emergency Response:")
            
            if "severity" in response:
                severity_icon = "🔴" if response["severity"] == "high" else "🟡" if response["severity"] == "medium" else "🟢"
                print(f"Severity: {severity_icon} {response['severity']}")
            
            if "immediate_actions" in response:
                print(f"\n⚡ Immediate Actions:")
                for i, action in enumerate(response["immediate_actions"], 1):
                    print(f"   {i}. {action}")
            
            if "recovery_plan" in response:
                print(f"\n🔧 Recovery Plan:")
                for i, step in enumerate(response["recovery_plan"], 1):
                    print(f"   {i}. {step}")
            
            return 0
        else:
            print(f"❌ Emergency consultation failed: {result.get('error', 'Unknown error')}")
            return 1
            
    except Exception as e:
        print(f"❌ Emergency consultation error: {e}")
        return 1


def help_command_handler(args: argparse.Namespace) -> int:
    """Handle help command."""
    print("🤖 Thea Strategic Consultation System")
    print("=" * 50)
    
    print("📋 Available Commands:")
    print("   consult       - Execute strategic consultation")
    print("   status-report - Show consultation status and history")
    print("   emergency     - Emergency consultation for critical issues")
    print("   help          - Show this help message")
    
    print(f"\n{format_template_help()}")
    
    print("🔧 Command Examples:")
    print("   python strategic_consultation_cli.py consult --template priority_guidance --question 'What should be our next priority?'")
    print("   python strategic_consultation_cli.py status-report")
    print("   python strategic_consultation_cli.py emergency --issue 'System performance is degrading'")
    
    return 0


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Thea Strategic Consultation System",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Consult command
    consult_parser = subparsers.add_parser('consult', help='Execute strategic consultation')
    consult_parser.add_argument('--question', required=True, help='Consultation question')
    consult_parser.add_argument('--template', help='Consultation template to use')
    consult_parser.add_argument('--context', help='Additional context for consultation')
    
    # Status report command
    status_parser = subparsers.add_parser('status-report', help='Show consultation status and history')
    
    # Emergency command
    emergency_parser = subparsers.add_parser('emergency', help='Emergency consultation for critical issues')
    emergency_parser.add_argument('--issue', required=True, help='Description of the emergency issue')
    
    # Help command
    help_parser = subparsers.add_parser('help', help='Show help information')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Route to appropriate handler
    if args.command == 'consult':
        return consult_command_handler(args)
    elif args.command == 'status-report':
        return status_report_command_handler(args)
    elif args.command == 'emergency':
        return emergency_command_handler(args)
    elif args.command == 'help':
        return help_command_handler(args)
    else:
        print(f"❌ Unknown command: {args.command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
