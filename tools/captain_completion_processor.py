#!/usr/bin/env python3
"""
Captain Completion Processor - Automated Agent Completion Processing
Automatically processes agent completion messages, awards points, and sends recognition.
"""

import sys
import re
from pathlib import Path
from datetime import datetime

repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))


def extract_completion_info(content: str) -> dict:
    """Extract completion information from message content."""
    info = {
        'task': 'Unknown',
        'points': 0,
        'roi': 0,
        'status': 'complete'
    }
    
    # Extract task name
    task_patterns = [
        r'Task[:\s]+([^\n]+)',
        r'Mission[:\s]+([^\n]+)',
        r'File[:\s]+([^\n]+\.py)',
        r'Phase\s+\d+[:\s]+([^\n]+)'
    ]
    for pattern in task_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            info['task'] = match.group(1).strip()
            break
    
    # Extract points
    points_patterns = [
        r'(\d+)\s*pts',
        r'(\d+)\s*points',
        r'Points[:\s]+(\d+)'
    ]
    for pattern in points_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            info['points'] = int(match.group(1))
            break
    
    # Extract ROI
    roi_patterns = [
        r'ROI[:\s]+([\d.]+)',
        r'ROI:\s+([\d.]+)'
    ]
    for pattern in roi_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            info['roi'] = float(match.group(1))
            break
    
    return info


def generate_recognition_message(agent_id: str, info: dict) -> str:
    """Generate appropriate recognition message based on completion."""
    
    # Determine recognition level based on ROI
    if info['roi'] >= 80:
        level = "🏆 LEGENDARY EXECUTION"
        multiplier = "10x"
    elif info['roi'] >= 50:
        level = "🔥 EXCEPTIONAL EXECUTION"
        multiplier = "8x"
    elif info['roi'] >= 30:
        level = "⭐ EXCELLENT EXECUTION"
        multiplier = "5x"
    elif info['roi'] >= 20:
        level = "✨ OUTSTANDING EXECUTION"
        multiplier = "3x"
    else:
        level = "✅ SOLID EXECUTION"
        multiplier = "2x"
    
    message = f"""🎉 {agent_id} COMPLETION RECOGNIZED - {level}!

✅ Task Complete: {info['task']}
📊 Points Awarded: +{info['points']} pts
💎 ROI: {info['roi']:.2f}
⛽ Gas Multiplier: {multiplier} (Recognition delivered!)

Your execution demonstrates {level.split('-')[0].strip().lower()}! The swarm benefits from your contribution!

Keep up the outstanding work! Next task assignment incoming...

🐝 WE. ARE. SWARM. ⚡🔥"""
    
    return message


def process_completion(agent_id: str, message_file: Path) -> dict:
    """Process a single completion message."""
    
    content = message_file.read_text(encoding='utf-8')
    info = extract_completion_info(content)
    
    # Generate recognition
    recognition = generate_recognition_message(agent_id, info)
    
    return {
        'agent': agent_id,
        'task': info['task'],
        'points': info['points'],
        'roi': info['roi'],
        'recognition': recognition,
        'processed': datetime.now()
    }


def main():
    """Process recent completions and award recognition."""
    
    if len(sys.argv) < 2:
        print("Usage: python captain_completion_processor.py <agent-id> [message-file]")
        print("\nExamples:")
        print("  python captain_completion_processor.py Agent-6")
        print("  python captain_completion_processor.py Agent-6 inbox/COMPLETION.md")
        return 1
    
    agent_id = sys.argv[1]
    
    # Find completion message
    if len(sys.argv) > 2:
        msg_file = Path(sys.argv[2])
    else:
        # Look for recent completion in inbox
        inbox = repo_root / "agent_workspaces" / agent_id / "inbox"
        if not inbox.exists():
            print(f"❌ No inbox found for {agent_id}")
            return 1
        
        completion_files = [
            f for f in inbox.glob("*.md")
            if 'COMPLETE' in f.read_text(encoding='utf-8').upper() or 
               'DONE' in f.read_text(encoding='utf-8').upper()
        ]
        
        if not completion_files:
            print(f"❌ No completion messages found for {agent_id}")
            return 1
        
        # Get most recent
        msg_file = max(completion_files, key=lambda p: p.stat().st_mtime)
    
    if not msg_file.exists():
        print(f"❌ Message file not found: {msg_file}")
        return 1
    
    print(f"🔍 PROCESSING COMPLETION")
    print(f"=" * 60)
    print(f"Agent: {agent_id}")
    print(f"File: {msg_file.name}")
    print(f"=" * 60)
    print()
    
    # Process completion
    result = process_completion(agent_id, msg_file)
    
    print(f"✅ COMPLETION PROCESSED")
    print(f"-" * 60)
    print(f"Task: {result['task']}")
    print(f"Points: {result['points']}")
    print(f"ROI: {result['roi']:.2f}")
    print(f"Time: {result['processed'].strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    print(f"📨 RECOGNITION MESSAGE GENERATED")
    print(f"-" * 60)
    print(result['recognition'])
    print()
    
    print(f"🚀 NEXT STEPS")
    print(f"-" * 60)
    print(f"1. Send recognition: python -m src.services.messaging_cli --agent {agent_id} --message \"[message]\" --pyautogui")
    print(f"2. Update leaderboard: python tools/captain_leaderboard_update.py {agent_id} {result['points']}")
    print(f"3. Assign next task: python tools/captain_next_task_picker.py {agent_id}")
    print()
    
    # Save recognition to file for easy copy
    recognition_file = repo_root / "agent_workspaces" / "Agent-4" / f"RECOGNITION_{agent_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    recognition_file.write_text(result['recognition'], encoding='utf-8')
    print(f"💾 Recognition saved to: {recognition_file.relative_to(repo_root)}")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

