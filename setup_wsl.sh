#!/bin/bash
# WSL Setup Script for Agent Cellphone V2 Project
# Run this script in WSL after installation

set -e

echo "🚀 Setting up WSL environment for Agent Cellphone V2 Project..."

# Update package list
echo "📦 Updating package list..."
sudo apt update

# Install Python 3.11 and essential tools
echo "🐍 Installing Python 3.11 and tools..."
sudo apt install -y python3.11 python3.11-pip python3.11-venv python3.11-dev
sudo apt install -y git curl wget build-essential

# Install Python packages
echo "📚 Installing Python packages..."
pip3 install --upgrade pip
pip3 install pre-commit
pip3 install -r requirements.txt

# Set up pre-commit hooks
echo "🔧 Setting up pre-commit hooks..."
pre-commit install

# Test pre-commit hooks
echo "🧪 Testing pre-commit hooks..."
pre-commit run --all-files || echo "⚠️  Some hooks may fail initially - this is normal"

# Test Python imports
echo "🐍 Testing Python imports..."
python3 -c "import src.services.messaging_core; print('✅ Import successful')" || echo "⚠️  Import test failed - check dependencies"

# Test messaging CLI
echo "📱 Testing messaging CLI..."
python3 -m src.services.messaging_cli --check-status || echo "⚠️  Messaging CLI test failed - check configuration"

echo "✅ WSL setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Configure Git: git config --global user.name 'Your Name'"
echo "2. Configure Git: git config --global user.email 'your.email@example.com'"
echo "3. Test commit: git add . && git commit -m 'test: WSL setup'"
echo "4. No more --no-verify flag needed! 🎉"
echo ""
echo "WE. ARE. SWARM. ⚡️🔥🏆"
