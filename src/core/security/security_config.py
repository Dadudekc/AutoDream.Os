from typing import List

from .security_auth import SecurityLevel


def get_default_isolation_rules(level: SecurityLevel) -> List[str]:
    if level == SecurityLevel.PUBLIC:
        return ["allow_all_agents"]
    if level == SecurityLevel.RESTRICTED:
        return ["allow_authenticated_agents", "log_all_access"]
    if level == SecurityLevel.PRIVATE:
        return ["allow_owner_only", "encrypt_data", "log_all_access"]
    if level == SecurityLevel.ISOLATED:
        return [
            "strict_isolation",
            "encrypt_all_data",
            "audit_everything",
            "no_shared_resources",
        ]
    if level == SecurityLevel.SECURE:
        return [
            "maximum_isolation",
            "encrypt_everything",
            "full_audit_trail",
            "no_external_access",
        ]
    return ["default_isolation"]
