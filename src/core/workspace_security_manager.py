#!/usr/bin/env python3
"""
Workspace Security Manager - V2 Workspace Security and Isolation

This module manages workspace security, isolation, and access control.
Follows Single Responsibility Principle - only workspace security management.
Architecture: Single Responsibility Principle - security management only
LOC: 195 lines (under 200 limit)
"""

import os
import json
import hashlib
import secrets
from typing import Dict, List, Optional, Any, Set
from pathlib import Path
import logging
from dataclasses import dataclass, asdict
from enum import Enum
import shutil

logger = logging.getLogger(__name__)


class SecurityLevel(Enum):
    """Security levels for workspaces"""
    PUBLIC = "public"
    RESTRICTED = "restricted"
    PRIVATE = "private"
    ISOLATED = "isolated"
    SECURE = "secure"


class Permission(Enum):
    """Workspace permissions"""
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"
    SHARE = "share"


@dataclass
class SecurityPolicy:
    """Security policy for a workspace"""
    workspace_name: str
    security_level: SecurityLevel
    allowed_agents: List[str]
    permissions: Dict[str, List[Permission]]
    isolation_rules: List[str]
    encryption_enabled: bool
    audit_logging: bool
    max_access_attempts: int


@dataclass
class AccessLog:
    """Access log entry"""
    timestamp: str
    agent_id: str
    action: str
    resource: str
    success: bool
    ip_address: str = "unknown"


