#!/usr/bin/env python3
print("=== INTEGRATION FRAMEWORK EXTENSION TEST ===")
print("Testing all connectors in the integration framework...")
import subprocess

connectors = [
    "simple_connector.py",
    "rest_api_connector.py",
    "discord_connector.py",
    "file_system_connector.py",
    "auth_connector.py",
    "monitoring_connector.py",
]
for connector in connectors:
    print(f"Testing {connector}...")
    result = subprocess.run(["python", connector], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"  ✅ {connector}: {result.stdout.strip()}")
        print(f"  ❌ {connector}: Failed")
print("\\n=== INTEGRATION TEST COMPLETE ===")
