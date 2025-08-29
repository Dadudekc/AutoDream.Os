"""
FSM Compliance Core - Modularized from FSM Compliance Integration
Captain Agent-3: MODULAR-001 Implementation
"""

import logging
from typing import Dict, Any, List, Optional
from .validators.compliance_validator import ComplianceValidator
from .auditors.compliance_auditor import ComplianceAuditor

class FSMComplianceCore:
    """Core FSM compliance functionality"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.validator = ComplianceValidator()
        self.auditor = ComplianceAuditor()
        self.compliance_rules = {}
        self.audit_history = []
    
    def validate_fsm_compliance(self, fsm_config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate FSM compliance"""
        try:
            validation_result = self.validator.validate_config(fsm_config)
            audit_result = self.auditor.audit_compliance(fsm_config)
            
            result = {
                "validation": validation_result,
                "audit": audit_result,
                "timestamp": "2025-08-28T22:55:00.000000Z"
            }
            
            self.audit_history.append(result)
            return result
            
        except Exception as e:
            self.logger.error(f"Compliance validation failed: {e}")
            return {"error": str(e)}
    
    def get_compliance_status(self) -> Dict[str, Any]:
        """Get compliance status"""
        return {
            "total_audits": len(self.audit_history),
            "compliance_rules": len(self.compliance_rules),
            "last_audit": self.audit_history[-1] if self.audit_history else None
        }
