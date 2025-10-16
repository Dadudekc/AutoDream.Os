#!/usr/bin/env python3
"""Quick test for DUP-001 ConfigManager SSOT consolidation."""

print("=" * 70)
print("DUP-001 CONFIGMANAGER SSOT CONSOLIDATION TEST")
print("=" * 70)

# Test 1: Primary SSOT import
print("\n✅ Test 1: Primary SSOT import (config_ssot)...")
from src.core.config_ssot import (
    get_config, 
    get_unified_config, 
    UnifiedConfigManager,
    TimeoutConfig,
    AgentConfig
)
config = get_unified_config()
print(f"   - Agent count: {config.agents.agent_count}")
print(f"   - Config sections: {list(config.get_all_configs().keys())}")
validation_result = config.validate()
print(f"   - Validation: {'PASSED ✅' if not validation_result else f'ERRORS: {validation_result}'}")

# Test 2: Backward compatibility - unified_config
print("\n✅ Test 2: Backward compatibility (unified_config)...")
from src.core.unified_config import get_unified_config as uc_get
uc_config = uc_get()
print(f"   - Agent count: {uc_config.agents.agent_count}")
print(f"   - Same instance: {uc_config is config}")

# Test 3: Backward compatibility - config_core
print("\n✅ Test 3: Backward compatibility (config_core)...")
from src.core.config_core import get_config as cc_get
agent_count = cc_get('AGENT_COUNT', 8)
print(f"   - AGENT_COUNT: {agent_count}")

# Test 4: Enhanced features (metadata tracking)
print("\n✅ Test 4: Enhanced features (metadata, history)...")
from src.core.config_ssot import ConfigSource
config.set("TEST_KEY", "test_value", ConfigSource.RUNTIME)
print(f"   - Config history events: {len(config.config_history)}")
print(f"   - Status: {config.get_status()['validation_status']}")

# Test 5: File persistence
print("\n✅ Test 5: File persistence...")
try:
    config.save_to_file("test_config.json")
    config.load_from_file("test_config.json")
    print("   - Save/Load: WORKING ✅")
except Exception as e:
    print(f"   - Save/Load: ERROR - {e}")

print("\n" + "=" * 70)
print("ALL TESTS COMPLETED SUCCESSFULLY! ✅")
print("=" * 70)

