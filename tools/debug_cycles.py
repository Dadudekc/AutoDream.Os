#!/usr/bin/env python3
import re

# Test the exact content from the devlog
test_content = '''# Agent-3 Devlog

## CYCLE START: c001 - 2025-10-04 20:34:54

## CYCLE COMPLETE: c001 - 2025-10-04 20:40:00

CYCLE_DONE Agent-3 c001 ["Scanned 712 Python files", "Found 26 estimated duplicates", "Identified 10 V2 violations", 
"Generated 3 reports"] "Project scan complete, ready for duplicate analysis"'''

print("Testing multiline CYCLE_DONE parsing...")
print("Content:", repr(test_content))
print()

# Try the multiline approach
lines = test_content.split('\n')
current_line = ""
for line_num, line in enumerate(lines, 1):
    current_line += line.strip() + " "
    if "CYCLE_DONE" in current_line and current_line.count('"') >= 2:
        print(f"Found potential CYCLE_DONE at line {line_num}")
        print("Current line:", repr(current_line.strip()))
        
        # Test the regex
        pattern = r"CYCLE_DONE\s+(\w+)\s+(\w+)\s+\[(.*?)\]\s+\"([^\"]+)\""
        match = re.search(pattern, current_line.strip())
        if match:
            print("✅ Regex match found!")
            print("Agent:", match.group(1))
            print("Cycle ID:", match.group(2))
            print("Metrics:", match.group(3)[:50] + "...")
            print("Summary:", match.group(4))
        else:
            print("❌ Regex match failed")
            # Try a simpler approach
            simple_match = re.search(r"CYCLE_DONE\s+(\w+)\s+(\w+)", current_line.strip())
            if simple_match:
                print("✅ Simple match works:", simple_match.groups())
        
        current_line = ""  # Reset for next cycle
