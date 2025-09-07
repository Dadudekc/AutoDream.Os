#!/usr/bin/env python3
"""
Quick script to check available contracts
"""

import json

def check_available_contracts():
    try:
        with open('task_list.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        available = []
        for cat_name, cat_data in data.get('contracts', {}).items():
            for contract in cat_data.get('contracts', []):
                if contract.get('status') == 'AVAILABLE':
                    available.append({
                        'id': contract.get('contract_id'),
                        'title': contract.get('title'),
                        'points': contract.get('extra_credit_points', 0),
                        'category': cat_data.get('category', 'unknown')
                    })
        
        print(f"Available contracts: {len(available)}")
        print("=" * 50)
        
        for contract in available:
            print(f"- {contract['id']}: {contract['title']} ({contract['points']} pts)")
            print(f"  Category: {contract['category']}")
            print()
            
        # Check Agent-5 status
        print("=" * 50)
        print("AGENT-5 STATUS:")
        
        # Count claimed contracts
        claimed = []
        for cat_name, cat_data in data.get('contracts', {}).items():
            for contract in cat_data.get('contracts', []):
                if contract.get('status') == 'CLAIMED' and contract.get('claimed_by') == 'Agent-5':
                    claimed.append({
                        'id': contract.get('contract_id'),
                        'title': contract.get('title'),
                        'points': contract.get('extra_credit_points', 0),
                        'progress': contract.get('progress', 'Unknown')
                    })
        
        print(f"Claimed contracts: {len(claimed)}")
        total_claimed_points = 0
        for contract in claimed:
            print(f"  - {contract['id']}: {contract['title']} ({contract['points']} pts) - {contract['progress']}")
            total_claimed_points += contract['points']
        
        print(f"Total claimed points: {total_claimed_points}")
            
        # Count completed contracts
        completed = []
        for cat_name, cat_data in data.get('contracts', {}).items():
            for contract in cat_data.get('contracts', []):
                if contract.get('status') == 'COMPLETED' and contract.get('claimed_by') == 'Agent-5':
                    completed.append({
                        'id': contract.get('contract_id'),
                        'title': contract.get('title'),
                        'points': contract.get('extra_credit_points', 0)
                    })
        
        print(f"\nCompleted contracts: {len(completed)}")
        total_completed_points = 0
        for contract in completed:
            print(f"  - {contract['id']}: {contract['title']} ({contract['points']} pts)")
            total_completed_points += contract['points']
        
        print(f"Total completed points: {total_completed_points}")
        print(f"Total points earned: {total_completed_points}")
        print(f"Total potential points (claimed + completed): {total_claimed_points + total_completed_points}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_available_contracts()
