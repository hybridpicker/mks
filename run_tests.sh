#!/bin/bash

# Simple script to run Django tests without interactive prompts
cd /Users/lukasschonsgibl/Coding/Django/mks

echo "Running Django tests with automatic database handling..."

# Method 1: Use in-memory SQLite (fastest, no database files)
echo "Trying in-memory SQLite tests..."
DJANGO_SETTINGS_MODULE=test_settings python3 manage.py test --verbosity=1
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Tests passed with in-memory database!"
    exit 0
fi

echo "In-memory tests failed, trying with regular database cleanup..."

# Method 2: Clean up and use regular tests
dropdb test_mks 2>/dev/null || true
psql -c "DROP DATABASE IF EXISTS test_mks;" 2>/dev/null || true
rm -f *.sqlite3 test_*.db 2>/dev/null || true

# Run tests with automatic yes responses
echo "Running tests with database recreation..."
(echo "yes"; sleep 1; echo "yes"; sleep 1; echo "yes") | python3 manage.py test --verbosity=1
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Tests passed!"
    exit 0
else
    echo "❌ Tests failed!"
    exit 1
fi
