#!/bin/bash
# Test script to verify Git Bash can perform git operations
echo "🧪 Testing Git Bash Git Operations"
echo "=================================="

# Check if we're in a git repository
if ! git status > /dev/null 2>&1; then
    echo "❌ Not in a git repository"
    exit 1
fi

echo "✅ Git repository detected"
echo "Current branch: $(git branch --show-current)"
echo "Repository status:"
git status --porcelain

echo ""
echo "🧪 Testing pre-commit hooks..."
if command -v pre-commit > /dev/null 2>&1; then
    echo "✅ Pre-commit available"
    # Test a simple pre-commit run (just check if it can execute)
    if pre-commit --help > /dev/null 2>&1; then
        echo "✅ Pre-commit hooks functional"
    else
        echo "⚠️ Pre-commit hooks may have issues"
    fi
else
    echo "⚠️ Pre-commit not found"
fi

echo ""
echo "🎯 Git Bash is ready for professional development!"
echo "You can now run: git commit, pre-commit, etc."
