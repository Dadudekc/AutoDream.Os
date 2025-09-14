from __future__ import annotations

import logging

logger = logging.getLogger(__name__)
"""
Onboarding Handler - V2 Compliant Module
=======================================

Handles onboarding-related commands for messaging CLI.
Extracted from messaging_cli_handlers.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""
from datetime import datetime

from ...automation.ui_onboarding import UIOnboarder, UIUnavailableError
from ...core.workspace_agent_registry import AgentRegistry
from ...quality.proof_ledger import run_tdd_proof
from ...templates.onboarding_roles import ROLES, build_role_message
from ...utils.backup import BackupManager
from ...utils.confirm import confirm


class OnboardingHandler:

    def can_handle(self, args) ->bool:
        """Check if this handler can handle the given arguments."""
        return hasattr(args, 'onboarding') and args.onboarding or hasattr(args,
            'onboard') and args.onboard or hasattr(args, 'hard_onboarding'
            ) and args.hard_onboarding

    def handle(self, args) ->bool:
        """Handle the command."""
        return self.handle_onboarding_commands(args)

    def __init__(self) ->None:
        self.exit_code = 0

    def handle_onboarding_commands(self, args) ->bool:
        if getattr(args, 'hard_onboarding', False):
            agents = None
            if hasattr(args, 'agent_subset') and args.agent_subset:
                agents = [a.strip() for a in args.agent_subset.split(',') if a.
                    strip()] or None
            elif hasattr(args, 'agents') and args.agents:
                agents = [a.strip() for a in args.agents.split(',') if a.
                    strip()] or None
            self.exit_code = self._handle_hard_onboarding(confirm_yes=args.
                yes, dry_run=args.dry_run, agents=agents, timeout=args.
                timeout, use_ui=args.ui, ui_retries=args.ui_retries,
                ui_tolerance=args.ui_tolerance, mode=args.onboarding_mode,
                role_map_str=args.assign_roles, emit_proof=args.proof,
                audit_cleanup=getattr(args, 'audit_cleanup', False))
            return True
        return False

    def _derive_role_map(self, agent_ids: list[str], mode: str,
        role_map_str: str) ->dict[str, str]:
        if role_map_str:
            mapping: dict[str, str] = {}
            for spec in role_map_str.split(','):
                spec = spec.strip()
                if not spec:
                    continue
                agent, role = (s.strip() for s in spec.split(':', 1))
                role = role.upper()
                if role not in ROLES:
                    raise ValueError(f"Unknown role '{role}'")
                mapping[agent] = role
            return mapping
        if mode == 'quality-suite':
            cycle = ['SOLID', 'SSOT', 'DRY', 'KISS', 'TDD']
        else:
            cycle = [mode.upper()]
        mapping: dict[str, str] = {}
        for idx, a in enumerate(agent_ids):
            mapping[a] = cycle[idx % len(cycle)]
        return mapping

    def _handle_hard_onboarding(self, confirm_yes: bool, dry_run: bool,
        agents: (list[str] | None), timeout: int, use_ui: bool, ui_retries:
        int, ui_tolerance: int, mode: str, role_map_str: str, emit_proof:
        bool, audit_cleanup: bool) ->int:
        logger.info('🚨 HARD ONBOARDING SEQUENCE INITIATED 🚨')
        reg = AgentRegistry()
        target_agents = agents or reg.list_agents()
        if not target_agents:
            logger.info('⚠️  No agents found. Aborting.')
            return 1
        try:
            role_map = self._derive_role_map(target_agents, mode, role_map_str)
        except Exception as e:
            logger.info(f'❌ Role mapping error: {e}')
            return 1
        if not confirm_yes:
            if not confirm(
                f'This will reset and re-onboard {len(target_agents)} agent(s) with roles ({mode}). Continue?'
                ):
                logger.info('🛑 Aborted by user.')
                return 1
        stamp = datetime.utcnow().strftime('%Y%m%d-%H%M%S')
        backup = BackupManager(root='runtime/agent_state', dest=
            f'runtime/backups/hard_onboarding/{stamp}')
        try:
            if dry_run:
                logger.info('🧪 DRY-RUN: Skipping backup (simulated).')
            else:
                backup_path = backup.create_backup(agents=target_agents)
                logger.info(f'🗄️  Backup created: {backup_path}')
        except Exception as e:
            logger.info(f'❌ Backup failed: {e}')
            return 1
        logger.info('🔄 Resetting all agent statuses...')
        if not dry_run:
            reg.reset_statuses(target_agents)
        logger.info('🗑️ Clearing previous onboardings...')
        if not dry_run:
            reg.clear_onboarding_flags(target_agents)
        ui_onboarder = None
        if use_ui:
            try:
                ui_onboarder = UIOnboarder(tolerance=ui_tolerance, retries=
                    ui_retries, dry_run=dry_run)
            except UIUnavailableError as e:
                logger.info(f'❌ UI mode unavailable: {e}')
                return 1
        logger.info('⚡ Sending role-based onboarding to all agents...')
        successes: list[str] = []
        failures: list[tuple[str, str]] = []
        for agent in target_agents:
            role = role_map[agent]
            message = build_role_message(agent, role)
            try:
                if use_ui:
                    coords = reg.get_onboarding_coords(agent)
                    ok = ui_onboarder.perform(agent_id=agent, coords=coords,
                        message=message)
                else:
                    if not dry_run:
                        reg.save_last_onboarding_message(agent, message)
                        reg.force_onboard(agent_id=agent, timeout=timeout)
                    ok = True if dry_run else reg.verify_onboarded(agent)
                if ok:
                    logger.info(f'✅ {agent}: {role} onboarding successful')
                    successes.append(agent)
                else:
                    logger.info(
                        f'❌ {agent}: {role} onboarding failed verification')
                    failures.append((agent, 'verification_failed'))
            except Exception as e:
                logger.info(f'❌ {agent}: onboarding error - {e}')
                failures.append((agent, 'exception'))
        logger.info('🔒 System synchronization...')
        try:
            if not dry_run:
                reg.synchronize()
            sync_ok = True
        except Exception as e:
            sync_ok = False
            logger.info(f'❌ Synchronization failed: {e}')
        if emit_proof:
            try:
                path = '(dry-run simulated)'
                if dry_run:
                    logger.info(
                        '🧪 DRY-RUN: Skipping proof emission (simulated).')
                else:
                    path = run_tdd_proof(mode=mode, role_map=role_map)
                logger.info(f'🧾 TDD Proof emitted: {path}')
            except Exception as e:
                logger.info(f'❌ Proof emission failed: {e}')
        if audit_cleanup:
            logger.info('🧹 Running cleanup auditor...')
            try:
                import subprocess
                import sys
                proc = subprocess.run(['python', 'tools/audit_cleanup.py'],
                    capture_output=True, text=True)
                sys.stdout.write(proc.stdout or '')
                sys.stderr.write(proc.stderr or '')
                if proc.returncode != 0:
                    logger.info('❌ Cleanup auditor guard triggered. Aborting.')
                    return 1
                else:
                    logger.info('✅ Cleanup auditor passed.')
            except Exception as e:
                logger.info(f'❌ Failed to run auditor: {e}')
                return 1
        total = len(target_agents)
        ok_count = len(successes)
        logger.info(
            f'📊 Role-based onboarding complete: {ok_count}/{total} agents ready'
            )
        logger.info('🔒 System synchronized and compliant' if sync_ok else
            '🔓 System not fully synchronized')
        if ok_count == total and sync_ok:
            return 0
        elif ok_count > 0:
            return 2
        else:
            if not dry_run:
                logger.info('🧯 Attempting rollback to pre-onboarding backup...'
                    )
                try:
                    backup.rollback()
                    logger.info('↩️  Rolled back to previous state.')
                except Exception as e:
                    logger.info(f'💥 Rollback failed: {e}')
            return 1
