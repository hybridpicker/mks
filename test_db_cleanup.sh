#!/bin/bash

echo "🧪 Testing database cleanup functionality..."

cd /Users/lukasschonsgibl/Coding/Django/mks

# Test database cleanup
echo "Attempting to clean up test database..."

# Try PostgreSQL
if command -v dropdb &> /dev/null; then
    echo "✅ PostgreSQL dropdb command available"
    dropdb test_mks 2>/dev/null && echo "✅ Dropped test_mks" || echo "⚠️  No test_mks database to drop"
else
    echo "⚠️  PostgreSQL dropdb not available"
fi

# Try psql
if command -v psql &> /dev/null; then
    echo "✅ PostgreSQL psql command available"
    psql -c "DROP DATABASE IF EXISTS test_mks;" 2>/dev/null && echo "✅ Dropped test_mks via psql" || echo "⚠️  Could not connect to PostgreSQL"
else
    echo "⚠️  PostgreSQL psql not available"
fi

# Test Django test run (just check if it starts properly)
echo "Testing Django test command..."
if command -v python3 &> /dev/null; then
    echo "Testing if Django tests can start..."
    timeout 10s python3 manage.py test --dry-run 2>/dev/null && echo "✅ Django tests can run" || echo "⚠️  Django test setup needs attention"
else
    echo "⚠️  Python3 not available"
fi

echo "✅ Database cleanup test completed"
