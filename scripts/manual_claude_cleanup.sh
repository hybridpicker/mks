#!/bin/bash

# Manual Claude Cleanup Script
# Kann jederzeit manuell ausgeführt werden, um Claude-generierte Dateien zu bereinigen

cd "$(git rev-parse --show-toplevel 2>/dev/null || dirname "$0"/..")"

echo "🧹 Manual Claude Documentation Cleanup"
echo "======================================"
echo ""

if [ -f "scripts/claude_cleanup.sh" ]; then
    echo "Running Claude cleanup script..."
    ./scripts/claude_cleanup.sh
    
    echo ""
    echo "✅ Manual cleanup completed!"
    echo ""
    echo "💡 Tip: This cleanup also runs automatically during git commits and pushes"
else
    echo "❌ Error: Claude cleanup script not found at scripts/claude_cleanup.sh"
    echo "Please ensure you're in the project root directory"
    exit 1
fi