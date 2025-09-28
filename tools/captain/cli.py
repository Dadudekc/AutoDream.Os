#!/usr/bin/env python3
"""
Enhanced Captain CLI with Role/Mode Management
=============================================

Integrated command-line interface for Captain with role/mode management,
agent oversight, and system coordination capabilities.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""

import argparse
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.captain.role_manager import RoleManager
from tools.captain.mode_manager import ModeManager
from tools.captain.oversight_loop import OversightLoop
from tools.captain.coordinate_manager import CoordinateManager
from src.fsm.captain_dashboard import get_captain_dashboard
from src.services.messaging.service import MessagingService

# V2 Compliance: File under 400 lines, functions under 30 lines


def show_agent_status():
    """Show comprehensive agent status with role/mode information."""
    dashboard = get_captain_dashboard()
    mode_manager = ModeManager()
    role_manager = RoleManager()
    
    # Get current mode and roles
    current_mode = mode_manager.get_current_mode()
    role_assignments = role_manager.list_assignments()
    
    print("🎯 CAPTAIN DASHBOARD")
    print("=" * 50)
    print(f"Current Mode: {current_mode}-agent mode")
    print(f"Active Agents: {mode_manager.get_active_agents()}")
    print()
    
    # Show role assignments
    if role_assignments:
        print("👥 ROLE ASSIGNMENTS:")
        for agent, role in role_assignments.items():
            print(f"   Agent-{agent}: {role}")
        print()
    
    # Show agent status
    report = dashboard.generate_captain_report()
    print(report)


def _parse_mode_to_int(value: str) -> int:
    if isinstance(value, int):
        return value
    s = str(value).strip().upper()
    if s.startswith('A'):
        s = s[1:]
    try:
        return int(s)
    except ValueError:
        return 8


def manage_modes(args):
    """Manage swarm modes."""
    mode_manager = ModeManager()
    
    if getattr(args, 'list', False):
        current_mode = mode_manager.get_current_mode()
        print(f"Current Mode: {current_mode}")
        print("Available Modes: 2, 4, 5, 6, 8")
        
    elif getattr(args, 'mode_action', None) == 'plan':
        target_mode = _parse_mode_to_int(args.to)
        plan = mode_manager.plan_mode(target_mode)
        current_mode = mode_manager.get_current_mode()
        print(f"Planning switch. Current mode: A{current_mode} -> A{target_mode}")
        print(f"OK: {plan.get('ok', False)}")
        print(f"Issues: {plan.get('issues', [])}")
        print(f"Diff: {plan.get('diff', {})}")
        return 0
    
    elif getattr(args, 'mode_action', None) == 'switch':
        target_mode = _parse_mode_to_int(args.to)
        if args.owner not in ["captain", "co_captain"]:
            print("❌ DENIED: Only captain/co_captain may switch modes")
            return 1
            
        success = mode_manager.switch_mode(target_mode, args.owner, force=args.force, signature_path=args.sign)
        if success:
            print(f"✅ Mode switched to {target_mode}-agent mode")
        else:
            print(f"❌ Mode switch blocked or failed")
            return 1
    elif getattr(args, 'mode_action', None) == 'rollback':
        ok = mode_manager.rollback_mode()
        if ok:
            print("✅ Rolled back to previous validated state")
        else:
            print("❌ Rollback failed or no snapshots available")
            return 1


def manage_roles(args):
    """Manage agent roles."""
    role_manager = RoleManager()
    
    if args.list:
        assignments = role_manager.list_assignments()
        if assignments:
            print("👥 CURRENT ROLE ASSIGNMENTS:")
            for agent, role in assignments.items():
                print(f"   Agent-{agent}: {role}")
        else:
            print("No role assignments found")
            
    elif args.assign:
        agent_id, role = args.assign
        result = role_manager.assign_role(int(agent_id), role)
        if result["ok"]:
            print(f"✅ Agent-{agent_id} assigned to {role}")
        else:
            print(f"❌ Assignment failed: {result['reason']}")
            return 1
            
    elif args.unassign:
        role_manager.unassign_role(int(args.unassign))
        print(f"✅ Agent-{args.unassign} unassigned")
    elif getattr(args, 'set', None):
        import json, yaml  # type: ignore
        file_path = Path(args.set)
        if not file_path.exists():
            print(f"❌ Roles file not found: {file_path}")
            return 1
        content = file_path.read_text(encoding='utf-8')
        try:
            data = yaml.safe_load(content) if file_path.suffix in {'.yml', '.yaml'} else json.loads(content)
        except Exception as e:
            print(f"❌ Failed to parse roles file: {e}")
            return 1
        if args.dry_run:
            print("📝 DRY-RUN: Would set roles to:")
            print(data)
            return 0
        active_path = Path('runtime/active_roles.json')
        active_path.parent.mkdir(parents=True, exist_ok=True)
        active_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        print("✅ Roles updated")


def run_oversight_loop():
    """Run Captain oversight loop."""
    loop = OversightLoop()
    loop.run_once()
    print("✅ Captain oversight loop completed")


def manage_coordinates(args):
    """Manage coordinate configurations."""
    coord_manager = CoordinateManager()
    
    if args.validate:
        valid, issues = coord_manager.validate_coordinates()
        if valid:
            print("✅ All coordinates are valid")
        else:
            print("❌ Coordinate validation issues:")
            for issue in issues:
                print(f"   - {issue}")
            return 1
            
    elif args.show:
        coords = coord_manager.get_active_coordinates()
        print("🎯 ACTIVE COORDINATES:")
        for agent, coord in coords.items():
            print(f"   Agent-{agent}: {coord}")


def onboard_agent(agent_id: str):
    """Onboard agent with role/mode awareness."""
    mode_manager = ModeManager()
    role_manager = RoleManager()
    
    # Check if agent is in current mode
    if not mode_manager.is_agent_active(int(agent_id.replace("Agent-", ""))):
        print(f"❌ Agent {agent_id} not active in current mode")
        return 1
    
    # Send onboarding message
    messaging_service = MessagingService()
    onboarding_message = f"""🚨 ONBOARDING REQUIRED - IMMEDIATE ACTION

