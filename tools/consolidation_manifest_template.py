#!/usr/bin/env python3
"""
Consolidation Manifest Template Generator
=========================================

Produces a starter manifest.json listing proposed canonical modules and actions.
Actions: keep|merge|delete|shim|move

V2 Compliance: ≤400 lines, focused manifest generator
Author: Agent-4 (Captain) - Strategic Oversight & Emergency Intervention
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "runtime" / "consolidation" / "manifest.json"

# Canonical modules identified from analysis
CANON = {
    "onboarding": {
        "canonical": "src/services/agent_hard_onboarding.py",
        "description": "Primary hard onboarding service with PyAutoGUI integration",
        "aliases": [
            "tools/agent_onboard_cli.py",
            "tools/enhanced_agent_onboarding.py",
            "src/services/messaging/onboarding/onboarding_service.py",
            "src/services/discord_bot/commands/agent_coordination/onboarding.py",
            "src/services/enhanced_onboarding_coordinator.py",
            "src/services/captain_onboarding_core.py",
            "src/services/captain_onboarding_system.py",
            "src/services/soft_onboarding.py",
            "src/services/enhanced_onboarding.py",
            "src/services/messaging/onboarding_bridge.py",
        ],
    },
    "discord": {
        "canonical": "src/services/discord_commander/discord_post_client.py",
        "description": "SSOT Discord posting service with webhook and bot support",
        "aliases": [
            "src/services/discord_devlog_service.py",
            "src/services/discord_devlog_bypass.py",
            "src/services/messaging/providers/discord_provider_core.py",
            "src/services/messaging/providers/discord_provider_operations.py",
            "src/services/messaging/providers/discord_provider_cli.py",
            "src/services/discord_bot_integrated.py",
            "src/services/discord_line_emitter.py",
            "src/services/ssot_discord_integration.py",
            "discord_manager.py",
            "discord_server_manager.py",
            "tools/discord_webhook_cli.py",
        ],
    },
    "discord_commander": {
        "canonical": "src/services/discord_commander/core.py",
        "description": "Core Discord commander functionality",
        "aliases": [
            "discord_commander_core.py",
            "run_discord_commander.py",
            "tools/discord_commander_launcher_core.py",
        ],
    },
}

# Consolidation actions based on analysis
MANIFEST = {
    "version": 1,
    "description": "Consolidation manifest for onboarding + discord systems",
    "targets": CANON,
    "actions": [
        # Onboarding consolidation actions
        {
            "file": "tools/agent_onboard_cli.py",
            "action": "shim",
            "module": "src.services.agent_hard_onboarding",
            "symbol_map": {"onboard_agent": "hard_onboard_agent"},
            "reason": "Legacy CLI interface - redirect to canonical service",
        },
        {
            "file": "tools/enhanced_agent_onboarding.py",
            "action": "delete",
            "reason": "Functionality merged into agent_hard_onboarding.py",
        },
        {
            "file": "src/services/messaging/onboarding/onboarding_service.py",
            "action": "shim",
            "module": "src.services.agent_hard_onboarding",
            "symbol_map": {"OnboardingService": "AgentHardOnboarder"},
            "reason": "Legacy service interface - redirect to canonical",
        },
        {
            "file": "src/services/discord_bot/commands/agent_coordination/onboarding.py",
            "action": "shim",
            "module": "src.services.agent_hard_onboarding",
            "symbol_map": {"AgentOnboardingHandler": "AgentHardOnboarder"},
            "reason": "Discord bot handler - redirect to canonical",
        },
        {
            "file": "src/services/enhanced_onboarding_coordinator.py",
            "action": "delete",
            "reason": "Redundant coordinator functionality",
        },
        {
            "file": "src/services/captain_onboarding_core.py",
            "action": "delete",
            "reason": "Redundant captain onboarding functionality",
        },
        {
            "file": "src/services/captain_onboarding_system.py",
            "action": "delete",
            "reason": "Redundant captain onboarding functionality",
        },
        {
            "file": "src/services/soft_onboarding.py",
            "action": "delete",
            "reason": "Soft onboarding deprecated in favor of hard onboarding",
        },
        {
            "file": "src/services/enhanced_onboarding.py",
            "action": "delete",
            "reason": "Enhanced onboarding functionality merged into canonical",
        },
        {
            "file": "src/services/messaging/onboarding_bridge.py",
            "action": "delete",
            "reason": "Bridge functionality integrated into canonical service",
        },
        # Discord consolidation actions
        {
            "file": "src/services/discord_devlog_bypass.py",
            "action": "delete",
            "reason": "Redundant with discord_post_client SSOT routing",
        },
        {
            "file": "src/services/messaging/providers/discord_provider_core.py",
            "action": "shim",
            "module": "src.services.discord_commander.discord_post_client",
            "symbol_map": {"DiscordMessagingProvider": "DiscordPostClient"},
            "reason": "Legacy provider interface - redirect to canonical",
        },
        {
            "file": "src/services/messaging/providers/discord_provider_operations.py",
            "action": "shim",
            "module": "src.services.discord_commander.discord_post_client",
            "symbol_map": {"DiscordProviderService": "DiscordPostClient"},
            "reason": "Legacy operations interface - redirect to canonical",
        },
        {
            "file": "src/services/messaging/providers/discord_provider_cli.py",
            "action": "delete",
            "reason": "CLI functionality redundant with webhook CLI",
        },
        {
            "file": "src/services/discord_bot_integrated.py",
            "action": "delete",
            "reason": "Integrated bot functionality merged into discord_commander",
        },
        {
            "file": "src/services/discord_line_emitter.py",
            "action": "delete",
            "reason": "Line emitter functionality integrated into canonical",
        },
        {
            "file": "src/services/ssot_discord_integration.py",
            "action": "delete",
            "reason": "SSOT integration functionality merged into canonical",
        },
        {
            "file": "discord_manager.py",
            "action": "move",
            "to": "src/services/discord_commander/legacy_manager.py",
            "reason": "Legacy manager - move to commander directory",
        },
        {
            "file": "discord_server_manager.py",
            "action": "move",
            "to": "src/services/discord_commander/server_manager.py",
            "reason": "Server manager - move to commander directory",
        },
        {
            "file": "tools/discord_webhook_cli.py",
            "action": "shim",
            "module": "src.services.discord_commander.discord_post_client",
            "symbol_map": {"main": "DiscordPostClient"},
            "reason": "CLI interface - redirect to canonical service",
        },
        # Discord commander consolidation
        {
            "file": "discord_commander_core.py",
            "action": "delete",
            "reason": "Root level duplicate - functionality in src/services/discord_commander/",
        },
        {
            "file": "run_discord_commander.py",
            "action": "move",
            "to": "src/services/discord_commander/launcher.py",
            "reason": "Launcher script - move to commander directory",
        },
        {
            "file": "tools/discord_commander_launcher_core.py",
            "action": "delete",
            "reason": "Duplicate launcher functionality",
        },
        # Manual merge candidates (defer to pass-2)
        {
            "file": "src/services/discord_devlog_service.py",
            "action": "merge",
            "into": "src/services/discord_commander/discord_post_client.py",
            "note": "Manual merge required - defer to pass-2",
            "reason": "Devlog service functionality to be merged into canonical",
        },
    ],
    "pass2_candidates": [
        {
            "file": "src/services/discord_devlog_service.py",
            "action": "manual_merge",
            "target": "src/services/discord_commander/discord_post_client.py",
            "reason": "Complex merge requiring manual code integration",
        }
    ],
    "expected_reduction": {
        "files_deleted": 15,
        "files_moved": 3,
        "shims_created": 6,
        "total_files_removed": 12,
    },
}


def main():
    """Generate consolidation manifest."""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(MANIFEST, indent=2), encoding="utf-8")
    print(f"✅ Generated consolidation manifest: {OUT}")
    print(f"   Actions: {len(MANIFEST['actions'])}")
    print(f"   Expected file reduction: {MANIFEST['expected_reduction']['total_files_removed']}")
    print(f"   Pass-2 candidates: {len(MANIFEST['pass2_candidates'])}")


if __name__ == "__main__":
    main()