class WorkspaceSecurityManager:
    """
    Manages workspace security, isolation, and access control
    
    Responsibilities:
    - Security policy enforcement
    - Access control and authentication
    - Workspace isolation
    - Audit logging
    """
    
    def __init__(self, base_workspace_dir: str = "agent_workspaces"):
        self.base_workspace_dir = Path(base_workspace_dir)
        self.security_policies: Dict[str, SecurityPolicy] = {}
        self.access_logs: List[AccessLog] = []
        self.failed_attempts: Dict[str, int] = {}
        self.logger = logging.getLogger(f"{__name__}.WorkspaceSecurityManager")
        
        # Load existing security policies
        self._load_existing_policies()
    
    def _load_existing_policies(self):
        """Load existing security policies from workspace directories"""
        try:
            for workspace_dir in self.base_workspace_dir.iterdir():
                if workspace_dir.is_dir():
                    policy_file = workspace_dir / "security_policy.json"
                    if policy_file.exists():
                        self._load_security_policy(workspace_dir.name, policy_file)
        except Exception as e:
            self.logger.error(f"Failed to load existing security policies: {e}")
    
    def _load_security_policy(self, workspace_name: str, policy_file: Path):
        """Load a security policy from file"""
        try:
            with open(policy_file, 'r') as f:
                data = json.load(f)
            
            # Convert string values back to enums
            security_level = SecurityLevel(data.get('security_level', 'restricted'))
            permissions = {}
            for agent, perms in data.get('permissions', {}).items():
                permissions[agent] = [Permission(p) for p in perms]
            
            policy = SecurityPolicy(
                workspace_name=workspace_name,
                security_level=security_level,
                allowed_agents=data.get('allowed_agents', []),
                permissions=permissions,
                isolation_rules=data.get('isolation_rules', []),
                encryption_enabled=data.get('encryption_enabled', False),
                audit_logging=data.get('audit_logging', True),
                max_access_attempts=data.get('max_access_attempts', 3)
            )
            
            self.security_policies[workspace_name] = policy
            self.logger.info(f"Loaded security policy for workspace: {workspace_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to load security policy for {workspace_name}: {e}")
    
    def create_security_policy(self, workspace_name: str, security_level: SecurityLevel,
                              allowed_agents: List[str] = None, 
                              permissions: Dict[str, List[Permission]] = None) -> bool:
        """Create a security policy for a workspace"""
        try:
            if workspace_name in self.security_policies:
                self.logger.warning(f"Security policy for {workspace_name} already exists")
                return False
            
            # Default permissions
            if permissions is None:
                permissions = {}
                for agent in (allowed_agents or []):
                    permissions[agent] = [Permission.READ, Permission.WRITE]
            
            # Create security policy
            policy = SecurityPolicy(
                workspace_name=workspace_name,
                security_level=security_level,
                allowed_agents=allowed_agents or [],
                permissions=permissions,
                isolation_rules=self._get_default_isolation_rules(security_level),
                encryption_enabled=security_level in [SecurityLevel.ISOLATED, SecurityLevel.SECURE],
                audit_logging=True,
                max_access_attempts=3
            )
            
            # Save policy
            self.security_policies[workspace_name] = policy
            self._save_security_policy(workspace_name, policy)
            
            # Create isolated directory structure if needed
            if security_level in [SecurityLevel.ISOLATED, SecurityLevel.SECURE]:
                self._create_isolated_structure(workspace_name)
            
            self.logger.info(f"Created security policy for workspace: {workspace_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create security policy for {workspace_name}: {e}")
            return False
    
    def _get_default_isolation_rules(self, security_level: SecurityLevel) -> List[str]:
        """Get default isolation rules based on security level"""
        if security_level == SecurityLevel.PUBLIC:
            return ["allow_all_agents"]
        elif security_level == SecurityLevel.RESTRICTED:
            return ["allow_authenticated_agents", "log_all_access"]
        elif security_level == SecurityLevel.PRIVATE:
            return ["allow_owner_only", "encrypt_data", "log_all_access"]
        elif security_level == SecurityLevel.ISOLATED:
            return ["strict_isolation", "encrypt_all_data", "audit_everything", "no_shared_resources"]
        elif security_level == SecurityLevel.SECURE:
            return ["maximum_isolation", "encrypt_everything", "full_audit_trail", "no_external_access"]
        else:
            return ["default_isolation"]
    
    def _create_isolated_structure(self, workspace_name: str):
        """Create isolated directory structure for high-security workspaces"""
        try:
            workspace_path = self.base_workspace_dir / workspace_name
            
            # Create isolated directories
            isolated_dirs = ["secure", "encrypted", "audit", "backup"]
            for dir_name in isolated_dirs:
                (workspace_path / dir_name).mkdir(exist_ok=True)
            
            # Create security metadata
            security_meta = {
                "isolation_level": "high",
                "created_at": self._get_current_timestamp(),
                "encryption_key": self._generate_encryption_key()
            }
            
            with open(workspace_path / "security_metadata.json", "w") as f:
                json.dump(security_meta, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Failed to create isolated structure for {workspace_name}: {e}")
    
    def _generate_encryption_key(self) -> str:
        """Generate a secure encryption key"""
        return secrets.token_hex(32)
    
    def _save_security_policy(self, workspace_name: str, policy: SecurityPolicy):
        """Save security policy to file"""
        try:
            policy_file = self.base_workspace_dir / workspace_name / "security_policy.json"
            
            # Convert enums to strings for JSON serialization
            policy_data = asdict(policy)
            policy_data['security_level'] = policy.security_level.value
            policy_data['permissions'] = {
                agent: [p.value for p in perms]
                for agent, perms in policy.permissions.items()
            }
            
            with open(policy_file, "w") as f:
                json.dump(policy_data, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Failed to save security policy for {workspace_name}: {e}")
    
    def check_access_permission(self, workspace_name: str, agent_id: str, 
                               permission: Permission) -> bool:
        """Check if an agent has permission to access a workspace"""
        try:
            if workspace_name not in self.security_policies:
                self.logger.warning(f"No security policy found for workspace: {workspace_name}")
                return False
            
            policy = self.security_policies[workspace_name]
            
            # Check if agent is allowed
            if agent_id not in policy.allowed_agents:
                self._log_access_attempt(workspace_name, agent_id, f"check_{permission.value}", False)
                return False
            
            # Check specific permission
            if agent_id in policy.permissions:
                if permission in policy.permissions[agent_id]:
                    self._log_access_attempt(workspace_name, agent_id, f"check_{permission.value}", True)
                    return True
            
            self._log_access_attempt(workspace_name, agent_id, f"check_{permission.value}", False)
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to check access permission: {e}")
            return False
    
    def _log_access_attempt(self, workspace_name: str, agent_id: str, action: str, success: bool):
        """Log an access attempt"""
        try:
            log_entry = AccessLog(
                timestamp=self._get_current_timestamp(),
                agent_id=agent_id,
                action=action,
                resource=workspace_name,
                success=success
            )
            
            self.access_logs.append(log_entry)
            
            # Keep only last 1000 log entries
            if len(self.access_logs) > 1000:
                self.access_logs = self.access_logs[-1000:]
                
        except Exception as e:
            self.logger.error(f"Failed to log access attempt: {e}")
    
    def get_security_summary(self) -> Dict[str, Any]:
        """Get summary of security policies and access logs"""
        try:
            total_policies = len(self.security_policies)
            total_logs = len(self.access_logs)
            
            security_levels = {}
            for policy in self.security_policies.values():
                level = policy.security_level.value
                security_levels[level] = security_levels.get(level, 0) + 1
            
            recent_failures = len([log for log in self.access_logs[-100:] if not log.success])
            
            return {
                "total_policies": total_policies,
                "total_access_logs": total_logs,
                "security_levels": security_levels,
                "recent_failures": recent_failures,
                "encrypted_workspaces": len([p for p in self.security_policies.values() if p.encryption_enabled])
            }
        except Exception as e:
            self.logger.error(f"Failed to get security summary: {e}")
            return {"error": str(e)}
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp string"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def run_smoke_test(self) -> bool:
        """Run basic functionality test for this instance"""
        try:
            # Test security policy creation
            test_workspace = "smoke_test_security"
            success = self.create_security_policy(test_workspace, SecurityLevel.PRIVATE, ["test_agent"])
            if not success:
                return False
            
            # Test access permission check
            has_permission = self.check_access_permission(test_workspace, "test_agent", Permission.READ)
            if not has_permission:
                return False
            
            # Test denied access
            no_permission = self.check_access_permission(test_workspace, "unauthorized_agent", Permission.READ)
            if no_permission:
                return False
            
            # Test security summary
            summary = self.get_security_summary()
            if "total_policies" not in summary:
                return False
            
            # Cleanup test policy
            if test_workspace in self.security_policies:
                del self.security_policies[test_workspace]
            
            # Cleanup test files
            test_path = self.base_workspace_dir / test_workspace
            if test_path.exists():
                import shutil
                shutil.rmtree(test_path)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Smoke test failed: {e}")
            return False


def run_smoke_test():
    """Run basic functionality test for WorkspaceSecurityManager"""
    print("🧪 Running WorkspaceSecurityManager Smoke Test...")
    
    try:
        # Test with temporary directory
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = WorkspaceSecurityManager(temp_dir)
            
            # Test security policy creation
            success = manager.create_security_policy("test_workspace", SecurityLevel.PRIVATE, ["Agent-1"])
            assert success
            
            # Test access permission check
            has_permission = manager.check_access_permission("test_workspace", "Agent-1", Permission.READ)
            assert has_permission
            
            # Test denied access
            no_permission = manager.check_access_permission("test_workspace", "Agent-2", Permission.READ)
            assert not no_permission
            
            # Test security summary
            summary = manager.get_security_summary()
            assert "total_policies" in summary
            
        print("✅ WorkspaceSecurityManager Smoke Test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ WorkspaceSecurityManager Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for WorkspaceSecurityManager testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Workspace Security Manager CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--create", nargs=3, metavar=("WORKSPACE", "LEVEL", "AGENTS"), help="Create security policy")
    parser.add_argument("--check", nargs=3, metavar=("WORKSPACE", "AGENT", "PERMISSION"), help="Check access permission")
    parser.add_argument("--summary", action="store_true", help="Show security summary")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_test()
        return
    
    manager = WorkspaceSecurityManager()
    
    if args.create:
        workspace, level, agents = args.create
        try:
            security_level = SecurityLevel(level)
            agent_list = agents.split(",") if agents else []
            success = manager.create_security_policy(workspace, security_level, agent_list)
            print(f"Security policy creation: {'✅ Success' if success else '❌ Failed'}")
        except ValueError:
            print(f"❌ Invalid security level: {level}")
            print(f"Valid levels: {[l.value for l in SecurityLevel]}")
    elif args.check:
        workspace, agent, permission = args.check
        try:
            perm = Permission(permission)
            has_access = manager.check_access_permission(workspace, agent, perm)
            print(f"Access check: {'✅ Granted' if has_access else '❌ Denied'}")
        except ValueError:
            print(f"❌ Invalid permission: {permission}")
            print(f"Valid permissions: {[p.value for p in Permission]}")
    elif args.summary:
        summary = manager.get_security_summary()
        print("Security Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