Agent {agent_id}, you need to complete onboarding protocol.

📋 REQUIRED ACTIONS:
1. Review onboarding documentation in your workspace
2. Read ONBOARDING_PROTOCOL.md file
3. Update your status to ACTIVE
4. Send confirmation message to Captain (Agent-4)

🎯 CURRENT SWARM STATE:
- Mode: {mode_manager.get_current_mode()}-agent mode
- Your Role: {role_manager.get_agent_role(int(agent_id.replace('Agent-', ''))) or 'Unassigned'}

📁 ONBOARDING FILES TO REVIEW:
• docs/fsm/OVERVIEW.md - FSM system overview
• AGENT_QUICK_START_GUIDE.md - Quick start guide
• AGENT_WORK_GUIDELINES.md - Work guidelines
• V2_COMPLIANCE_REPORT.md - V2 compliance standards

🎯 COMPLETION REQUIRED:
Complete onboarding protocol and confirm with Captain.

📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory"""
    
    success = messaging_service.send(agent_id, onboarding_message, priority="HIGH", high_priority=True)
    
    if success:
        print(f"✅ Onboarding message sent to {agent_id}")
    else:
        print(f"❌ Failed to send onboarding message to {agent_id}")
        return 1


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="Enhanced Captain CLI with Role/Mode Management")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Status command
    subparsers.add_parser('status', help='Show agent status with role/mode info')
    
    # Mode management
    mode_parser = subparsers.add_parser('mode', help='Manage swarm modes')
    mode_subparsers = mode_parser.add_subparsers(dest='mode_action')
    mode_subparsers.add_parser('list', help='List current mode')
    plan_parser = mode_subparsers.add_parser('plan', help='Plan a mode switch and show validation/diff')
    plan_parser.add_argument('--to', required=True, help='Target mode (e.g., A4)')
    switch_parser = mode_subparsers.add_parser('switch', help='Switch mode')
    switch_parser.add_argument('--to', required=True, help='Target mode (e.g., A4)')
    switch_parser.add_argument('--owner', default='captain', choices=['captain','co_captain'], help='Switch authority')
    switch_parser.add_argument('--sign', dest='sign', help='Path to captain signature file')
    switch_parser.add_argument('--force', action='store_true', help='Force switch even if unsafe')
    mode_subparsers.add_parser('rollback', help='Rollback to previous validated state')
    
    # Role management
    role_parser = subparsers.add_parser('role', help='Manage agent roles')
    role_subparsers = role_parser.add_subparsers(dest='role_action')
    role_subparsers.add_parser('list', help='List role assignments')
    assign_parser = role_subparsers.add_parser('assign', help='Assign role to agent')
    assign_parser.add_argument('assign', nargs=2, metavar=('AGENT','ROLE'), help='Agent ID and role name')
    unassign_parser = role_subparsers.add_parser('unassign', help='Unassign agent role')
    unassign_parser.add_argument('unassign', type=int, help='Agent ID to unassign')
    set_parser = role_subparsers.add_parser('set', help='Set roles from file (YAML/JSON)')
    set_parser.add_argument('--file', dest='set', required=True, help='Roles file path')
    set_parser.add_argument('--dry-run', action='store_true', help='Show changes without applying')
    
    # Oversight
    subparsers.add_parser('oversight', help='Run Captain oversight loop')
    
    # Coordinate management
    coord_parser = subparsers.add_parser('coords', help='Manage coordinates')
    # Audit
    audit_parser = subparsers.add_parser('audit', help='Audit utilities')
    audit_sub = audit_parser.add_subparsers(dest='audit_action')
    history_parser = audit_sub.add_parser('history', help='Show recent mode switch history')
    history_parser.add_argument('--last', type=int, default=20, help='Number of records to show')
    coord_subparsers = coord_parser.add_subparsers(dest='coord_action')
    coord_subparsers.add_parser('validate', help='Validate coordinates')
    coord_subparsers.add_parser('show', help='Show active coordinates')
    
    # Onboarding
    onboard_parser = subparsers.add_parser('onboard', help='Onboard agent')
    onboard_parser.add_argument('agent_id', help='Agent ID to onboard')
    
    # Legacy commands for backward compatibility
    subparsers.add_parser('inactive', help='Show inactive agents')
    subparsers.add_parser('report', help='Generate captain report')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == 'status':
            show_agent_status()
        elif args.command == 'mode':
            return manage_modes(args)
        elif args.command == 'role':
            return manage_roles(args)
        elif args.command == 'oversight':
            run_oversight_loop()
        elif args.command == 'coords':
            return manage_coordinates(args)
        elif args.command == 'audit':
            last = getattr(args, 'last', 20)
            hist_path = Path('runtime/governance/mode_switch.jsonl')
            if not hist_path.exists():
                print('No audit history found')
                return 0
            lines = hist_path.read_text(encoding='utf-8').strip().splitlines()[-last:]
            for line in lines:
                print(line)
            return 0
        elif args.command == 'onboard':
            return onboard_agent(args.agent_id)
        elif args.command == 'inactive':
            # Legacy command - redirect to status
            show_agent_status()
        elif args.command == 'report':
            # Legacy command - redirect to status
            show_agent_status()
        
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)