#!/bin/bash

# Test Script for Pre-Push Hook
# =============================
# This script tests the pre-push hook functionality without actually pushing

echo "=== Testing MKS Pre-Push Hook ==="
echo

# Change to project directory
cd /Users/lukasschonsgibl/Coding/Django/mks

# Show current git status
echo "Current git status:"
git status --short
echo

# Check if there are any CSS files in the staging area
echo "CSS files in staging area:"
git diff --cached --name-only | grep '\.css$' || echo "No CSS files staged"
echo

# Test the hook by running it directly
echo "Running pre-push hook..."
echo "========================="

# Run the pre-push hook
.git/hooks/pre-push

HOOK_EXIT_CODE=$?

echo
echo "========================="
if [ $HOOK_EXIT_CODE -eq 0 ]; then
    echo "✅ Pre-push hook completed successfully"
else
    echo "❌ Pre-push hook failed with exit code: $HOOK_EXIT_CODE"
fi

echo
echo "=== Hook Test Completed ==="
