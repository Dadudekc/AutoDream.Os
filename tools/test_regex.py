#!/usr/bin/env python3
import re

# Test different patterns
test_line = 'CYCLE_DONE Agent-3 c001 ["Scanned 712 Python files", "Found 26 estimated duplicates", "Identified 10 V2 violations", "Generated 3 reports"] "Project scan complete, ready for duplicate analysis"'

patterns = [
    r"CYCLE_DONE\s+(\w+)\s+(\w+)\s+\[(.*?)\]\s+\"([^\"]+)\"",
    r"CYCLE_DONE\s+(\w+)\s+(\w+)\s+\[(.*?)\]\s+\"([^\"]+)\"",
    r"CYCLE_DONE\s+(\w+)\s+(\w+)\s+\[(.*?)\]\s+\"([^\"]+)\"",
    r"CYCLE_DONE\s+(\w+)\s+(\w+)\s+\[(.*?)\]\s+\"([^\"]+)\"",
]

for i, pattern in enumerate(patterns):
    print(f"Pattern {i+1}: {pattern}")
    match = re.search(pattern, test_line)
    if match:
        print(f"✅ Match {i+1} found!")
        print("Agent:", match.group(1))
        print("Cycle ID:", match.group(2))
        print("Metrics:", match.group(3)[:50] + "...")
        print("Summary:", match.group(4))
        break
    else:
        print(f"❌ Pattern {i+1} failed")

# Let's try a more flexible approach
print("\n--- Flexible approach ---")
flexible_pattern = r"CYCLE_DONE\s+(\w+)\s+(\w+)\s+\[(.*?)\]\s+\"([^\"]+)\""
match = re.search(flexible_pattern, test_line, re.DOTALL)
if match:
    print("✅ Flexible pattern works!")
    print("Agent:", match.group(1))
    print("Cycle ID:", match.group(2))
    print("Metrics:", match.group(3)[:50] + "...")
    print("Summary:", match.group(4))
else:
    print("❌ Flexible pattern failed")
    
    # Debug: show what we're actually matching
    print("\n--- Debug ---")
    print("Looking for:", "CYCLE_DONE")
    print("In line:", test_line)
    print("Found CYCLE_DONE:", "CYCLE_DONE" in test_line)