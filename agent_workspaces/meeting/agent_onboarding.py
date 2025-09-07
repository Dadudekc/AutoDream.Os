#!/usr/bin/env python3
"""
Agent Onboarding Protocol
Executes onboarding for Agent-5 with contract review
"""

import json
import os
from pathlib import Path

def execute_onboarding():
    """Execute the agent onboarding protocol"""
    
    print("🚨 AGENT ONBOARDING - IMMEDIATE EXECUTION!")
    print("=" * 60)
    print("Agent-5: Coding Standards Implementation Specialist")
    print("Contract: Coding Standards Implementation - 350 points")
    print("Objective: Restore system momentum and reach INNOVATION PLANNING MODE")
    print()
    
    try:
        # Load contract data
        with open('task_list.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("✅ Contract system loaded successfully")
        print()
        
        # Check Agent-5 contract status
        print("📋 AGENT-5 CONTRACT STATUS:")
        print("-" * 40)
        
        agent5_claimed = []
        agent5_completed = []
        
        for cat_name, cat_data in data.get('contracts', {}).items():
            for contract in cat_data.get('contracts', []):
                if contract.get('claimed_by') == 'Agent-5':
                    if contract.get('status') == 'CLAIMED':
                        agent5_claimed.append(contract)
                    elif contract.get('status') == 'COMPLETED':
                        agent5_completed.append(contract)
        
        print(f"Claimed contracts: {len(agent5_claimed)}")
        print(f"Completed contracts: {len(agent5_completed)}")
        print()
        
        # Display claimed contracts
        if agent5_claimed:
            print("🔄 CLAIMED CONTRACTS (IMMEDIATE COMPLETION REQUIRED):")
            total_points = 0
            for contract in agent5_claimed:
                points = contract.get('extra_credit_points', 0)
                total_points += points
                print(f"  - {contract['contract_id']}: {contract['title']} ({points} pts)")
                print(f"    Progress: {contract.get('progress', 'Unknown')}")
                print()
            print(f"Total potential points: {total_points}")
            print()
        
        # Display completed contracts
        if agent5_completed:
            print("✅ COMPLETED CONTRACTS:")
            total_completed = 0
            for contract in agent5_completed:
                points = contract.get('extra_credit_points', 0)
                total_completed += points
                print(f"  - {contract['contract_id']}: {contract['title']} ({points} pts)")
            print(f"Total points earned: {total_completed}")
            print()
        
        # Check for Coding Standards Implementation contract
        print("🎯 CODING STANDARDS IMPLEMENTATION CONTRACT SEARCH:")
        print("-" * 50)
        
        coding_standards_contract = None
        for cat_name, cat_data in data.get('contracts', {}).items():
            for contract in cat_data.get('contracts', []):
                if 'coding standards' in contract.get('title', '').lower():
                    coding_standards_contract = contract
                    break
            if coding_standards_contract:
                break
        
        if coding_standards_contract:
            print(f"✅ Found: {coding_standards_contract['contract_id']}")
            print(f"   Title: {coding_standards_contract['title']}")
            print(f"   Points: {coding_standards_contract.get('extra_credit_points', 0)}")
            print(f"   Status: {coding_standards_contract.get('status', 'Unknown')}")
            print(f"   Category: {cat_name}")
        else:
            print("⚠️ Coding Standards Implementation contract not found")
            print("   May need to be claimed or created")
        
        print()
        
        # Onboarding directory review
        print("📚 ONBOARDING DIRECTORY REVIEW:")
        print("-" * 40)
        
        onboarding_path = Path("../../onboarding")
        if onboarding_path.exists():
            print(f"✅ Onboarding directory found: {onboarding_path.absolute()}")
            
            # List onboarding files
            onboarding_files = list(onboarding_path.glob("*.md")) + list(onboarding_path.glob("*.json"))
            if onboarding_files:
                print("   Available training materials:")
                for file in onboarding_files[:5]:  # Show first 5
                    print(f"     - {file.name}")
                if len(onboarding_files) > 5:
                    print(f"     ... and {len(onboarding_files) - 5} more files")
            else:
                print("   No training materials found")
        else:
            print(f"⚠️ Onboarding directory not found at: {onboarding_path.absolute()}")
        
        print()
        
        # System overview
        print("🔄 SYSTEM OVERVIEW:")
        print("-" * 40)
        print("Multiagentic feedback loop system")
        print("Continuous improvement and quality assurance")
        print("Devlog system for transparency and coordination")
        print("Coding standards compliance required")
        print()
        
        # Immediate action plan
        print("⚡ IMMEDIATE ACTION PLAN:")
        print("-" * 40)
        print("1. Complete claimed contracts immediately")
        print("2. Submit deliverables with maximum quality")
        print("3. Update devlog with progress")
        print("4. Claim next contract to maintain momentum")
        print("5. Help restore system functionality")
        print()
        
        print("🎯 ONBOARDING PROTOCOL EXECUTED SUCCESSFULLY!")
        print("   Next Action: Begin contract execution immediately")
        
    except Exception as e:
        print(f"❌ Error executing onboarding protocol: {e}")
        print("   System restoration may be required")

if __name__ == "__main__":
    execute_onboarding()
