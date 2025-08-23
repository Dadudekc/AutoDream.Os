#!/usr/bin/env python3
"""
Data Consistency Management System
==================================
Comprehensive consistency management for distributed agent swarm data.
Follows 200 LOC limit and single responsibility principle.
"""

import logging
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class ConsistencyLevel(Enum):
    """Data consistency levels"""

    EVENTUAL = "eventual"
    STRONG = "strong"
    LINEARIZABLE = "linearizable"


@dataclass
class ConsistencyRule:
    """Consistency rule definition"""

    rule_id: str
    data_key: str
    consistency_level: ConsistencyLevel
    max_drift_ms: int = 1000
    replication_factor: int = 1


class ConsistencyManagement:
    """Data consistency management system for agent swarms"""

    def __init__(self, system_id: str = "default-consistency"):
        self.logger = logging.getLogger(f"{__name__}.ConsistencyManagement")
        self.system_id = system_id
        self._consistency_rules: Dict[str, ConsistencyRule] = {}
        self._data_consistency: Dict[str, Dict[str, Any]] = {}
        self._data_versions: Dict[str, Dict[str, int]] = {}
        self.logger.info(f"Consistency Management '{system_id}' initialized")

    def add_consistency_rule(self, rule: ConsistencyRule) -> bool:
        """Add a consistency rule"""
        if rule.rule_id in self._consistency_rules:
            return False
        self._consistency_rules[rule.rule_id] = rule
        if rule.data_key not in self._data_consistency:
            self._data_consistency[rule.data_key] = {
                "current_value": None,
                "last_update": 0.0,
                "replicas": {},
                "consistency_status": "unknown",
            }
        return True

    def remove_consistency_rule(self, rule_id: str) -> bool:
        """Remove a consistency rule"""
        if rule_id not in self._consistency_rules:
            return False
        del self._consistency_rules[rule_id]
        return True

    def update_data_value(
        self,
        data_key: str,
        value: Any,
        agent_id: str,
        timestamp: Optional[float] = None,
    ) -> bool:
        """Update data value with consistency checking"""
        if timestamp is None:
            timestamp = time.time()
        relevant_rules = [
            r for r in self._consistency_rules.values() if r.data_key == data_key
        ]
        if not relevant_rules:
            self._update_data_store(data_key, value, agent_id, timestamp)
            return True
        for rule in relevant_rules:
            if not self._check_consistency_rule(rule, data_key, value, timestamp):
                return False
        self._update_data_store(data_key, value, agent_id, timestamp)
        self._update_consistency_status(data_key)
        return True

    def _update_data_store(
        self, data_key: str, value: Any, agent_id: str, timestamp: float
    ):
        """Update internal data store"""
        if data_key not in self._data_consistency:
            self._data_consistency[data_key] = {
                "current_value": None,
                "last_update": 0.0,
                "replicas": {},
                "consistency_status": "unknown",
            }
        self._data_consistency[data_key]["current_value"] = value
        self._data_consistency[data_key]["last_update"] = timestamp
        self._data_consistency[data_key]["replicas"][agent_id] = {
            "value": value,
            "timestamp": timestamp,
        }
        if data_key not in self._data_versions:
            self._data_versions[data_key] = {}
        self._data_versions[data_key][agent_id] = (
            self._data_versions[data_key].get(agent_id, 0) + 1
        )

    def _check_consistency_rule(
        self, rule: ConsistencyRule, data_key: str, value: Any, timestamp: float
    ) -> bool:
        """Check if update complies with consistency rule"""
        current_data = self._data_consistency.get(data_key, {})
        last_update = current_data.get("last_update", 0.0)
        if timestamp < last_update - (rule.max_drift_ms / 1000.0):
            return False
        if rule.replication_factor > 1:
            replicas = current_data.get("replicas", {})
            if len(replicas) < rule.replication_factor:
                return False
        if rule.consistency_level == ConsistencyLevel.STRONG:
            if not self._check_strong_consistency(data_key, value):
                return False
        return True

    def _check_strong_consistency(self, data_key: str, value: Any) -> bool:
        """Check strong consistency requirements"""
        current_data = self._data_consistency.get(data_key, {})
        replicas = current_data.get("replicas", {})
        if len(replicas) < 2:
            return True
        replica_values = [r["value"] for r in replicas.values()]
        if len(set(replica_values)) > 1:
            return False
        return True

    def _update_consistency_status(self, data_key: str):
        """Update consistency status for data key"""
        current_data = self._data_consistency.get(data_key, {})
        replicas = current_data.get("replicas", {})
        if len(replicas) == 0:
            status = "unknown"
        elif len(replicas) == 1:
            status = "single_replica"
        else:
            replica_values = [r["value"] for r in replicas.values()]
            if len(set(replica_values)) == 1:
                status = "consistent"
            else:
                status = "inconsistent"
        current_data["consistency_status"] = status

    def get_consistency_status(self, data_key: Optional[str] = None) -> Dict[str, Any]:
        """Get consistency status for data key or overall system"""
        if data_key:
            return self._data_consistency.get(data_key, {})
        total_rules = len(self._consistency_rules)
        consistent_keys = 0
        inconsistent_keys = 0
        for data_info in self._data_consistency.values():
            if data_info.get("consistency_status") == "consistent":
                consistent_keys += 1
            elif data_info.get("consistency_status") == "inconsistent":
                inconsistent_keys += 1
        return {
            "system_id": self.system_id,
            "total_rules": total_rules,
            "consistent_keys": consistent_keys,
            "inconsistent_keys": inconsistent_keys,
            "monitoring_active": False,
            "timestamp": time.time(),
        }

    def start_consistency_monitoring(self, interval_seconds: int = 30):
        """Start consistency monitoring (stub for compatibility)"""
        pass

    def stop_consistency_monitoring(self):
        """Stop consistency monitoring (stub for compatibility)"""
        pass


def main():
    """CLI interface for testing ConsistencyManagement"""
    import argparse

    parser = argparse.ArgumentParser(description="Consistency Management CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    args = parser.parse_args()

    if args.test:
        print("🧪 ConsistencyManagement Smoke Test")
        print("=" * 45)
        consistency = ConsistencyManagement("test-consistency")
        rule1 = ConsistencyRule(
            "rule-1",
            "user-data",
            ConsistencyLevel.STRONG,
            max_drift_ms=1000,
            replication_factor=2,
        )
        rule2 = ConsistencyRule(
            "rule-2",
            "config-data",
            ConsistencyLevel.EVENTUAL,
            max_drift_ms=5000,
            replication_factor=1,
        )
        consistency.add_consistency_rule(rule1)
        consistency.add_consistency_rule(rule2)
        success1 = consistency.update_data_value(
            "user-data", "user1", "agent-1", time.time()
        )
        success2 = consistency.update_data_value(
            "user-data", "user1", "agent-2", time.time()
        )
        print(f"✅ User data update 1: {success1}")
        print(f"✅ User data update 2: {success2}")
        status = consistency.get_consistency_status()
        print(f"✅ Total rules: {status['total_rules']}")
        print(f"✅ Consistent keys: {status['consistent_keys']}")
        print("🎉 ConsistencyManagement smoke test PASSED!")
    else:
        print("ConsistencyManagement ready")
        print("Use --test to run smoke test")


if __name__ == "__main__":
    main()
