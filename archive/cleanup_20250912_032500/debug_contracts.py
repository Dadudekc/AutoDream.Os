#!/usr/bin/env python3
import json
import os
from pathlib import Path

contracts_dir = Path("contracts")
available_contracts = []

print("Scanning contracts directory...")
for json_file in contracts_dir.glob("*.json"):
    if json_file.name.startswith("TEMPLATE"):
        continue

    print(f"Checking file: {json_file.name}")
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            contract = json.load(f)

        status = contract.get("status")
        agent_id = contract.get("agent_id")
        print(f"  Status: {status}, Agent: {agent_id}")

        if status == "AVAILABLE":
            available_contracts.append(contract)
            print("  ✅ ADDED TO AVAILABLE LIST")
    except Exception as e:
        print(f"  ❌ ERROR: {e}")

print(f"\nTotal available contracts found: {len(available_contracts)}")
for contract in available_contracts[:5]:  # Show first 5
    print(f"- {contract['contract_id']} for {contract['agent_id']}")
