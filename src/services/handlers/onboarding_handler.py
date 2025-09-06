"""
Onboarding Handler - V2 Compliant Module
=======================================

Handles onboarding-related commands for messaging CLI.
Extracted from messaging_cli_handlers.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from __future__ import annotations
from typing import List, Tuple, Dict
from datetime import datetime

from ...core.agent_registry import AgentRegistry
from ...utils.backup import BackupManager
from ...utils.confirm import confirm
from ...automation.ui_onboarding import UIOnboarder, UIUnavailableError
from ...templates.onboarding_roles import build_role_message, ROLES
from ...quality.proof_ledger import run_tdd_proof


class OnboardingHandler:
    def __init__(self) -> None:
        self.exit_code = 0

    def handle_onboarding_commands(self, args) -> bool:
        if getattr(args, "hard_onboarding", False):
            agents = [a.strip() for a in args.agents.split(",") if a.strip()] or None
            self.exit_code = self._handle_hard_onboarding(
                confirm_yes=args.yes,
                dry_run=args.dry_run,
                agents=agents,
                timeout=args.timeout,
                use_ui=args.ui,
                ui_retries=args.ui_retries,
                ui_tolerance=args.ui_tolerance,
                mode=args.onboarding_mode,
                role_map_str=args.assign_roles,
                emit_proof=args.proof,
                audit_cleanup=getattr(args, "audit_cleanup", False),
            )
            return True
        return False

    def _derive_role_map(
        self, agent_ids: List[str], mode: str, role_map_str: str
    ) -> Dict[str, str]:
        # explicit mapping overrides
        if role_map_str:
            mapping: Dict[str, str] = {}
            for spec in role_map_str.split(","):
                spec = spec.strip()
                if not spec:
                    continue
                agent, role = [s.strip() for s in spec.split(":", 1)]
                role = role.upper()
                if role not in ROLES:
                    raise ValueError(f"Unknown role '{role}'")
                mapping[agent] = role
            return mapping

        if mode == "quality-suite":
            cycle = ["SOLID", "SSOT", "DRY", "KISS", "TDD"]
        else:
            cycle = [mode.upper()]

        mapping: Dict[str, str] = {}
        for idx, a in enumerate(agent_ids):
            mapping[a] = cycle[idx % len(cycle)]
        return mapping

    def _handle_hard_onboarding(
        self,
        confirm_yes: bool,
        dry_run: bool,
        agents: List[str] | None,
        timeout: int,
        use_ui: bool,
        ui_retries: int,
        ui_tolerance: int,
        mode: str,
        role_map_str: str,
        emit_proof: bool,
        audit_cleanup: bool,
    ) -> int:
        print("🚨 HARD ONBOARDING SEQUENCE INITIATED 🚨")
        reg = AgentRegistry()
        target_agents = agents or reg.list_agents()
        if not target_agents:
            print("⚠️  No agents found. Aborting.")
            return 1

        # Role map
        try:
            role_map = self._derive_role_map(target_agents, mode, role_map_str)
        except Exception as e:
            print(f"❌ Role mapping error: {e}")
            return 1

        # Confirm
        if not confirm_yes:
            if not confirm(
                f"This will reset and re-onboard {len(target_agents)} agent(s) with roles ({mode}). Continue?"
            ):
                print("🛑 Aborted by user.")
                return 1

        # Backup
        stamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        backup = BackupManager(
            root="runtime/agent_state", dest=f"runtime/backups/hard_onboarding/{stamp}"
        )
        try:
            if dry_run:
                print("🧪 DRY-RUN: Skipping backup (simulated).")
            else:
                backup_path = backup.create_backup(agents=target_agents)
                print(f"🗄️  Backup created: {backup_path}")
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return 1

        # Reset + clear
        print("🔄 Resetting all agent statuses...")
        if not dry_run:
            reg.reset_statuses(target_agents)
        print("🗑️ Clearing previous onboardings...")
        if not dry_run:
            reg.clear_onboarding_flags(target_agents)

        # Prepare UI onboarder
        ui_onboarder = None
        if use_ui:
            try:
                ui_onboarder = UIOnboarder(
                    tolerance=ui_tolerance, retries=ui_retries, dry_run=dry_run
                )
            except UIUnavailableError as e:
                print(f"❌ UI mode unavailable: {e}")
                return 1

        print("⚡ Sending role-based onboarding to all agents...")
        successes: List[str] = []
        failures: List[Tuple[str, str]] = []

        for agent in target_agents:
            role = role_map[agent]
            message = build_role_message(agent, role)
            try:
                if use_ui:
                    coords = reg.get_onboarding_coords(agent)
                    ok = ui_onboarder.perform(
                        agent_id=agent, coords=coords, message=message
                    )
                else:
                    # programmatic: log message + mark onboarded
                    if not dry_run:
                        reg.save_last_onboarding_message(agent, message)
                        reg.force_onboard(agent_id=agent, timeout=timeout)
                    ok = True if dry_run else reg.verify_onboarded(agent)
                if ok:
                    print(f"✅ {agent}: {role} onboarding successful")
                    successes.append(agent)
                else:
                    print(f"❌ {agent}: {role} onboarding failed verification")
                    failures.append((agent, "verification_failed"))
            except Exception as e:
                print(f"❌ {agent}: onboarding error - {e}")
                failures.append((agent, "exception"))

        # Sync
        print("🔒 System synchronization...")
        try:
            if not dry_run:
                reg.synchronize()
            sync_ok = True
        except Exception as e:
            sync_ok = False
            print(f"❌ Synchronization failed: {e}")

        # Optional TDD proof
        if emit_proof:
            try:
                path = "(dry-run simulated)"
                if dry_run:
                    print("🧪 DRY-RUN: Skipping proof emission (simulated).")
                else:
                    path = run_tdd_proof(mode=mode, role_map=role_map)
                print(f"🧾 TDD Proof emitted: {path}")
            except Exception as e:
                print(f"❌ Proof emission failed: {e}")

        # Optional cleanup audit
        if audit_cleanup:
            print("🧹 Running cleanup auditor...")
            try:
                import subprocess
                import sys

                proc = subprocess.run(
                    ["python", "tools/audit_cleanup.py"], capture_output=True, text=True
                )
                sys.stdout.write(proc.stdout or "")
                sys.stderr.write(proc.stderr or "")
                if proc.returncode != 0:
                    print("❌ Cleanup auditor guard triggered. Aborting.")
                    return 1
                else:
                    print("✅ Cleanup auditor passed.")
            except Exception as e:
                print(f"❌ Failed to run auditor: {e}")
                return 1

        # Summary
        total = len(target_agents)
        ok_count = len(successes)
        print(f"📊 Role-based onboarding complete: {ok_count}/{total} agents ready")
        print(
            "🔒 System synchronized and compliant"
            if sync_ok
            else "🔓 System not fully synchronized"
        )

        if ok_count == total and sync_ok:
            return 0
        elif ok_count > 0:
            return 2
        else:
            if not dry_run:
                print("🧯 Attempting rollback to pre-onboarding backup...")
                try:
                    backup.rollback()
                    print("↩️  Rolled back to previous state.")
                except Exception as e:
                    print(f"💥 Rollback failed: {e}")
            return 1
