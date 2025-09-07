#!/usr/bin/env python3
"""
Check all agent statuses and points
"""

import json

def check_agent_statuses():
    try:
        with open('meeting.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        agents = data.get('agent_status', {})
        
        print("AGENT COMPETITION STATUS")
        print("=" * 50)
        
        agent_points = []
        for agent, info in agents.items():
            points = info.get('extra_credit_earned', 0)
            status = info.get('status', 'Unknown')
            role = info.get('role', 'Unknown')
            agent_points.append((agent, points, status, role))
        
        # Sort by points (highest first)
        agent_points.sort(key=lambda x: x[1], reverse=True)
        
        for i, (agent, points, status, role) in enumerate(agent_points):
            rank = i + 1
            if rank == 1:
                rank_symbol = "🥇"
            elif rank == 2:
                rank_symbol = "🥈"
            elif rank == 3:
                rank_symbol = "🥉"
            else:
                rank_symbol = f"{rank}."
            
            print(f"{rank_symbol} {agent}: {points} pts")
            print(f"   Role: {role}")
            print(f"   Status: {status}")
            print()
        
        # Competition analysis
        print("=" * 50)
        print("COMPETITION ANALYSIS")
        
        if len(agent_points) >= 2:
            leader = agent_points[0]
            second = agent_points[1]
            gap = leader[1] - second[1]
            
            print(f"🏆 Current Leader: {leader[0]} with {leader[1]} points")
            print(f"🥈 Second Place: {second[0]} with {second[1]} points")
            print(f"📊 Lead: {gap} points")
            
            # Check if Agent-5 can catch up
            agent5_points = next((points for agent, points, _, _ in agent_points if agent == 'Agent-5'), 0)
            agent5_rank = next((i+1 for i, (agent, _, _, _) in enumerate(agent_points) if agent == 'Agent-5'), 0)
            
            print(f"\n🎯 Agent-5 Status:")
            print(f"   Current Rank: #{agent5_rank}")
            print(f"   Current Points: {agent5_points}")
            
            if agent5_rank > 1:
                points_needed = leader[1] - agent5_points
                print(f"   Points needed to lead: {points_needed}")
                
                # Check available contracts
                with open('task_list.json', 'r', encoding='utf-8') as f:
                    task_data = json.load(f)
                
                available_points = 0
                for cat_name, cat_data in task_data.get('contracts', {}).items():
                    for contract in cat_data.get('contracts', []):
                        if contract.get('status') == 'AVAILABLE':
                            available_points += contract.get('extra_credit_points', 0)
                
                print(f"   Available contracts total: {available_points} points")
                
                if available_points >= points_needed:
                    print(f"   ✅ ENOUGH CONTRACTS AVAILABLE TO TAKE THE LEAD!")
                else:
                    print(f"   ⚠️ Need {points_needed - available_points} more points to take the lead")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_agent_statuses()
