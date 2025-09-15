#!/usr/bin/env bash
set -euo pipefail

# Example usage of the improved coordinate validation and messaging system
# This script demonstrates the new CLI commands for validation and message delivery

echo "🔍 Validating agent coordinates..."
python -m src.services.consolidated_messaging_service_new --coords cursor_agent_coords.json validate --report --show

echo ""
echo "📤 Sending test message to Agent-1..."
python -m src.services.consolidated_messaging_service_new --coords cursor_agent_coords.json send --agent Agent-1 --message "Ping from Captain"

echo ""
echo "📢 Broadcasting system maintenance message..."
python -m src.services.consolidated_messaging_service_new --coords cursor_agent_coords.json broadcast --message "System maintenance at 23:00"

echo ""
echo "✅ Validation and messaging examples completed!"
