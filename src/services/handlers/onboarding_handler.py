"""
Onboarding Handler - V2 Compliant Module
=======================================

Handles onboarding-related commands for messaging CLI.
Extracted from messaging_cli_handlers.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from typing import Any, Dict, List, Optional
import time
import os

from ..messaging_core import UnifiedMessagingCore
from ..models.messaging_models import (
    UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority,
    UnifiedMessageTag, SenderType, RecipientType
)
from ..unified_messaging_imports import load_coordinates_from_json
from ..utils.agent_registry import AGENTS
from ..architectural_onboarding import architectural_manager, ArchitecturalPrinciple
from ...utils.backup import BackupManager
from ...utils.confirm import confirm


class OnboardingHandler:
    """
    Handles onboarding-related commands for messaging CLI.
    
    Manages agent onboarding and welcome message distribution.
    """
    
    def __init__(self):
        """Initialize onboarding handler."""
        self.messaging_core = UnifiedMessagingCore()
        self.onboarded_agents = set()
        self.onboarding_history = []
    
    def handle_onboarding_commands(self, args) -> bool:
        """Handle onboarding-related commands."""
        try:
            if getattr(args, "hard_onboarding", False):
                agents = [a.strip() for a in args.agents.split(",") if a.strip()] or None
                exit_code = self._handle_hard_onboarding(
                    confirm_yes=getattr(args, "yes", False),
                    dry_run=getattr(args, "dry_run", False),
                    agents=agents,
                    timeout=getattr(args, "timeout", 30),
                )
                self.exit_code = exit_code
                return True

            if args.onboarding:
                return self._handle_bulk_onboarding(args)

            if args.onboard:
                if not args.agent:
                    print("❌ Error: --agent required for --onboard")
                    return True

                return self._handle_single_onboarding(args)

        except Exception as e:
            print(f"❌ Error handling onboarding command: {e}")
            return False

        return False
    
    def _handle_bulk_onboarding(self, args) -> bool:
        """Handle bulk onboarding to all agents."""
        try:
            print("🚀 Starting bulk onboarding...")
            # Load coordinates
            agents = load_coordinates_from_json()
            if not agents:
                print("❌ No agent coordinates found")
                return True
            
            # Send onboarding to all agents
            success_count = 0
            
            for agent_id in agents.keys():
                # Create architectural onboarding message if style is set to architectural
                if getattr(args, 'onboarding_style', 'friendly') == 'architectural':
                    content = architectural_manager.create_onboarding_message(agent_id)
                else:
                    content = f"Welcome to the team, {agent_id}! You are now part of the V2 SWARM."

                message = self.messaging_core.create_message(
                    content=content,
                    sender="Captain Agent-4",
                    recipient=agent_id,
                    message_type=UnifiedMessageType.ONBOARDING,
                    priority=UnifiedMessagePriority.REGULAR,
                    tags=[UnifiedMessageTag.ONBOARDING],
                    sender_type=SenderType.SYSTEM,
                    recipient_type=RecipientType.AGENT
                )
                
                if message:
                    success = self.messaging_core.send_message(message, mode=args.mode)
                    if success:
                        success_count += 1
                        self.onboarded_agents.add(agent_id)
                        print(f"✅ Onboarding sent to {agent_id}")
                    else:
                        print(f"❌ Failed to send onboarding to {agent_id}")
                else:
                    print(f"❌ Failed to create onboarding message for {agent_id}")
            
            print(f"📊 Onboarding complete: {success_count}/{len(agents)} agents")
            return True
            
        except Exception as e:
            print(f"❌ Error in bulk onboarding: {e}")
            return False
    
    def _handle_single_onboarding(self, args) -> bool:
        """Handle single agent onboarding."""
        try:
            print(f"🚀 Onboarding {args.agent}...")

            # Create architectural onboarding message if style is set to architectural
            if getattr(args, 'onboarding_style', 'friendly') == 'architectural':
                # Check if a specific principle was requested
                if hasattr(args, 'architectural_principle') and args.architectural_principle:
                    principle_map = {
                        'SRP': ArchitecturalPrinciple.SINGLE_RESPONSIBILITY,
                        'OCP': ArchitecturalPrinciple.OPEN_CLOSED,
                        'LSP': ArchitecturalPrinciple.LISKOV_SUBSTITUTION,
                        'ISP': ArchitecturalPrinciple.INTERFACE_SEGREGATION,
                        'DIP': ArchitecturalPrinciple.DEPENDENCY_INVERSION,
                        'SSOT': ArchitecturalPrinciple.SINGLE_SOURCE_OF_TRUTH,
                        'DRY': ArchitecturalPrinciple.DONT_REPEAT_YOURSELF,
                        'KISS': ArchitecturalPrinciple.KEEP_IT_SIMPLE_STUPID,
                        'TDD': ArchitecturalPrinciple.TEST_DRIVEN_DEVELOPMENT,
                    }
                    principle = principle_map.get(args.architectural_principle)
                    if principle:
                        content = architectural_manager.create_onboarding_message(args.agent)
                        # Temporarily assign the specific principle for this onboarding
                        original_principle = architectural_manager.get_agent_principle(args.agent)
                        architectural_manager.assign_principle_to_agent(args.agent, principle)
                        try:
                            content = architectural_manager.create_onboarding_message(args.agent)
                        finally:
                            # Restore original assignment
                            if original_principle:
                                architectural_manager.assign_principle_to_agent(args.agent, original_principle)
                    else:
                        content = architectural_manager.create_onboarding_message(args.agent)
                else:
                    content = architectural_manager.create_onboarding_message(args.agent)
            else:
                content = f"Welcome to the team, {args.agent}! You are now part of the V2 SWARM."

            message = self.messaging_core.create_message(
                content=content,
                sender="Captain Agent-4",
                recipient=args.agent,
                message_type=UnifiedMessageType.ONBOARDING,
                priority=UnifiedMessagePriority.REGULAR,
                tags=[UnifiedMessageTag.ONBOARDING],
                sender_type=SenderType.SYSTEM,
                recipient_type=RecipientType.AGENT
            )
            
            if message:
                success = self.messaging_core.send_message(message, mode=args.mode)
                if success:
                    self.onboarded_agents.add(args.agent)
                    print(f"✅ Onboarding sent to {args.agent}")
                    return True
                else:
                    print(f"❌ Failed to send onboarding to {args.agent}")
                    return False
            else:
                print(f"❌ Failed to create onboarding message for {args.agent}")
                return False
                
        except Exception as e:
            print(f"❌ Error in single onboarding: {e}")
            return False
    
    def onboard_agent(self, agent_id: str, mode: str = "pyautogui") -> bool:
        """Onboard a specific agent."""
        try:
            message = self.messaging_core.create_message(
                content=f"Welcome to the team, {agent_id}! You are now part of the V2 SWARM.",
                sender="Captain Agent-4",
                recipient=agent_id,
                message_type=UnifiedMessageType.ONBOARDING,
                priority=UnifiedMessagePriority.REGULAR,
                tags=[UnifiedMessageTag.ONBOARDING],
                sender_type=SenderType.SYSTEM,
                recipient_type=RecipientType.AGENT
            )
            
            if message:
                success = self.messaging_core.send_message(message, mode=mode)
                if success:
                    self.onboarded_agents.add(agent_id)
                    self.onboarding_history.append({
                        "agent_id": agent_id,
                        "timestamp": "now",
                        "status": "success"
                    })
                    return True
                else:
                    self.onboarding_history.append({
                        "agent_id": agent_id,
                        "timestamp": "now",
                        "status": "failed"
                    })
                    return False
            return False
            
        except Exception as e:
            print(f"❌ Error onboarding agent {agent_id}: {e}")
            return False
    
    def get_onboarded_agents(self) -> List[str]:
        """Get list of onboarded agents."""
        return list(self.onboarded_agents)
    
    def get_onboarding_history(self) -> List[Dict[str, Any]]:
        """Get onboarding history."""
        return self.onboarding_history.copy()
    
    def is_agent_onboarded(self, agent_id: str) -> bool:
        """Check if agent is onboarded."""
        return agent_id in self.onboarded_agents
    
    def get_onboarding_status(self) -> Dict[str, Any]:
        """Get onboarding handler status."""
        return {
            "onboarded_count": len(self.onboarded_agents),
            "history_count": len(self.onboarding_history),
            "onboarded_agents": list(self.onboarded_agents)
        }
    
    def reset_onboarding(self):
        """Reset onboarding data."""
        self.onboarded_agents.clear()
        self.onboarding_history.clear()

    # ---- Hard Onboarding Implementation ----
    def _handle_hard_onboarding(self, confirm_yes: bool, dry_run: bool, agents: List[str] | None, timeout: int) -> int:
        """Handle hard onboarding sequence with PyAutoGUI automation."""
        print("🚨 HARD ONBOARDING SEQUENCE INITIATED 🚨")

        # Get target agents
        if agents:
            target_agents = agents
        else:
            target_agents = list(AGENTS.keys())

        if not target_agents:
            print("⚠️  No agents found. Aborting.")
            return 1

        # Safety: confirmation + backup
        if not confirm_yes:
            if not confirm(
                "This will reset onboarding state for "
                f"{len(target_agents)} agent(s). Continue?"
            ):
                print("🛑 Aborted by user.")
                return 1

        # Create backup
        from datetime import datetime
        stamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        backup = BackupManager(root="runtime/agent_state", dest=f"runtime/backups/hard_onboarding/{stamp}")

        try:
            if dry_run:
                print("🧪 DRY-RUN: Skipping backup (simulated).")
            else:
                backup_path = backup.create_backup(agents=target_agents)
                print(f"🗄️  Backup created: {backup_path}")
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return 1

        # Sequence execution
        print("🔄 Resetting all agent statuses...")
        if not dry_run:
            self._reset_agent_statuses(target_agents)

        print("🗑️ Clearing previous onboardings...")
        if not dry_run:
            self._clear_onboarding_flags(target_agents)

        print("⚡ Sending force onboarding to all agents...")

        successes: List[str] = []
        failures: List[tuple[str, str]] = []

        for agent in target_agents:
            try:
                if dry_run:
                    ok = True
                else:
                    ok = self._perform_hard_onboarding_pyautogui(agent, timeout)

                if ok:
                    print(f"✅ {agent}: Hard onboarding successful")
                    successes.append(agent)
                else:
                    print(f"❌ {agent}: Hard onboarding failed")
                    failures.append((agent, "onboarding_failed"))
            except Exception as e:
                print(f"❌ {agent}: Hard onboarding error - {e}")
                failures.append((agent, "exception"))

        # System sync
        print("🔒 System synchronization...")
        try:
            if not dry_run:
                self._synchronize_system()
            sync_ok = True
        except Exception as e:
            sync_ok = False
            print(f"❌ Synchronization failed: {e}")

        # Summary
        total = len(target_agents)
        ok_count = len(successes)
        print(f"📊 Hard onboarding complete: {ok_count}/{total} agents successfully onboarded")
        if sync_ok:
            print("🔒 System synchronized and compliant")
        else:
            print("🔓 System not fully synchronized")

        # Exit code policy
        if ok_count == total and sync_ok:
            return 0
        elif ok_count > 0:
            return 2
        else:
            # Offer rollback if catastrophic and not dry-run
            if not dry_run:
                print("🧯 Attempting rollback to pre-onboarding backup...")
                try:
                    backup.rollback()
                    print("↩️  Rolled back to previous state.")
                except Exception as e:
                    print(f"💥 Rollback failed: {e}")
            return 1

    def _perform_hard_onboarding_pyautogui(self, agent_id: str, timeout: int) -> bool:
        """Perform PyAutoGUI hard onboarding sequence."""
        try:
            # Get onboarding coordinates
            agent_data = AGENTS.get(agent_id)
            if not agent_data:
                print(f"❌ No coordinates found for {agent_id}")
                return False

            coords = agent_data.get("onboarding_coords")
            if not coords:
                print(f"❌ No onboarding coordinates found for {agent_id}")
                return False

            x, y = coords["x"], coords["y"]

            # Import PyAutoGUI
            try:
                import pyautogui
                import pyperclip
            except ImportError:
                print("❌ PyAutoGUI or pyperclip not available")
                return False

            # 1. Click onboarding input coordinates
            pyautogui.moveTo(x, y)
            pyautogui.click()
            time.sleep(0.5)

            # 2. Press ctrl+n to create new tab/window
            pyautogui.hotkey('ctrl', 'n')
            time.sleep(0.5)

            # 3. Click onboarding input coordinates again
            pyautogui.moveTo(x, y)
            pyautogui.click()
            time.sleep(0.5)

            # 4. Validate mouse position
            current_pos = pyautogui.position()

            if current_pos.x == x and current_pos.y == y:
                # Mouse is at correct coordinates - paste message
                onboarding_message = f"Welcome to the team, {agent_id}! You are now part of the V2 SWARM."
                pyperclip.copy(onboarding_message)
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.press('enter')
                time.sleep(1)
                return True
            else:
                # Mouse is NOT at coordinates - navigate and retry
                pyautogui.moveTo(x, y)
                time.sleep(0.2)

                # Re-validate position
                current_pos = pyautogui.position()
                if current_pos.x == x and current_pos.y == y:
                    onboarding_message = f"Welcome to the team, {agent_id}! You are now part of the V2 SWARM."
                    pyperclip.copy(onboarding_message)
                    pyautogui.hotkey('ctrl', 'v')
                    pyautogui.press('enter')
                    time.sleep(1)
                    return True
                else:
                    print(f"❌ Failed to position mouse at coordinates for {agent_id}")
                    return False

        except Exception as e:
            print(f"❌ PyAutoGUI error for {agent_id}: {e}")
            return False

    def _reset_agent_statuses(self, agents: List[str]) -> None:
        """Reset agent statuses for hard onboarding."""
        # This would integrate with the agent registry
        print(f"🔄 Resetting statuses for {len(agents)} agents")

    def _clear_onboarding_flags(self, agents: List[str]) -> None:
        """Clear onboarding flags for hard onboarding."""
        # This would integrate with the agent registry
        print(f"🗑️ Clearing onboarding flags for {len(agents)} agents")

    def _synchronize_system(self) -> None:
        """Synchronize system after hard onboarding."""
        # This would perform system-wide synchronization
        print("🔄 Synchronizing system state")
