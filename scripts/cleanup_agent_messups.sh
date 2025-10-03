#!/bin/bash
# Agent Mess-Up Cleanup Script
# Removes files created due to agent misunderstandings

echo "🧹 AGENT MESS-UP CLEANUP SCRIPT"
echo "================================"

# Safety check
read -p "This will delete many files. Are you sure? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cleanup cancelled."
    exit 1
fi

echo "Starting cleanup..."

# 1. Delete agent-specific prefix files
echo "1. Removing agent-specific prefix files..."
rm -rf /workspace/tsla_forecast_app/agent_tasks/
rm -rf /workspace/tests/agent3_database/
rm -f /workspace/devlogs/agent*
rm -f /workspace/devlogs/archive/agent*

# 2. Delete phase-specific files
echo "2. Removing phase-specific files..."
rm -f /workspace/src/integration/phase*

# 3. Delete complex coordination systems
echo "3. Removing complex coordination systems..."
rm -f /workspace/src/integration/*system*.py
rm -f /workspace/src/integration/*coordination*.py
rm -f /workspace/src/integration/*consolidation*.py

# 4. Delete V3 confusion files
echo "4. Removing V3 confusion files..."
rm -rf /workspace/src/v3/
rm -f /workspace/src/integration/v3_*

# 5. Delete duplicate implementations
echo "5. Removing duplicate implementations..."
rm -f /workspace/workspaces/infrastructure/data_backup_validation_strategy.md
rm -f /workspace/agent_workspaces/Agent-3/data_backup_validation_strategy.md

# 6. Clean up agent workspaces
echo "6. Cleaning up agent workspaces..."
rm -rf /workspace/agent_workspaces/

echo "✅ Cleanup completed!"
echo ""
echo "📊 SUMMARY:"
echo "- Removed agent-specific prefix files"
echo "- Removed phase-specific files" 
echo "- Removed complex coordination systems"
echo "- Removed V3 confusion files"
echo "- Removed duplicate implementations"
echo "- Cleaned up agent workspaces"
echo ""
echo "🎯 Agents should now use:"
echo "- Messaging system for communication"
echo "- Workflow chains for coordination"
echo "- Proper naming conventions"
echo "- Clean modular architecture"