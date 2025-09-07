#!/usr/bin/env python3
"""
Perpetual Motion Workflow Executor
Executes the --get-next-task protocol for Agent-5
"""

import json
import datetime
from pathlib import Path

def execute_perpetual_motion():
    """Execute the perpetual motion workflow protocol"""
    
    print("🚀 PERPETUAL MOTION WORKFLOW EXECUTOR")
    print("=" * 50)
    print("Agent-5: SPRINT ACCELERATION REFACTORING TOOL PREPARATION MANAGER")
    print("Mission: Restore system momentum and reach INNOVATION PLANNING MODE")
    print()
    
    try:
        # Load contract data
        with open('task_list.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("✅ Contract system loaded successfully")
        
        # Check Agent-5 status
        agent5_claimed = []
        agent5_completed = []
        
        for cat_name, cat_data in data.get('contracts', {}).items():
            for contract in cat_data.get('contracts', []):
                if contract.get('claimed_by') == 'Agent-5':
                    if contract.get('status') == 'CLAIMED':
                        agent5_claimed.append(contract)
                    elif contract.get('status') == 'COMPLETED':
                        agent5_completed.append(contract)
        
        print(f"📊 Agent-5 Status:")
        print(f"   Claimed contracts: {len(agent5_claimed)}")
        print(f"   Completed contracts: {len(agent5_completed)}")
        
        # Find available contracts
        available = []
        for cat_name, cat_data in data.get('contracts', {}).items():
            for contract in cat_data.get('contracts', []):
                if contract.get('status') == 'AVAILABLE':
                    available.append({
                        'contract': contract,
                        'category': cat_data.get('category', 'unknown'),
                        'manager': cat_data.get('manager', 'unknown')
                    })
        
        print(f"   Available contracts: {len(available)}")
        print()
        
        # Execute perpetual motion protocol
        print("🔄 EXECUTING PERPETUAL MOTION PROTOCOL")
        print("=" * 50)
        
        if available:
            # Sort by points (highest first)
            available.sort(key=lambda x: x['contract'].get('extra_credit_points', 0), reverse=True)
            
            print("🎯 HIGHEST VALUE AVAILABLE CONTRACTS:")
            for i, item in enumerate(available[:5]):
                contract = item['contract']
                points = contract.get('extra_credit_points', 0)
                print(f"   {i+1}. {contract['contract_id']}: {contract['title']} ({points} pts)")
                print(f"      Category: {item['category']}")
                print(f"      Manager: {item['manager']}")
                print()
            
            # Recommend next contract to claim
            best_contract = available[0]
            contract = best_contract['contract']
            
            print("🚀 RECOMMENDED NEXT CONTRACT:")
            print(f"   Contract ID: {contract['contract_id']}")
            print(f"   Title: {contract['title']}")
            print(f"   Points: {contract['extra_credit_points']}")
            print(f"   Category: {best_contract['category']}")
            print()
            
            # Execute contract claiming
            print("⚡ EXECUTING CONTRACT CLAIMING...")
            
            # Update contract status
            contract['status'] = 'CLAIMED'
            contract['claimed_by'] = 'Agent-5'
            contract['claimed_at'] = datetime.datetime.now().isoformat() + 'Z'
            contract['progress'] = '0% Complete - In Progress'
            
            # Save updated contracts
            with open('task_list.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ SUCCESSFULLY CLAIMED: {contract['contract_id']}")
            print(f"   Status: CLAIMED by Agent-5")
            print(f"   Progress: 0% Complete - In Progress")
            print(f"   Next Action: Begin execution immediately")
            
        else:
            print("⚠️ No available contracts found")
            print("   All contracts are either claimed or completed")
            print("   Check for completed contracts that can be marked as finished")
        
        # Check for contracts that can be completed
        print()
        print("🔍 CONTRACTS READY FOR COMPLETION:")
        for contract in agent5_claimed:
            progress = contract.get('progress', 'Unknown')
            if 'In Progress' in progress:
                print(f"   - {contract['contract_id']}: {contract['title']}")
                print(f"     Progress: {progress}")
                print(f"     Points: {contract.get('extra_credit_points', 0)}")
                print()
        
        print("🎯 PERPETUAL MOTION PROTOCOL EXECUTED SUCCESSFULLY!")
        print("   Next Action: Execute claimed contracts and maintain momentum")
        
    except Exception as e:
        print(f"❌ Error executing perpetual motion protocol: {e}")
        print("   System restoration may be required")

if __name__ == "__main__":
    execute_perpetual_motion()
